import yt_dlp
import os
import uuid # Tambahkan ini untuk nama unik
from pathlib import Path

def get_video_info(url):
    try:
        ydl_opts = {"quiet": True, "skip_download": True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return info
    except Exception as e:
        print(f"Error fetching info: {e}")
        return None

def download_video(url):
    try:
        # Gunakan folder unique agar tidak bentrok antar user
        unique_id = str(uuid.uuid4())
        temp_dir = Path("temp_downloads") / unique_id
        temp_dir.mkdir(parents=True, exist_ok=True)
        
        # Template nama file
        outtmpl = str(temp_dir / "%(title)s.%(ext)s")
        
        ydl_opts = {
            "outtmpl": outtmpl,
            "quiet": True,
            "noplaylist": True,
            # Format terbaik yg kompatibel (mp4) agar tidak perlu merge ribet
            "format": "best[ext=mp4]/best", 
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            
        # Cari file yang barusan didownload di folder unique tersebut
        candidates = list(temp_dir.glob("*"))
        if candidates:
            # Kembalikan path file
            return str(candidates[0])
        return None
    except Exception as e:
        print(f"Download error: {e}")
        return None
