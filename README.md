# PodAgent - Ingestion Source Validation

This directory contains validation scripts to test and compare different podcast ingestion sources for the PodAgent project.

## Prerequisites

Install `uv` (if not already installed):

```bash
# On macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# On Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Or via pip
pip install uv
```

## Quick Start with uv

### 1. Create Virtual Environment and Install Dependencies

```bash
# Navigate to research directory
cd research

# Create virtual environment and install dependencies (one command!)
uv sync

# Or to include dev dependencies
uv sync --extra dev
```

### 2. Set Up API Keys

#### YouTube (No API key needed!)
The `youtube-transcript-api` works without an API key by extracting existing captions.

#### Podcast Index (Free)
```bash
# Sign up for free API key at: https://api.podcastindex.org/signup
export PODCAST_INDEX_API_KEY="your_key_here"
export PODCAST_INDEX_API_SECRET="your_secret_here"
```

#### Spotify (Free)
```bash
# Create app at: https://developer.spotify.com/dashboard
export SPOTIFY_CLIENT_ID="your_client_id"
export SPOTIFY_CLIENT_SECRET="your_client_secret"
```

### 3. Run Validation Scripts

Using `uv run` (no need to activate virtual environment):

```bash
# Test YouTube Transcript Extraction
uv run python validate_youtube.py

# Test specific video
uv run python validate_youtube.py --video-id "9Uq_zig3LgI"

# Test Podcast Index
uv run python validate_podcastindex.py

# Search for specific podcast
uv run python validate_podcastindex.py --search "This American Life"

# Test Spotify API
uv run python validate_spotify.py

# Search for specific podcast
uv run python validate_spotify.py --search "Huberman Lab"

# Test Combined/Hybrid Approach
uv run python validate_combined.py --podcast "Huberman Lab"

# Test specific source only
uv run python validate_combined.py --podcast "Lex Fridman" --youtube-only
```

## uv Commands Reference

| Command | Description |
|---------|-------------|
| `uv sync` | Create venv and install dependencies from pyproject.toml |
| `uv sync --extra dev` | Install with dev dependencies |
| `uv run <command>` | Run command in the virtual environment |
| `uv add <package>` | Add a new dependency |
| `uv add --dev <package>` | Add a dev dependency |
| `uv remove <package>` | Remove a dependency |
| `uv lock` | Update the lock file |
| `uv tree` | Show dependency tree |

## Alternative: Traditional Virtual Environment

If you prefer the traditional approach:

```bash
# Create and activate virtual environment
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
uv pip install -r pyproject.toml --extra dev

# Run scripts
python validate_youtube.py
```

## Overview

PodAgent needs to ingest podcast content from multiple sources. These scripts validate three potential sources:

| Source | Library | Audio Access | Transcripts | Best For |
|--------|---------|--------------|-------------|----------|
| **YouTube** | `youtube-transcript-api` | ❌ No | ✅ Yes (captions) | YouTube-hosted podcasts |
| **Podcast Index** | `python-podcastindex` | ✅ Yes (MP3 URLs) | ⚠️ Sometimes | RSS-based podcasts |
| **Spotify** | `spotipy` | ❌ No (ToS) | ❌ No | Metadata only |

## Script Details

### validate_youtube.py

Tests transcript extraction from YouTube videos.

**Features:**
- Fetches transcripts with timestamps
- Detects auto-generated vs manual captions
- Lists available languages
- Measures extraction time

**Requirements:** None (no API key needed)

**Limitations:**
- Only works for videos with captions
- Age-restricted videos may fail
- YouTube may block cloud provider IPs (use proxy if needed)

**Example:**
```bash
uv run python validate_youtube.py
uv run python validate_youtube.py --video-id "9Uq_zig3LgI"
```

### validate_podcastindex.py

Tests Podcast Index API for podcast discovery.

**Features:**
- Search 4M+ podcasts
- Get RSS feed URLs
- Extract MP3 enclosure URLs
- Check for transcript URLs

**Requirements:** Free API key from podcastindex.org

**Output:** Metadata + direct MP3 URLs for audio download

**Example:**
```bash
uv run python validate_podcastindex.py
uv run python validate_podcastindex.py --search "This American Life"
uv run python validate_podcastindex.py --feed-id 522613
```

### validate_spotify.py

Tests Spotify Web API for podcast metadata.

**Features:**
- Search Spotify podcast catalog
- Get show and episode metadata
- Check for 30-second preview clips

**Requirements:** Free Spotify Developer account

**⚠️ Important:** Spotify API provides **metadata only**. Full audio access is prohibited by Terms of Service.

**Example:**
```bash
uv run python validate_spotify.py
uv run python validate_spotify.py --search "Huberman Lab"
```

### validate_combined.py

Tests the hybrid approach - finds the best source for a given podcast.

**Features:**
- Searches across all three sources
- Recommends optimal ingestion strategy
- Provides actionable next steps

**Example:**
```bash
uv run python validate_combined.py --podcast "Huberman Lab"
uv run python validate_combined.py --podcast "Lex Fridman" --youtube-only
uv run python validate_combined.py --podcast "This American Life" --full-test
```

**Example Output:**
```
🏆 RECOMMENDED SOURCE: YOUTUBE

Strategy: direct_transcript_extraction
✓ BEST - Use this source
```

## Ingestion Strategy Matrix

| Scenario | Recommended Source | Method | Complexity |
|----------|-------------------|--------|------------|
| Podcast on YouTube with captions | YouTube | Direct transcript extraction | Low |
| RSS podcast with transcript URL | Podcast Index | Fetch transcript from URL | Low |
| RSS podcast with MP3 only | Podcast Index | Download MP3 → STT (Whisper) | Medium |
| Spotify exclusive (no YouTube/RSS) | ❌ Not viable | N/A | N/A |

## API Key Obtention

### YouTube
**Status:** NOT NEEDED ✅

The `youtube-transcript-api` library works **without any API key**.

### Podcast Index (FREE)
**Website:** https://api.podcastindex.org/signup

1. Go to https://api.podcastindex.org/signup
2. Enter your email address
3. Check your email for API credentials
4. Set environment variables:
```bash
export PODCAST_INDEX_API_KEY="your_key_here"
export PODCAST_INDEX_API_SECRET="your_secret_here"
```

### Spotify (FREE)
**Website:** https://developer.spotify.com/dashboard

1. Log in with your Spotify account (free account works)
2. Click "Create App"
3. Fill in app details (any name/description works)
4. Add `http://localhost:8888/callback` as Redirect URI
5. Click "Settings" to view your credentials
6. Set environment variables:
```bash
export SPOTIFY_CLIENT_ID="your_client_id"
export SPOTIFY_CLIENT_SECRET="your_client_secret"
```

## Test Results Summary

After running all scripts, you'll have JSON files with validation results:

- `youtube_validation_results.json` - YouTube transcript extraction results
- `podcastindex_validation_results.json` - Podcast Index search results
- `spotify_validation_results.json` - Spotify API metadata results
- `combined_validation_results.json` - Hybrid recommendation

## Next Steps for PodAgent

Based on validation results, the recommended MVP approach:

1. **Phase 1 (YouTube-first):**
   - Use `youtube-transcript-api` for YouTube-hosted podcasts
   - Fast, no audio processing, includes timestamps
   - Cover ~60% of popular podcasts

2. **Phase 2 (RSS fallback):**
   - Use `python-podcastindex` for RSS-based podcasts
   - Download MP3 from enclosure URLs
   - Process with STT (OpenAI Whisper, AssemblyAI, or Deepgram)

3. **Phase 3 (Spotify integration):**
   - Use `spotipy` for podcast discovery
   - Link to Spotify for "Listen on Spotify" buttons
   - Do NOT attempt audio extraction (ToS violation)

## Troubleshooting

### uv: command not found
```bash
# Reinstall uv
curl -LsSf https://astral.sh/uv/install.sh | sh
# Then restart your terminal
```

### YouTube "Video unavailable" errors
- Video may be age-restricted
- Captions may not be enabled
- Try a different video ID

### Podcast Index "Authentication failed"
- Check `PODCAST_INDEX_API_KEY` and `PODCAST_INDEX_API_SECRET` are set
- Verify keys are correct at podcastindex.org

### Spotify "Invalid client"
- Check `SPOTIFY_CLIENT_ID` and `SPOTIFY_CLIENT_SECRET` are set
- Verify app is created at developer.spotify.com/dashboard

### All scripts fail
```bash
# Ensure dependencies are installed
uv sync

# Check uv is working
uv --version

# Verify Python version
uv run python --version
```

## Resources

- **uv documentation:** https://docs.astral.sh/uv/
- **YouTube Transcript API:** https://github.com/jdepoix/youtube-transcript-api
- **Podcast Index API:** https://podcastindex.org
- **Spotify Web API:** https://developer.spotify.com/documentation/web-api
- **Spotipy:** https://spotipy.readthedocs.io/

## License

These validation scripts are part of the PodAgent project.
