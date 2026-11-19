# Automated Multi-Platform Posting System

A FastAPI application that validates a promotional message (<= 200 chars, exactly 1 valid CTA URL) and publishes it concurrently across 5 third-party platforms via REST APIs.

## Supported Platforms
1. **GitHub Gist** (`POST https://api.github.com/gists`)
2. **Telegraph** (`POST https://api.telegra.ph/createPage`)
3. **Pastebin** (`POST https://pastebin.com/api/api_post.php`)
4. **Dev.to** (`POST https://dev.to/api/articles`)
5. **Mastodon** (`POST https://mastodon.social/api/v1/statuses`)

## Setup & Local Execution

1. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Configure environment variables:**
   ```bash
   cp .env.example .env
   # Add your API keys/tokens to .env
   ```

3. **Run the server:**
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 4000
   ```

4. **Open Swagger API Docs:**
   Navigate to `http://localhost:4000/docs`

5. **Run Tests:**
   ```bash
   pytest -v
   ```

## Sample Request & Response

### Request
```bash
curl -X POST "http://localhost:4000/posting" \
  -H "Content-Type: application/json" \
  -d '{"message": "Check out our latest business platform and grow your online visibility. https://example.com"}'
```

### Response
```json
{
  "success": true,
  "results": [
    {
      "platform": "GitHub Gist",
      "status": "success",
      "posted_url": "https://gist.github.com/username/8f9a2b3c4d5e",
      "public_access": true,
      "date": "2026-11-19",
      "time": "08:05:12",
      "error": null
    },
    {
      "platform": "Telegraph",
      "status": "success",
      "posted_url": "https://telegra.ph/Check-out-our-latest-business-platform-11-19",
      "public_access": true,
      "date": "2026-11-19",
      "time": "08:05:13",
      "error": null
    },
    {
      "platform": "Pastebin",
      "status": "failed",
      "posted_url": null,
      "public_access": false,
      "date": null,
      "time": null,
      "error": "Missing PASTEBIN_API_KEY environment variable"
    }
  ]
}
```
