import sys
import re


def extract_video_id(url):
    """Extracts the video ID from a YouTube URL."""
    patterns = [
        r"(?:v=|\/)([0-9A-Za-z_-]{11}).*",
        r"youtu\.be\/([0-9A-Za-z_-]{11})",
        r"embed\/([0-9A-Za-z_-]{11})",
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None


def get_transcript(video_id):
    """Fetches the transcript for a given video ID."""
    try:
        from youtube_transcript_api import YouTubeTranscriptApi

        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        # Join the transcript pieces into a single string
        return " ".join([item["text"] for item in transcript_list])
    except ImportError:
        return "Error: 'youtube-transcript-api' library not found. Please install it with 'pip install youtube-transcript-api'."
    except Exception as e:
        return f"Error: {str(e)}"


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python get_transcript.py <youtube_url>")
        sys.exit(1)

    url = sys.argv[1]
    video_id = extract_video_id(url)

    if not video_id:
        print("Error: Could not extract Video ID from URL.")
        sys.exit(1)

    transcript = get_transcript(video_id)
    print(transcript)
