# YouTube Transcript API - IP Blocking Solutions

## Problem
YouTube blocks requests from cloud provider IPs (AWS, GCP, Azure, etc.), causing the error:
```
Could not retrieve a transcript - IP blocked by YouTube
```

## Solutions (Pick One)

---

### Solution 1: Use a Proxy (Recommended for Production)

The `youtube-transcript-api` supports proxies. Updated script now includes proxy support.

#### Option A: Webshare Proxy (Recommended)
1. Sign up at https://www.webshare.io (free tier available)
2. Get your proxy credentials
3. Add to `.env`:
```bash
WEBSHARE_PROXY_USERNAME=your_username
WEBSHARE_PROXY_PASSWORD=your_password
```
4. Run with proxy:
```bash
uv run python research/validate_youtube.py --use-proxy
```

#### Option B: Generic HTTP/HTTPS Proxy
If you have your own proxy:
```bash
export HTTP_PROXY=http://user:pass@proxy:port
export HTTPS_PROXY=https://user:pass@proxy:port
uv run python research/validate_youtube.py --use-proxy
```

**Pros:**
- Works from cloud servers
- Rotating IPs avoid blocks
- Production-ready

**Cons:**
- Proxy services cost money (or have limited free tier)
- Slightly slower due to proxy hop

---

### Solution 2: Run from Local Machine (Easiest)

Run the validation scripts from your local computer (not cloud):

```bash
# On your local machine (home/office internet)
git clone <repo>
cd podagent/research
uv sync
uv run python validate_youtube.py
```

**Pros:**
- Free
- No configuration needed
- Fast

**Cons:**
- Must run locally, not on cloud servers
- Not suitable for production deployment

---

### Solution 3: Use YouTube Data API v3 (Official)

Instead of the unofficial transcript API, use the official YouTube API:

1. Get API key at https://console.cloud.google.com/apis/credentials
2. Enable "YouTube Data API v3"
3. Use captions endpoint:
```python
from googleapiclient.discovery import build

youtube = build('youtube', 'v3', developerKey='YOUR_API_KEY')

# Get captions for a video
captions = youtube.captions().list(
    part='snippet',
    videoId='VIDEO_ID'
).execute()

# Download caption content
caption_content = youtube.captions().download(
    id='CAPTION_ID'
).execute()
```

**Pros:**
- Official API, stable
- No IP blocking
- Quota-based (10,000 units/day for free)

**Cons:**
- Requires OAuth for downloading captions (not just API key)
- More complex authentication
- Different data format

---

### Solution 4: Hybrid Approach (Recommended for PodAgent)

Since Podcast Index API works perfectly, use this strategy:

```
┌─────────────────────────────────────────────────────┐
│  Podcast Request                                    │
└─────────────────┬───────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────┐
│  1. Try YouTube First                               │
│     - Use proxy if available                        │
│     - If blocked → fallback to Podcast Index        │
└─────────────────┬───────────────────────────────────┘
                  │
         ┌────────┴────────┐
         │                 │
    Success            Blocked
         │                 │
         ▼                 ▼
┌─────────────┐   ┌──────────────────────┐
│ Use YouTube │   │ Use Podcast Index    │
│ Transcript  │   │ - Get MP3 URL        │
│ (fast)      │   │ - Download audio     │
│             │   │ - STT (Whisper)      │
└─────────────┘   │ (slower but works)   │
                  └──────────────────────┘
```

**Implementation:**
```python
# Try YouTube first
try:
    transcript = fetch_youtube_transcript(video_id, use_proxy=True)
except IPBlockedError:
    # Fallback to Podcast Index
    podcast = search_podcast_index(podcast_name)
    mp3_url = podcast['episodes'][0]['enclosure_url']
    transcript = transcribe_with_whisper(mp3_url)
```

---

## Quick Fix for Testing

Since you're on a cloud provider, the fastest solution for testing is:

**Use Podcast Index instead** (already working!):
```bash
# This works right now
uv run python research/validate_podcastindex.py
```

**Or run YouTube test locally**:
```bash
# Download the repo to your laptop and run there
uv run python research/validate_youtube.py
```

---

## Updated Script Usage

The `validate_youtube.py` script now supports proxies:

```bash
# Test without proxy (may fail on cloud IPs)
uv run python research/validate_youtube.py

# Test with proxy (if configured in .env)
uv run python research/validate_youtube.py --use-proxy

# Test specific video with proxy
uv run python research/validate_youtube.py --video-id "9Uq_zig3LgI" --use-proxy
```

---

## Recommendation for PodAgent

**Go with Solution 4 (Hybrid):**

1. **For YouTube podcasts:** Try YouTube transcript API first
   - On local dev: Works without proxy
   - On production: Use proxy or fall back to Podcast Index

2. **For RSS podcasts:** Use Podcast Index directly
   - Already proven working
   - Direct MP3 access
   - Just needs STT processing

3. **Accept that YouTube may fail:**
   - Build fallback logic
   - Don't depend solely on YouTube
   - Podcast Index is more reliable for production

---

## Summary Table

| Solution | Cost | Complexity | Reliability | Best For |
|----------|------|------------|-------------|----------|
| **Proxy (Webshare)** | $5-10/mo | Low | High | Production servers |
| **Local machine** | Free | None | High | Development only |
| **YouTube Data API** | Free* | Medium | Medium | Official approach |
| **Hybrid approach** | Free | Medium | Very High | **PodAgent (Recommended)** |

*YouTube Data API has quota limits

---

## Resources

- **youtube-transcript-api proxy docs:** https://github.com/jdepoix/youtube-transcript-api#working-around-ip-bans-requestblocked-or-ipblocked-exception
- **Webshare proxy:** https://www.webshare.io/
- **YouTube Data API:** https://developers.google.com/youtube/v3/docs/captions
