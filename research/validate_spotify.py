#!/usr/bin/env python3
"""
Script 3: Spotify API Validation
Tests spotipy for Spotify podcast metadata access.

Prerequisites:
    - Create app at: https://developer.spotify.com/dashboard
    - Set environment variables:
        export SPOTIFY_CLIENT_ID="your_client_id"
        export SPOTIFY_CLIENT_SECRET="your_client_secret"

Usage:
    python validate_spotify.py
    python validate_spotify.py --search "podcast name"
    python validate_spotify.py --show-id <SHOW_ID>
"""

import json
import os
import argparse
from typing import List, Dict, Optional


def get_spotify_client():
    """Initialize Spotify API client."""
    import spotipy
    from spotipy.oauth2 import SpotifyClientCredentials
    
    client_id = os.environ.get("SPOTIFY_CLIENT_ID")
    client_secret = os.environ.get("SPOTIFY_CLIENT_SECRET")
    
    if not client_id or not client_secret:
        raise ValueError(
            "SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET must be set. "
            "Create a free app at https://developer.spotify.com/dashboard"
        )
    
    auth_manager = SpotifyClientCredentials(
        client_id=client_id,
        client_secret=client_secret
    )
    
    return spotipy.Spotify(auth_manager=auth_manager)


def search_podcasts(query: str, limit: int = 5) -> dict:
    """Search for podcasts (shows) on Spotify."""
    try:
        sp = get_spotify_client()
        
        # Search for shows (podcasts)
        results = sp.search(q=query, type='show', limit=limit)
        
        shows = []
        for show in results.get('shows', {}).get('items', []):
            if show:  # Sometimes null items appear
                shows.append({
                    "id": show.get("id"),
                    "name": show.get("name"),
                    "description": show.get("description", "")[:200] + "..." if len(show.get("description", "")) > 200 else show.get("description"),
                    "publisher": show.get("publisher"),
                    "explicit": show.get("explicit"),
                    "episode_count": show.get("total_episodes"),
                    "languages": show.get("languages", []),
                    "external_url": show.get("external_urls", {}).get("spotify"),
                    "images": show.get("images", []),
                    "is_externally_hosted": show.get("is_externally_hosted")
                })
        
        return {
            "success": True,
            "query": query,
            "total_results": results.get('shows', {}).get('total'),
            "shows": shows
        }
    
    except Exception as e:
        return {
            "success": False,
            "query": query,
            "error": str(type(e).__name__),
            "error_message": str(e)
        }


def get_show_details(show_id: str) -> dict:
    """Get detailed information about a podcast show."""
    try:
        sp = get_spotify_client()
        show = sp.show(show_id)
        
        return {
            "success": True,
            "show_id": show_id,
            "name": show.get("name"),
            "description": show.get("description", "")[:300] + "..." if len(show.get("description", "")) > 300 else show.get("description"),
            "publisher": show.get("publisher"),
            "explicit": show.get("explicit"),
            "total_episodes": show.get("total_episodes"),
            "languages": show.get("languages", []),
            "media_type": show.get("media_type"),
            "external_url": show.get("external_urls", {}).get("spotify"),
            "images": show.get("images", []),
            "is_externally_hosted": show.get("is_externally_hosted"),
            "copyrights": show.get("copyrights", [])
        }
    
    except Exception as e:
        return {
            "success": False,
            "show_id": show_id,
            "error": str(e)
        }


def get_show_episodes(show_id: str, limit: int = 5) -> dict:
    """Get episodes for a podcast show."""
    try:
        sp = get_spotify_client()
        results = sp.show_episodes(show_id, limit=limit)
        
        episodes = []
        for episode in results.get('items', []):
            if episode:
                # Get preview URL (30-second clip, if available)
                preview_url = episode.get('audio_preview_url')
                
                episodes.append({
                    "id": episode.get("id"),
                    "name": episode.get("name"),
                    "description": episode.get("description", "")[:200] + "..." if len(episode.get("description", "")) > 200 else episode.get("description"),
                    "duration_ms": episode.get("duration_ms"),
                    "duration_formatted": format_duration_ms(episode.get("duration_ms")),
                    "release_date": episode.get("release_date"),
                    "explicit": episode.get("explicit"),
                    "external_url": episode.get("external_urls", {}).get("spotify"),
                    "images": episode.get("images", []),
                    "is_externally_hosted": episode.get("is_externally_hosted"),
                    "is_playable": episode.get("is_playable"),
                    "languages": episode.get("languages", []),
                    "audio_preview_url": preview_url,
                    "has_preview": preview_url is not None
                })
        
        return {
            "success": True,
            "show_id": show_id,
            "total_episodes_returned": len(episodes),
            "episodes": episodes
        }
    
    except Exception as e:
        return {
            "success": False,
            "show_id": show_id,
            "error": str(e)
        }


def get_episode_details(episode_id: str) -> dict:
    """Get detailed information about a specific episode."""
    try:
        sp = get_spotify_client()
        episode = sp.episode(episode_id)
        
        return {
            "success": True,
            "episode_id": episode_id,
            "name": episode.get("name"),
            "description": episode.get("description", "")[:300] + "..." if len(episode.get("description", "")) > 300 else episode.get("description"),
            "duration_ms": episode.get("duration_ms"),
            "duration_formatted": format_duration_ms(episode.get("duration_ms")),
            "release_date": episode.get("release_date"),
            "explicit": episode.get("explicit"),
            "external_url": episode.get("external_urls", {}).get("spotify"),
            "audio_preview_url": episode.get("audio_preview_url"),
            "has_preview": episode.get("audio_preview_url") is not None,
            "is_externally_hosted": episode.get("is_externally_hosted"),
            "is_playable": episode.get("is_playable"),
            "languages": episode.get("languages", []),
            "show_name": episode.get("show", {}).get("name"),
            "show_id": episode.get("show", {}).get("id")
        }
    
    except Exception as e:
        return {
            "success": False,
            "episode_id": episode_id,
            "error": str(e)
        }


def format_duration_ms(ms: Optional[int]) -> str:
    """Format milliseconds into HH:MM:SS."""
    if not ms:
        return "N/A"
    seconds = ms // 1000
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    if hours > 0:
        return f"{hours}:{minutes:02d}:{secs:02d}"
    return f"{minutes}:{secs:02d}"


def main():
    parser = argparse.ArgumentParser(description="Validate Spotify Web API for Podcasts")
    parser.add_argument("--search", "-s", help="Search query for podcasts")
    parser.add_argument("--show-id", help="Get podcast by Spotify show ID")
    parser.add_argument("--episode-id", "-e", help="Get episode by Spotify episode ID")
    parser.add_argument("--output", "-o", default="spotify_validation_results.json",
                        help="Output JSON file (default: spotify_validation_results.json)")
    args = parser.parse_args()
    
    print("=" * 60)
    print("Spotify Web API Validation (Podcasts)")
    print("=" * 60)
    print("\n⚠️  IMPORTANT: Spotify API provides METADATA ONLY")
    print("   Full audio access is NOT available per Terms of Service")
    print("   30-second preview clips may be available for some episodes")
    print("=" * 60)
    
    # Check for API credentials
    if not os.environ.get("SPOTIFY_CLIENT_ID"):
        print("\n❌ ERROR: SPOTIFY_CLIENT_ID not set")
        print("Create a free app at: https://developer.spotify.com/dashboard")
        print("\nThen set environment variables:")
        print("  export SPOTIFY_CLIENT_ID='your_client_id'")
        print("  export SPOTIFY_CLIENT_SECRET='your_client_secret'")
        return
    
    results = {
        "test_type": "spotify_web_api",
        "library": "spotipy",
        "note": "Spotify API provides metadata only - no full audio access",
        "tests": []
    }
    
    if args.search:
        # Search mode
        print(f"\nSearching for: '{args.search}'")
        search_result = search_podcasts(args.search)
        print(json.dumps(search_result, indent=2))
        results["tests"].append({"type": "search", "result": search_result})
        
        # If search successful, get episodes for first result
        if search_result.get("success") and search_result.get("shows"):
            first_show = search_result["shows"][0]
            show_id = first_show["id"]
            print(f"\nGetting episodes for '{first_show['name']}' (ID: {show_id})...")
            episodes_result = get_show_episodes(show_id)
            print(json.dumps(episodes_result, indent=2))
            results["tests"].append({"type": "episodes", "result": episodes_result})
    
    elif args.show_id:
        # Get specific show
        print(f"\nGetting show with ID: {args.show_id}")
        show_result = get_show_details(args.show_id)
        print(json.dumps(show_result, indent=2))
        results["tests"].append({"type": "show", "result": show_result})
        
        # Get episodes
        print(f"\nGetting episodes...")
        episodes_result = get_show_episodes(args.show_id)
        print(json.dumps(episodes_result, indent=2))
        results["tests"].append({"type": "episodes", "result": episodes_result})
    
    elif args.episode_id:
        # Get specific episode
        print(f"\nGetting episode ID: {args.episode_id}")
        episode_result = get_episode_details(args.episode_id)
        print(json.dumps(episode_result, indent=2))
        results["tests"].append({"type": "episode", "result": episode_result})
    
    else:
        # Default test mode
        test_queries = [
            "Huberman Lab",
            "Lex Fridman Podcast",
            "The Joe Rogan Experience"
        ]
        
        for query in test_queries:
            print(f"\n{'-' * 60}")
            print(f"Search Query: {query}")
            print("-" * 60)
            
            # Search
            search_result = search_podcasts(query, limit=3)
            
            if search_result["success"]:
                print(f"✓ Found {search_result['total_results']} result(s)")
                
                if search_result["shows"]:
                    # Show first result
                    show = search_result["shows"][0]
                    print(f"\n  Top result:")
                    print(f"    Name: {show['name']}")
                    print(f"    Publisher: {show['publisher']}")
                    print(f"    Episodes: {show.get('episode_count', 'N/A')}")
                    print(f"    Languages: {', '.join(show.get('languages', []))}")
                    print(f"    Externally Hosted: {show.get('is_externally_hosted')}")
                    
                    # Get episodes
                    print(f"\n  Fetching latest episodes...")
                    episodes_result = get_show_episodes(show["id"], limit=3)
                    
                    if episodes_result["success"]:
                        print(f"  ✓ Retrieved {episodes_result['total_episodes_returned']} episode(s)")
                        
                        previews_available = sum(1 for ep in episodes_result["episodes"] if ep['has_preview'])
                        print(f"  ℹ️  {previews_available}/{len(episodes_result['episodes'])} episodes have 30s preview clips")
                        
                        for i, ep in enumerate(episodes_result["episodes"][:3], 1):
                            print(f"\n    [{i}] {ep['name']}")
                            print(f"        Released: {ep['release_date']}")
                            print(f"        Duration: {ep['duration_formatted']}")
                            print(f"        Preview: {'✓ Available' if ep['has_preview'] else '✗ Not available'}")
                            print(f"        External URL: {ep['external_url']}")
                    else:
                        print(f"  ✗ Failed to get episodes: {episodes_result.get('error')}")
            else:
                print(f"✗ Search failed: {search_result.get('error_message')}")
            
            results["tests"].append({
                "query": query,
                "search": search_result,
                "episodes": episodes_result if search_result.get("success") and search_result.get("shows") else None
            })
    
    # Save results
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\n{'=' * 60}")
    print(f"Results saved to: {args.output}")
    print("=" * 60)
    
    # Summary
    successful = sum(1 for t in results["tests"] if t.get("search", {}).get("success"))
    total = len([t for t in results["tests"] if "search" in t])
    print(f"\nSummary: {successful}/{total} searches successful")
    print("\n⚠️  Remember: Spotify API provides metadata only")
    print("   For audio/transcripts, use YouTube or Podcast Index (RSS) sources")


if __name__ == "__main__":
    main()
