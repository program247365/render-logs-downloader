#!/usr/bin/env python3
import requests
import json
from datetime import datetime, timedelta
import time
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description='Download Render service logs')
    parser.add_argument('--auth-token', required=True, help='Render API authentication token')
    parser.add_argument('--service-id', required=True, help='Render service ID')
    parser.add_argument('--date', help='Date to download logs for in YYYYMMDD format (defaults to last 24 hours)')
    return parser.parse_args()

# Get command line arguments
args = parse_args()

# Configuration
SERVICE_ID = args.service_id
AUTH_TOKEN = args.auth_token

# Calculate time range
if args.date:
    # Parse the date argument
    try:
        target_date = datetime.strptime(args.date, '%Y%m%d')
        # Set time range for the entire specified day (UTC)
        start_time = target_date.isoformat() + "Z"
        end_time = (target_date + timedelta(days=1)).isoformat() + "Z"
        current_date = args.date
    except ValueError:
        print("Error: Date must be in YYYYMMDD format")
        exit(1)
else:
    # Default: last 24 hours
    end_time = datetime.utcnow().isoformat() + "Z"
    start_time = (datetime.utcnow() - timedelta(hours=24)).isoformat() + "Z"
    current_date = datetime.utcnow().strftime('%Y%m%d')

OUTPUT_FILE = f"{current_date}_render_logs.txt"

# GraphQL query
query = """
query logs($query: LogQueryInput!) {
  logs(query: $query) {
    logs {
      id
      labels {
        label
        value
      }
      timestamp
      text
    }
    nextEndTime
    nextStartTime
    hasMore
  }
}
"""

# Headers
headers = {
    "Content-Type": "application/json",
    "Authorization": AUTH_TOKEN if AUTH_TOKEN.startswith("Bearer ") else f"Bearer {AUTH_TOKEN}"
}

def fetch_logs(start=None, end=None):
    """Fetch logs from Render API with pagination"""
    has_more = True
    current_start = start
    current_end = end
    
    # Open file for appending
    with open(OUTPUT_FILE, "a") as f:
        f.write(f"=== LOGS FROM {start} TO {end} ===\n\n")
        
        while has_more:
            # Prepare the request variables
            variables = {
                "query": {
                    "start": current_start,
                    "end": current_end,
                    "filters": [
                        {"field": "SERVICE", "values": [SERVICE_ID], "operator": "INCLUDES"},
                        {"field": "LOG_TYPE", "operator": "INCLUDES", "values": ["app", "request"]}
                    ],
                    "ownerId": "tea-cviu8aggjchc73c07or0",
                    "pageSize": 50,
                    "region": "ohio",
                    "direction": "BACKWARD"
                }
            }
            
            # Make the request
            response = requests.post(
                "https://api.render.com/graphql",
                headers=headers,
                json={"query": query, "variables": variables}
            )
            
            if response.status_code != 200:
                print(f"Error: {response.status_code}")
                print(response.text)
                break
                
            result = response.json()
            
            # Extract logs
            logs_data = result.get("data", {}).get("logs", {})
            logs = logs_data.get("logs", [])
            
            # Write logs to file
            for log in logs:
                timestamp = log.get("timestamp")
                text = log.get("text", "")
                f.write(f"[{timestamp}] {text}\n")
            
            print(f"Fetched {len(logs)} logs")
            
            # Check if there are more logs to fetch
            has_more = logs_data.get("hasMore", False)
            
            if has_more:
                # Update pagination parameters based on direction
                current_end = logs_data.get("nextEndTime")
                time.sleep(0.5)  # Add a small delay to avoid rate limiting

# Run the script
if __name__ == "__main__":
    if args.date:
        print(f"Downloading logs for {args.date} to {OUTPUT_FILE}")
    else:
        print(f"Downloading logs for the last 24 hours to {OUTPUT_FILE}")
    fetch_logs(start=start_time, end=end_time)
    print("Download complete!")
