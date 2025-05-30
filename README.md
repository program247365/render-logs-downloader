# Render Logs Downloader

This script downloads logs from your Render.com service for the last 24 hours by default and saves them to a dated log file. You can also specify a specific date to download logs for.

## Prerequisites

- Python 3.x
- `requests` library (`pip install requests`)
- [uv](https://github.com/astral-sh/uv) (optional, for faster execution)

## How to Get the Auth Token

1. Log in to your [Render.com](https://render.com) dashboard
2. Navigate to your service
3. Go to the "Logs" tab
4. Open your browser's Developer Tools (F12 or right-click -> Inspect)
5. Go to the Network tab
6. Click "Load More" in the logs section
7. Find the GraphQL request to `api.render.com/graphql`
8. In the request headers, look for the `Authorization` header
9. Copy the token value (it starts with `Bearer `)

## Usage

### Using uv run (recommended)

```bash
# Download logs for the last 24 hours
uv run download_render_logs.py --auth-token "your-auth-token" --service-id "your-service-id"

# Download logs for a specific date
uv run download_render_logs.py --auth-token "your-auth-token" --service-id "your-service-id" --date 20240522
```

### Example

```bash
# Download last 24 hours using Python
python3 download_render_logs.py --auth-token "Bearer rnd_abc123..." --service-id "srv-xyz789..."

# Download specific date using Python
python3 download_render_logs.py --auth-token "Bearer rnd_abc123..." --service-id "srv-xyz789..." --date 20240522

# Download last 24 hours using uv
uv run download_render_logs.py --auth-token "Bearer rnd_abc123..." --service-id "srv-xyz789..."

# Download specific date using uv
uv run download_render_logs.py --auth-token "Bearer rnd_abc123..." --service-id "srv-xyz789..." --date 20240522
```

## Output

The script will create a log file named with the date in the format `YYYYMMDD_render_logs.txt`. For example:
- `20240522_render_logs.txt` for May 22, 2024 (when using --date 20240522)
- Current date when downloading the last 24 hours

The logs will include:
- Timestamp
- Log text
- Service information
- Request details

## Notes

- The script fetches logs for the last 24 hours by default
- Use the --date parameter to download logs for a specific day in YYYYMMDD format
- Logs are fetched in batches of 50 entries
- A small delay (0.5s) is added between requests to avoid rate limiting
- Using `uv run` is recommended for faster execution and better dependency management 