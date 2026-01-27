import yt_dlp
import os
from pathlib import Path

def get_video_info(url):
    """
    Fetches video metadata from YouTube URL.
    Returns a dictionary with title, thumbnail, and formats.
    """
    try:
        ydl_opts = {"quiet": True, "skip_download": True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return info
    except Exception as e:
        print(f"Error fetching info: {e}")
        return None

def download_video(url, format_id=None):
    """
    Downloads the video.
    Returns the path to the downloaded file or None if failed.
    """
    try:
        # Default filename template
        outtmpl = "downloaded_video.%(ext)s"
        
        ydl_opts = {
            "outtmpl": outtmpl,
            "quiet": True,
            "noplaylist": True,
        }
        
        # If specific format logic is needed, add it here.
        # For now we stick to best video+audio
        ydl_opts["format"] = "bestvideo+bestaudio/best"

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            
        # Find the file
        candidates = list(Path(".").glob("downloaded_video.*"))
        if candidates:
            return str(candidates[0])
        return None
    except Exception as e:
        print(f"Download error: {e}")
        return None
