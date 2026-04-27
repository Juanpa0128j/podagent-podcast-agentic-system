#!/usr/bin/env python3
"""
Script 1: YouTube Transcript Validation
Tests youtube-transcript-api with popular podcast YouTube videos.

Supports proxy configuration via environment variables:
    HTTP_PROXY=http://user:pass@proxy:port
    HTTPS_PROXY=https://user:pass@proxy:port

Or use Webshare proxy:
    WEBSHARE_PROXY_USERNAME=your_username
    WEBSHARE_PROXY_PASSWORD=your_password

Usage:
    python validate_youtube.py
    python validate_youtube.py --video-id <VIDEO_ID>
    python validate_youtube.py --use-proxy
"""

import json
import time
import argparse
import os
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import JSONFormatter, TextFormatter


def get_ytt_api_with_proxy():
    """Initialize YouTubeTranscriptApi with proxy if configured."""
    # Check for Webshare proxy
    webshare_username = os.environ.get("WEBSHARE_PROXY_USERNAME")
    webshare_password = os.environ.get("WEBSHARE_PROXY_PASSWORD")
    
    if webshare_username and webshare_password:
        print("   Using Webshare proxy...")
        from youtube_transcript_api.proxies import WebshareProxyConfig
        return YouTubeTranscriptApi(
            proxy_config=WebshareProxyConfig(
                proxy_username=webshare_username,
                proxy_password=webshare_password,
            )
        )
    
    # Check for generic HTTP/HTTPS proxy
    http_proxy = os.environ.get("HTTP_PROXY")
    https_proxy = os.environ.get("HTTPS_PROXY")
    
    if http_proxy or https_proxy:
        print("   Using generic proxy...")
        from youtube_transcript_api.proxies import GenericProxyConfig
        return YouTubeTranscriptApi(
            proxy_config=GenericProxyConfig(
                http_url=http_proxy,
                https_url=https_proxy,
            )
        )
    
    # No proxy configured
    return YouTubeTranscriptApi()


# Popular podcast episodes on YouTube for testing
TEST_VIDEOS = [
    {
        "name": "Huberman Lab - Intro to Episode",
        "video_id": "9Uq_zig3LgI",  # Short intro video
        "description": "Huberman Lab Podcast - Andrew Huberman"
    },
    {
        "name": "Lex Fridman Podcast - Sample",
        "video_id": "gP5gl3Nf0C8",  # Lex Fridman intro
        "description": "Lex Fridman Podcast"
    },
    {
        "name": "The Diary of a CEO - Sample",
        "video_id": "Z2C9jzbcf0Q",  # Steven Bartlett
        "description": "The Diary of a CEO"
    }
]


def fetch_transcript(video_id: str, use_proxy: bool = False) -> dict:
    """Fetch transcript for a YouTube video."""
    start_time = time.time()
    
    try:
        # Initialize API (with or without proxy)
        if use_proxy:
            ytt_api = get_ytt_api_with_proxy()
        else:
            ytt_api = YouTubeTranscriptApi()
        
        # Fetch transcript (auto-detects language, prefers English)
        transcript = ytt_api.fetch(video_id, languages=['en'])
        
        elapsed_time = time.time() - start_time
        
        # Convert to raw data
        raw_data = transcript.to_raw_data()
        
        return {
            "success": True,
            "video_id": video_id,
            "language": transcript.language,
            "language_code": transcript.language_code,
            "is_generated": transcript.is_generated,
            "snippet_count": len(transcript.snippets),
            "first_snippet": raw_data[0] if raw_data else None,
            "last_snippet": raw_data[-1] if raw_data else None,
            "sample_snippets": raw_data[:3] if len(raw_data) >= 3 else raw_data,
            "extraction_time_seconds": round(elapsed_time, 2),
            "total_duration_seconds": raw_data[-1]["start"] + raw_data[-1]["duration"] if raw_data else 0
        }
    
    except Exception as e:
        elapsed_time = time.time() - start_time
        return {
            "success": False,
            "video_id": video_id,
            "error": str(type(e).__name__),
            "error_message": str(e),
            "extraction_time_seconds": round(elapsed_time, 2)
        }


def list_available_transcripts(video_id: str) -> dict:
    """List all available transcripts for a video."""
    try:
        ytt_api = YouTubeTranscriptApi()
        transcript_list = ytt_api.list(video_id)
        
        available = []
        for transcript in transcript_list:
            available.append({
                "language": transcript.language,
                "language_code": transcript.language_code,
                "is_generated": transcript.is_generated,
                "is_translatable": transcript.is_translatable,
                "translation_languages_count": len(transcript.translation_languages)
            })
        
        return {
            "success": True,
            "video_id": video_id,
            "available_transcripts": available
        }
    except Exception as e:
        return {
            "success": False,
            "video_id": video_id,
            "error": str(e)
        }


def main():
    parser = argparse.ArgumentParser(description="Validate YouTube transcript extraction")
    parser.add_argument("--video-id", help="Test a specific YouTube video ID")
    parser.add_argument("--output", "-o", default="youtube_validation_results.json",
                        help="Output JSON file (default: youtube_validation_results.json)")
    parser.add_argument("--use-proxy", action="store_true",
                        help="Use proxy if configured via environment variables")
    args = parser.parse_args()
    
    print("=" * 60)
    print("YouTube Transcript API Validation")
    if args.use_proxy:
        print("(Proxy enabled)")
    print("=" * 60)
    
    results = {
        "test_type": "youtube_transcript_api",
        "library": "youtube-transcript-api",
        "tests": []
    }
    
    if args.video_id:
        # Test specific video
        print(f"\nTesting video ID: {args.video_id}")
        
        # List available transcripts
        print("\n1. Listing available transcripts...")
        list_result = list_available_transcripts(args.video_id)
        print(json.dumps(list_result, indent=2))
        
        # Fetch transcript
        print("\n2. Fetching transcript...")
        transcript_result = fetch_transcript(args.video_id, use_proxy=args.use_proxy)
        print(json.dumps(transcript_result, indent=2))
        
        results["tests"].append({
            "video_id": args.video_id,
            "list_result": list_result,
            "transcript_result": transcript_result
        })
    else:
        # Test default videos
        for video in TEST_VIDEOS:
            print(f"\n{'-' * 60}")
            print(f"Testing: {video['name']}")
            print(f"Video ID: {video['video_id']}")
            print(f"Description: {video['description']}")
            print("-" * 60)
            
            # List available transcripts
            print("\n1. Listing available transcripts...")
            list_result = list_available_transcripts(video['video_id'])
            if list_result["success"]:
                print(f"   Found {len(list_result['available_transcripts'])} transcript(s)")
                for t in list_result['available_transcripts']:
                    gen_type = "auto-generated" if t['is_generated'] else "manual"
                    print(f"   - {t['language']} ({t['language_code']}): {gen_type}")
            else:
                print(f"   Error: {list_result.get('error', 'Unknown')}")
            
            # Fetch transcript
            print("\n2. Fetching transcript...")
            transcript_result = fetch_transcript(video['video_id'], use_proxy=args.use_proxy)
            
            if transcript_result["success"]:
                print(f"   ✓ Success!")
                print(f"   - Language: {transcript_result['language']}")
                print(f"   - Type: {'auto-generated' if transcript_result['is_generated'] else 'manual'}")
                print(f"   - Snippets: {transcript_result['snippet_count']}")
                print(f"   - Extraction time: {transcript_result['extraction_time_seconds']}s")
                print(f"\n   Sample snippets:")
                for i, snippet in enumerate(transcript_result['sample_snippets'], 1):
                    text = snippet['text'][:80] + "..." if len(snippet['text']) > 80 else snippet['text']
                    print(f"   [{i}] @{snippet['start']:.1f}s: {text}")
            else:
                print(f"   ✗ Failed: {transcript_result.get('error_message', 'Unknown error')}")
            
            results["tests"].append({
                "video": video,
                "list_result": list_result,
                "transcript_result": transcript_result
            })
    
    # Save results
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\n{'=' * 60}")
    print(f"Results saved to: {args.output}")
    print("=" * 60)
    
    # Summary
    successful = sum(1 for t in results["tests"] if t["transcript_result"].get("success"))
    total = len(results["tests"])
    print(f"\nSummary: {successful}/{total} tests successful")


if __name__ == "__main__":
    main()
