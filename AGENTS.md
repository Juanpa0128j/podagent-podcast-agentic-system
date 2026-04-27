# AGENTS.md

> **Purpose:** This file contains essential context and instructions for AI agents working on the PodAgent project. It complements the README by providing agent-specific guidance.

---

## Project Overview

**PodAgent** is an agentic system for interactive podcast intelligence. It enables users to:
- Ask questions about podcast episodes using natural language
- Search across episodes and podcast series
- Generate summaries and extract highlights
- Explore topics without listening to entire episodes

**Current Phase:** Research & Validation

We're validating three potential podcast ingestion sources before building the full system.

---

## Repository Structure

```
podagent/
├── .env                                 # Local environment variables (DO NOT COMMIT)
├── .env.example                         # Template for env variables
├── .gitignore
├── AGENTS.md                            # This file - agent guidance
├── README.md                            # Project overview
├── pyproject.toml                       # uv project configuration
├── docs/
│   └── podagent-srs.docx.md             # Full Software Requirements Specification
└── research/                            # VALIDATION SCRIPTS (current focus)
    ├── README.md                        # Research-specific documentation
    ├── validate_youtube.py              # Script 1: YouTube transcript API
    ├── validate_podcastindex.py         # Script 2: Podcast Index API
    ├── validate_spotify.py              # Script 3: Spotify Web API
    └── validate_combined.py             # Script 4: Hybrid approach
```

---

## Technology Stack

### Package Management
- **uv** - Modern Python package manager (required)
  - Install: `curl -LsSf https://astral.sh/uv/install.sh | sh`
  - Key commands: `uv sync`, `uv run`, `uv add`

### Python Libraries
| Library | Purpose | API Key? |
|---------|---------|----------|
| `youtube-transcript-api` | Extract YouTube captions | ❌ None needed |
| `python-podcastindex` | Search RSS podcasts | ✅ Free key required |
| `spotipy` | Spotify metadata | ✅ Free key required |

---

## Environment Variables

Copy `.env.example` to `.env` and fill in your API keys:

```bash
cp .env.example .env
# Edit .env with your keys
```

### Required API Keys

#### 1. Podcast Index (FREE)
- **Get keys:** https://api.podcastindex.org/signup
- **Variables:** `PODCAST_INDEX_API_KEY`, `PODCAST_INDEX_API_SECRET`
- **Cost:** Free, no credit card

#### 2. Spotify (FREE)
- **Get keys:** https://developer.spotify.com/dashboard
- **Variables:** `SPOTIFY_CLIENT_ID`, `SPOTIFY_CLIENT_SECRET`
- **Cost:** Free, requires Spotify account

#### 3. YouTube
- **Status:** NO KEY NEEDED ✅
- The `youtube-transcript-api` works without authentication

---

## Running Validation Scripts

### Setup (One-time)
```bash
cd research
uv sync                    # Creates venv + installs deps
```

### Run Scripts
```bash
# YouTube (no API key needed)
uv run python validate_youtube.py

# Podcast Index (requires API key)
uv run python validate_podcastindex.py

# Spotify (requires API key)
uv run python validate_spotify.py

# Combined/Hybrid test
uv run python validate_combined.py --podcast "Huberman Lab"
```

### With Arguments
```bash
# Test specific video
uv run python validate_youtube.py --video-id "9Uq_zig3LgI"

# Search specific podcast
uv run python validate_podcastindex.py --search "This American Life"

# Full test across all sources
uv run python validate_combined.py --podcast "Lex Fridman" --full-test
```

---

## Key Findings

### YouTube (`youtube-transcript-api`)
- ✅ **BEST for transcripts** - Direct caption extraction
- ✅ Includes timestamps
- ✅ No API key needed
- ⚠️ **BLOCKED from cloud IPs** - YouTube blocks AWS/GCP/Azure
- ⚠️ Free proxies don't work reliably (rate limited)
- ✅ Works from local/residential IPs
- ✅ Works from cloud with paid residential proxy (~$5-20/mo)
- ⚠️ May fail for age-restricted videos

### Podcast Index (`python-podcastindex`)
- ✅ **BEST for production** - Works everywhere, no blocking
- ✅ **BEST for audio access** - Returns MP3 URLs
- ✅ 4M+ podcasts indexed
- ✅ Free API (KEY + SECRET required)
- ⚠️ Requires STT for transcripts (Whisper, etc.)
- ⚠️ Not all podcasts have transcript URLs

### Spotify (`spotipy`)
- ⚠️ **Metadata ONLY** - No audio per ToS
- ✅ Good for discovery
- ✅ User's saved shows sync
- ❌ Cannot download/stream audio
- ❌ No transcript access

### Recommended Strategy (Updated)
1. **Podcast Index FIRST** (Primary) - Reliable, no IP blocking, direct MP3 access
2. **YouTube fallback** - Only for local dev or with paid proxy
3. **Spotify** - Metadata & linking only

### Production Architecture
```
User Request → Podcast Index API → MP3 URL → STT (Whisper) → Transcript
                    ↓ (fallback)
            YouTube API (local dev only or with proxy)
```

See full research report: `docs/RESEARCH_SUMMARY.md`

---

## Development Guidelines

### Code Style
- Python 3.10+ required
- Type hints encouraged
- Follow existing patterns in validation scripts
- Use `uv run` for all Python commands

### Testing New Sources
When adding a new ingestion source:
1. Create `validate_<source>.py` script
2. Follow pattern: search → get metadata → determine strategy
3. Add to `validate_combined.py` hybrid logic
4. Update this AGENTS.md

### Adding Dependencies
```bash
uv add new-package-name        # Production dep
uv add --dev new-package-name  # Dev dep
```

---

## Common Issues

### uv not found
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
# Restart terminal
```

### API key errors
- Check `.env` file exists and is filled in
- Verify keys with `echo $PODCAST_INDEX_API_KEY`
- Ensure keys are valid (not expired)

### Import errors
```bash
# Re-sync dependencies
uv sync
```

---

## Resources

- **uv docs:** https://docs.astral.sh/uv/
- **SRS Document:** `docs/podagent-srs.docx.md`
- **YouTube API:** https://github.com/jdepoix/youtube-transcript-api
- **Podcast Index:** https://podcastindex.org
- **Spotify API:** https://developer.spotify.com/documentation/web-api

---

## Contact

For questions about the validation scripts or PodAgent architecture, refer to the SRS document or existing validation scripts for examples.

---

*Last updated: April 2026*
