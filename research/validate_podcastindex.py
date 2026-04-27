#!/usr/bin/env python3
"""
Script 2: Podcast Index Validation
Tests python-podcastindex for RSS-based podcast discovery and metadata.

Prerequisites:
    - Get free API key at: https://api.podcastindex.org/signup
    - Set environment variables:
        export PODCAST_INDEX_API_KEY="your_key"
        export PODCAST_INDEX_API_SECRET="your_secret"

Usage:
    python validate_podcastindex.py
    python validate_podcastindex.py --search "podcast name"
"""

import json
import os
import argparse
from typing import Optional


def get_podcast_index():
    """Initialize Podcast Index API client."""
    import podcastindex
    
    api_key = os.environ.get("PODCAST_INDEX_API_KEY")
    api_secret = os.environ.get("PODCAST_INDEX_API_SECRET")
    
    if not api_key or not api_secret:
        raise ValueError(
            "PODCAST_INDEX_API_KEY and PODCAST_INDEX_API_SECRET must be set. "
            "Get free API keys at https://api.podcastindex.org/signup"
        )
    
    config = {
        "api_key": api_key,
        "api_secret": api_secret
    }
    
    return podcastindex.init(config)


def search_podcasts(query: str, limit: int = 5) -> dict:
    """Search for podcasts by name."""
    try:
        index = get_podcast_index()
        result = index.search(query)
        
        feeds = []
        for feed in result.get("feeds", [])[:limit]:
            feeds.append({
                "id": feed.get("id"),
                "title": feed.get("title"),
                "author": feed.get("author"),
                "description": feed.get("description", "")[:200] + "..." if len(feed.get("description", "")) > 200 else feed.get("description"),
                "url": feed.get("url"),
                "link": feed.get("link"),
                "image": feed.get("image"),
                "episode_count": feed.get("episodeCount"),
                "categories": list(feed.get("categories", {}).values()) if feed.get("categories") else [],
                "language": feed.get("language"),
                "newest_item_timestamp": feed.get("newestItemPublishTime")
            })
        
        return {
            "success": True,
            "query": query,
            "total_results": result.get("count"),
            "feeds": feeds
        }
    
    except Exception as e:
        return {
            "success": False,
            "query": query,
            "error": str(type(e).__name__),
            "error_message": str(e)
        }


def get_podcast_by_feed_id(feed_id: int) -> dict:
    """Get podcast details by feed ID."""
    try:
        index = get_podcast_index()
        result = index.podcastByFeedId(feed_id)
        
        feed = result.get("feed", {})
        return {
            "success": True,
            "feed_id": feed_id,
            "title": feed.get("title"),
            "description": feed.get("description", "")[:300] + "..." if len(feed.get("description", "")) > 300 else feed.get("description"),
            "author": feed.get("author"),
            "url": feed.get("url"),
            "link": feed.get("link"),
            "image": feed.get("image"),
            "language": feed.get("language"),
            "episode_count": feed.get("episodeCount"),
            "categories": list(feed.get("categories", {}).values()) if feed.get("categories") else []
        }
    
    except Exception as e:
        return {
            "success": False,
            "feed_id": feed_id,
            "error": str(e)
        }


def get_episodes_by_feed_id(feed_id: int, limit: int = 5) -> dict:
    """Get episodes for a podcast feed."""
    try:
        index = get_podcast_index()
        result = index.episodesByFeedId(feed_id, max_results=limit)
        
        episodes = []
        for episode in result.get("items", [])[:limit]:
            episodes.append({
                "id": episode.get("id"),
                "title": episode.get("title"),
                "description": episode.get("description", "")[:200] + "..." if len(episode.get("description", "")) > 200 else episode.get("description"),
                "date_published": episode.get("datePublishedPretty"),
                "duration_seconds": episode.get("duration"),
                "duration_formatted": format_duration(episode.get("duration")),
                "enclosure_url": episode.get("enclosureUrl"),
                "explicit": episode.get("explicit"),
                "episode_number": episode.get("episode"),
                "season": episode.get("season"),
                "transcript_url": episode.get("transcriptUrl"),
                "image": episode.get("image") or episode.get("feedImage")
            })
        
        return {
            "success": True,
            "feed_id": feed_id,
            "total_episodes": result.get("count"),
            "episodes": episodes
        }
    
    except Exception as e:
        return {
            "success": False,
            "feed_id": feed_id,
            "error": str(e)
        }


def get_episode_by_id(episode_id: int) -> dict:
    """Get specific episode details."""
    try:
        index = get_podcast_index()
        result = index.episodeById(episode_id)
        
        episode = result.get("episode", {})
        return {
            "success": True,
            "episode_id": episode_id,
            "title": episode.get("title"),
            "description": episode.get("description", "")[:300] + "..." if len(episode.get("description", "")) > 300 else episode.get("description"),
            "date_published": episode.get("datePublishedPretty"),
            "duration_seconds": episode.get("duration"),
            "enclosure_url": episode.get("enclosureUrl"),
            "transcript_url": episode.get("transcriptUrl"),
            "feed_title": episode.get("feedTitle"),
            "feed_id": episode.get("feedId")
        }
    
    except Exception as e:
        return {
            "success": False,
            "episode_id": episode_id,
            "error": str(e)
        }


def format_duration(seconds: Optional[int]) -> str:
    """Format seconds into HH:MM:SS."""
    if not seconds:
        return "N/A"
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    if hours > 0:
        return f"{hours}:{minutes:02d}:{secs:02d}"
    return f"{minutes}:{secs:02d}"


def main():
    parser = argparse.ArgumentParser(description="Validate Podcast Index API")
    parser.add_argument("--search", "-s", help="Search query for podcasts")
    parser.add_argument("--feed-id", "-f", type=int, help="Get podcast by feed ID")
    parser.add_argument("--episode-id", "-e", type=int, help="Get episode by ID")
    parser.add_argument("--output", "-o", default="podcastindex_validation_results.json",
                        help="Output JSON file (default: podcastindex_validation_results.json)")
    args = parser.parse_args()
    
    print("=" * 60)
    print("Podcast Index API Validation")
    print("=" * 60)
    
    # Check for API credentials
    if not os.environ.get("PODCAST_INDEX_API_KEY"):
        print("\n❌ ERROR: PODCAST_INDEX_API_KEY not set")
        print("Get free API keys at: https://api.podcastindex.org/signup")
        print("\nThen set environment variables:")
        print("  export PODCAST_INDEX_API_KEY='your_key'")
        print("  export PODCAST_INDEX_API_SECRET='your_secret'")
        return
    
    results = {
        "test_type": "podcast_index_api",
        "library": "python-podcastindex",
        "tests": []
    }
    
    if args.search:
        # Search mode
        print(f"\nSearching for: '{args.search}'")
        search_result = search_podcasts(args.search)
        print(json.dumps(search_result, indent=2))
        results["tests"].append({"type": "search", "result": search_result})
        
        # If search successful, get episodes for first result
        if search_result.get("success") and search_result.get("feeds"):
            first_feed = search_result["feeds"][0]
            feed_id = first_feed["id"]
            print(f"\nGetting episodes for '{first_feed['title']}' (ID: {feed_id})...")
            episodes_result = get_episodes_by_feed_id(feed_id)
            print(json.dumps(episodes_result, indent=2))
            results["tests"].append({"type": "episodes", "result": episodes_result})
    
    elif args.feed_id:
        # Get specific podcast
        print(f"\nGetting podcast with feed ID: {args.feed_id}")
        podcast_result = get_podcast_by_feed_id(args.feed_id)
        print(json.dumps(podcast_result, indent=2))
        results["tests"].append({"type": "podcast", "result": podcast_result})
        
        # Get episodes
        print(f"\nGetting episodes...")
        episodes_result = get_episodes_by_feed_id(args.feed_id)
        print(json.dumps(episodes_result, indent=2))
        results["tests"].append({"type": "episodes", "result": episodes_result})
    
    elif args.episode_id:
        # Get specific episode
        print(f"\nGetting episode ID: {args.episode_id}")
        episode_result = get_episode_by_id(args.episode_id)
        print(json.dumps(episode_result, indent=2))
        results["tests"].append({"type": "episode", "result": episode_result})
    
    else:
        # Default test mode
        test_queries = [
            "This American Life",
            "Huberman Lab",
            "Lex Fridman"
        ]
        
        for query in test_queries:
            print(f"\n{'-' * 60}")
            print(f"Search Query: {query}")
            print("-" * 60)
            
            # Search
            search_result = search_podcasts(query, limit=3)
            
            if search_result["success"]:
                print(f"✓ Found {search_result['total_results']} result(s)")
                
                if search_result["feeds"]:
                    # Show first result
                    feed = search_result["feeds"][0]
                    print(f"\n  Top result:")
                    print(f"    Title: {feed['title']}")
                    print(f"    Author: {feed['author']}")
                    print(f"    Episodes: {feed.get('episode_count', 'N/A')}")
                    print(f"    Language: {feed.get('language', 'N/A')}")
                    print(f"    Categories: {', '.join(feed.get('categories', [])[:3])}")
                    
                    # Get episodes
                    print(f"\n  Fetching latest episodes...")
                    episodes_result = get_episodes_by_feed_id(feed["id"], limit=3)
                    
                    if episodes_result["success"]:
                        print(f"  ✓ Found {episodes_result['total_episodes']} episode(s)")
                        
                        for i, ep in enumerate(episodes_result["episodes"][:3], 1):
                            print(f"\n    [{i}] {ep['title']}")
                            print(f"        Published: {ep['date_published']}")
                            print(f"        Duration: {ep['duration_formatted']}")
                            print(f"        Audio URL: {ep['enclosure_url'][:70]}..." if ep['enclosure_url'] and len(ep['enclosure_url']) > 70 else f"        Audio URL: {ep['enclosure_url']}")
                            if ep['transcript_url']:
                                print(f"        ✓ Transcript URL available!")
                    else:
                        print(f"  ✗ Failed to get episodes: {episodes_result.get('error')}")
            else:
                print(f"✗ Search failed: {search_result.get('error_message')}")
            
            results["tests"].append({
                "query": query,
                "search": search_result,
                "episodes": episodes_result if search_result.get("success") and search_result.get("feeds") else None
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


if __name__ == "__main__":
    main()
