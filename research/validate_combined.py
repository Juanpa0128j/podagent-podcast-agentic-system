#!/usr/bin/env python3
"""
Script 4: Combined Ingestion Test (Hybrid Approach)
Tests finding a podcast across all three sources and determines the best ingestion path.

Usage:
    python validate_combined.py --podcast "Huberman Lab"
    python validate_combined.py --podcast "Lex Fridman" --youtube-only
    python validate_combined.py --podcast "This American Life" --full-test

The script will:
1. Search for the podcast across YouTube, Podcast Index, and Spotify
2. Determine the best ingestion strategy for each source
3. Recommend the optimal path for transcription
"""

import json
import os
import sys
import argparse
from typing import Dict, List, Optional, Tuple

# Import functions from other validation scripts
from validate_youtube import fetch_transcript as youtube_fetch_transcript
from validate_podcastindex import search_podcasts as pi_search_podcasts, get_episodes_by_feed_id as pi_get_episodes
from validate_spotify import search_podcasts as spotify_search_podcasts, get_show_episodes as spotify_get_episodes


# Known YouTube podcast channels (for testing)
KNOWN_YOUTUBE_PODCASTS = {
    "huberman lab": "UC2D2CMWXMOVWx7giW1n3LIg",  # Huberman Lab
    "lex fridman": "UCSHZKyawb77ixDdsGog4iWA",   # Lex Fridman
    "joe rogan": "UCzQUP1qoWDoEbmsQxvdjxgQ",     # PowerfulJRE
    "diary of a ceo": "UCGq-a6pETI0ProAsbkMXqKw", # Steven Bartlett
}


def search_youtube_podcast(podcast_name: str, max_results: int = 3) -> Dict:
    """
    Search for podcast on YouTube by looking for channel + recent videos.
    Note: youtube-transcript-api doesn't have search, so we check known channels.
    """
    # Normalize podcast name
    name_lower = podcast_name.lower()
    
    # Check if it's a known podcast
    channel_id = None
    for key, cid in KNOWN_YOUTUBE_PODCASTS.items():
        if key in name_lower or name_lower in key:
            channel_id = cid
            break
    
    # For demonstration, we'll test a known video ID
    # In production, you'd use YouTube Data API to search
    test_video_ids = {
        "huberman lab": "9Uq_zig3LgI",
        "lex fridman": "gP5gl3Nf0C8",
        "joe rogan": "d-ZsB1poP4w",
        "diary of a ceo": "Z2C9jzbcf0Q"
    }
    
    results = {
        "success": False,
        "source": "youtube",
        "podcast_name": podcast_name,
        "found": False,
        "ingestion_strategy": None,
        "details": {}
    }
    
    # Check if we have a test video for this podcast
    for key, video_id in test_video_ids.items():
        if key in name_lower:
            print(f"  Testing with known YouTube video: {video_id}")
            transcript_result = youtube_fetch_transcript(video_id)
            
            results["found"] = transcript_result["success"]
            results["success"] = True
            results["details"] = {
                "video_id": video_id,
                "has_transcript": transcript_result.get("success", False),
                "language": transcript_result.get("language"),
                "is_generated": transcript_result.get("is_generated"),
                "snippet_count": transcript_result.get("snippet_count")
            }
            
            if transcript_result["success"]:
                results["ingestion_strategy"] = {
                    "method": "direct_transcript_extraction",
                    "tool": "youtube-transcript-api",
                    "output": "transcript with timestamps",
                    "speed": "fast (no audio processing needed)",
                    "recommendation": "✓ BEST - Use this source"
                }
            else:
                results["ingestion_strategy"] = {
                    "method": "not_available",
                    "error": transcript_result.get("error_message"),
                    "recommendation": "✗ No YouTube transcript available"
                }
            break
    else:
        results["details"]["message"] = "No known YouTube video for testing. Use YouTube Data API for full search."
        results["ingestion_strategy"] = {
            "method": "requires_youtube_data_api",
            "recommendation": "Use YouTube Data API v3 to search for videos, then extract transcripts"
        }
    
    return results


def search_podcast_index(podcast_name: str) -> Dict:
    """Search for podcast on Podcast Index."""
    results = {
        "success": False,
        "source": "podcast_index",
        "podcast_name": podcast_name,
        "found": False,
        "ingestion_strategy": None,
        "details": {}
    }
    
    # Check if API keys are available
    if not os.environ.get("PODCAST_INDEX_API_KEY"):
        results["details"]["error"] = "PODCAST_INDEX_API_KEY not set"
        results["ingestion_strategy"] = {
            "method": "api_key_required",
            "recommendation": "Set PODCAST_INDEX_API_KEY to use this source"
        }
        return results
    
    try:
        search_result = pi_search_podcasts(podcast_name, limit=3)
        
        if search_result["success"] and search_result.get("feeds"):
            feed = search_result["feeds"][0]
            results["found"] = True
            results["success"] = True
            
            # Get episodes to check for audio URLs
            episodes_result = pi_get_episodes(feed["id"], limit=1)
            has_audio = False
            audio_url = None
            has_transcript_url = False
            
            if episodes_result.get("success") and episodes_result.get("episodes"):
                ep = episodes_result["episodes"][0]
                audio_url = ep.get("enclosure_url")
                has_audio = audio_url is not None
                has_transcript_url = ep.get("transcript_url") is not None
            
            results["details"] = {
                "feed_id": feed["id"],
                "title": feed["title"],
                "episode_count": feed.get("episode_count"),
                "has_audio_url": has_audio,
                "sample_audio_url": audio_url[:80] + "..." if audio_url and len(audio_url) > 80 else audio_url,
                "has_transcript_url": has_transcript_url
            }
            
            if has_audio:
                if has_transcript_url:
                    results["ingestion_strategy"] = {
                        "method": "transcript_url_available",
                        "tool": "Podcast Index API",
                        "output": "pre-made transcript",
                        "speed": "fastest",
                        "recommendation": "✓ BEST - Transcript already available"
                    }
                else:
                    results["ingestion_strategy"] = {
                        "method": "audio_download_then_stt",
                        "steps": [
                            "1. Download MP3 from enclosureUrl",
                            "2. Process with STT (Whisper/AssemblyAI/Deepgram)"
                        ],
                        "output": "generated transcript",
                        "speed": "slow (audio processing)",
                        "cost": "STT API costs apply",
                        "recommendation": "✓ GOOD - Viable but requires STT processing"
                    }
            else:
                results["ingestion_strategy"] = {
                    "method": "audio_not_available",
                    "recommendation": "✗ Audio URL not available in feed"
                }
        else:
            results["details"]["error"] = search_result.get("error_message", "No results found")
            results["ingestion_strategy"] = {
                "method": "not_found",
                "recommendation": "✗ Podcast not found in Podcast Index"
            }
    
    except Exception as e:
        results["details"]["error"] = str(e)
        results["ingestion_strategy"] = {
            "method": "error",
            "recommendation": f"✗ Error: {str(e)}"
        }
    
    return results


def search_spotify(podcast_name: str) -> Dict:
    """Search for podcast on Spotify."""
    results = {
        "success": False,
        "source": "spotify",
        "podcast_name": podcast_name,
        "found": False,
        "ingestion_strategy": None,
        "details": {}
    }
    
    # Check if API credentials are available
    if not os.environ.get("SPOTIFY_CLIENT_ID"):
        results["details"]["error"] = "SPOTIFY_CLIENT_ID not set"
        results["ingestion_strategy"] = {
            "method": "api_credentials_required",
            "recommendation": "Set SPOTIFY_CLIENT_ID to use this source"
        }
        return results
    
    try:
        search_result = spotify_search_podcasts(podcast_name, limit=3)
        
        if search_result["success"] and search_result.get("shows"):
            show = search_result["shows"][0]
            results["found"] = True
            results["success"] = True
            
            # Get episodes to check for preview URLs
            episodes_result = spotify_get_episodes(show["id"], limit=1)
            has_preview = False
            
            if episodes_result.get("success") and episodes_result.get("episodes"):
                ep = episodes_result["episodes"][0]
                has_preview = ep.get("has_preview", False)
            
            results["details"] = {
                "show_id": show["id"],
                "name": show["name"],
                "publisher": show["publisher"],
                "episode_count": show.get("episode_count"),
                "is_externally_hosted": show.get("is_externally_hosted"),
                "has_30s_preview": has_preview,
                "external_url": show.get("external_url")
            }
            
            # Spotify doesn't allow full audio access per ToS
            results["ingestion_strategy"] = {
                "method": "metadata_only",
                "note": "Spotify ToS prohibits downloading/stream ripping",
                "available": [
                    "Podcast metadata (title, description, publisher)",
                    "Episode list with release dates",
                    "30-second preview clips (not full audio)",
                    "External Spotify URL for linking"
                ],
                "recommendation": "✗ NOT VIABLE for transcription - Use for metadata/linking only"
            }
        else:
            results["details"]["error"] = search_result.get("error_message", "No results found")
            results["ingestion_strategy"] = {
                "method": "not_found",
                "recommendation": "✗ Podcast not found on Spotify"
            }
    
    except Exception as e:
        results["details"]["error"] = str(e)
        results["ingestion_strategy"] = {
            "method": "error",
            "recommendation": f"✗ Error: {str(e)}"
        }
    
    return results


def recommend_best_source(results: List[Dict]) -> Dict:
    """Analyze results and recommend the best ingestion source."""
    print("\n" + "=" * 60)
    print("INGESTION STRATEGY RECOMMENDATION")
    print("=" * 60)
    
    # Priority order: YouTube (direct) > Podcast Index (with transcript) > Podcast Index (STT) > Spotify
    recommendations = []
    
    for r in results:
        strategy = r.get("ingestion_strategy", {})
        if r.get("found"):
            recommendations.append({
                "source": r["source"],
                "priority": strategy.get("recommendation", "").startswith("✓ BEST"),
                "viable": strategy.get("recommendation", "").startswith("✓"),
                "strategy": strategy
            })
    
    # Sort by priority
    best = None
    for r in recommendations:
        if r["priority"]:
            best = r
            break
    
    if not best:
        for r in recommendations:
            if r["viable"]:
                best = r
                break
    
    if best:
        print(f"\n🏆 RECOMMENDED SOURCE: {best['source'].upper()}")
        print(f"\nStrategy: {best['strategy'].get('method', 'N/A')}")
        if 'steps' in best['strategy']:
            print("\nSteps:")
            for step in best['strategy']['steps']:
                print(f"  {step}")
        print(f"\n{best['strategy'].get('recommendation', '')}")
    else:
        print("\n⚠️  No viable source found for transcription")
        print("\nRecommendations:")
        print("  1. Check YouTube for video versions of the podcast")
        print("  2. Look for official RSS feeds from the podcast website")
        print("  3. Consider if this is a Spotify-exclusive that may not have transcripts available")
    
    return best


def main():
    parser = argparse.ArgumentParser(
        description="Combined ingestion test - find best source for podcast transcription"
    )
    parser.add_argument("--podcast", "-p", required=True, help="Podcast name to search for")
    parser.add_argument("--youtube-only", action="store_true", help="Test YouTube only")
    parser.add_argument("--podcast-index-only", action="store_true", help="Test Podcast Index only")
    parser.add_argument("--spotify-only", action="store_true", help="Test Spotify only")
    parser.add_argument("--full-test", action="store_true", help="Test all available sources")
    parser.add_argument("--output", "-o", default="combined_validation_results.json",
                        help="Output JSON file (default: combined_validation_results.json)")
    args = parser.parse_args()
    
    print("=" * 60)
    print("PodAgent Combined Ingestion Test")
    print("=" * 60)
    print(f"\nSearching for: '{args.podcast}'")
    print("\nThis test will check multiple sources and recommend the best")
    print("ingestion strategy for transcription.")
    print("=" * 60)
    
    results = {
        "podcast_name": args.podcast,
        "test_timestamp": None,  # Would add timestamp here
        "sources_tested": [],
        "recommendation": None
    }
    
    all_results = []
    
    # Determine which sources to test
    test_youtube = args.youtube_only or args.full_test or not (args.podcast_index_only or args.spotify_only)
    test_podcast_index = args.podcast_index_only or args.full_test or not (args.youtube_only or args.spotify_only)
    test_spotify = args.spotify_only or args.full_test or not (args.youtube_only or args.podcast_index_only)
    
    # Test YouTube
    if test_youtube:
        print("\n" + "-" * 60)
        print("1. Testing YouTube (youtube-transcript-api)")
        print("-" * 60)
        yt_result = search_youtube_podcast(args.podcast)
        all_results.append(yt_result)
        results["sources_tested"].append("youtube")
        
        print(f"   Found: {yt_result['found']}")
        if yt_result['found']:
            print(f"   Has transcript: {yt_result['details'].get('has_transcript')}")
            print(f"   Strategy: {yt_result['ingestion_strategy'].get('method')}")
        print(f"   {yt_result['ingestion_strategy'].get('recommendation', '')}")
    
    # Test Podcast Index
    if test_podcast_index:
        print("\n" + "-" * 60)
        print("2. Testing Podcast Index (python-podcastindex)")
        print("-" * 60)
        pi_result = search_podcast_index(args.podcast)
        all_results.append(pi_result)
        results["sources_tested"].append("podcast_index")
        
        print(f"   Found: {pi_result['found']}")
        if pi_result['found']:
            print(f"   Title: {pi_result['details'].get('title')}")
            print(f"   Has audio URL: {pi_result['details'].get('has_audio_url')}")
            print(f"   Has transcript URL: {pi_result['details'].get('has_transcript_url')}")
        print(f"   {pi_result['ingestion_strategy'].get('recommendation', '')}")
    
    # Test Spotify
    if test_spotify:
        print("\n" + "-" * 60)
        print("3. Testing Spotify (spotipy)")
        print("-" * 60)
        sp_result = search_spotify(args.podcast)
        all_results.append(sp_result)
        results["sources_tested"].append("spotify")
        
        print(f"   Found: {sp_result['found']}")
        if sp_result['found']:
            print(f"   Name: {sp_result['details'].get('name')}")
            print(f"   Episodes: {sp_result['details'].get('episode_count')}")
        print(f"   {sp_result['ingestion_strategy'].get('recommendation', '')}")
    
    # Get recommendation
    best = recommend_best_source(all_results)
    
    results["results"] = all_results
    results["recommendation"] = best["source"] if best else None
    
    # Save results
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\n{'=' * 60}")
    print(f"Results saved to: {args.output}")
    print("=" * 60)


if __name__ == "__main__":
    main()
