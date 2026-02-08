import yt_dlp
import instaloader
import os
import shutil
import uuid
import requests
from pathlib import Path

# --- KONFIGURASI TOPENG (Menyamar jadi iPhone) ---
CUSTOM_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1',
    'Accept-Language': 'en-US,en;q=0.9',
}

# --- FUNGSI PENGHANCUR LINK PENDEK (vt.tiktok.com) ---
def unshorten_url(url):
    try:
        # Jika link pendek, kita telusuri aslinya
        if "vt.tiktok.com" in url or "vm.tiktok.com" in url or "bit.ly" in url:
            response = requests.head(url, allow_redirects=True, headers=CUSTOM_HEADERS)
            return response.url
        return url
    except:
        return url

# --- INFO VIDEO ---
def get_video_info(url):
    # 1. Perbaiki Link Dulu
    clean_url = unshorten_url(url)
    
    try:
        # Khusus Instagram
        if "instagram.com" in clean_url:
            return {"title": "Instagram Post", "thumbnail": None, "duration_string": "Slide/Carousel", "ext": "Mixed"}
        
        # Khusus TikTok & YouTube
        ydl_opts = {
            "quiet": True, 
            "no_warnings": True,
            "ignoreerrors": True,
            "http_headers": CUSTOM_HEADERS,
            "skip_download": True, # Hanya ambil info
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Ambil info mentah
            info = ydl.extract_info(clean_url, download=False)
            
            if not info: return None
            
            # CEK APAKAH INI SLIDE TIKTOK?
            # TikTok Slide biasanya dianggap 'playlist' atau punya 'entries'
            if 'entries' in info:
                first_entry = list(info['entries'])[0] # Ambil slide pertama
                return {
                    "title": info.get('title', 'TikTok Slide Gallery'),
                    "thumbnail": first_entry.get('thumbnail'), # Pakai thumb slide 1
                    "duration_string": f"{len(list(info['entries']))} Slide",
                    "ext": "Album"
                }
                
            return info
            
    except Exception as e:
        print(f"Error Info: {e}")
        return None

# --- ENGINE DOWNLOAD (RETURN LIST FILE) ---
def download_video(url):
    # 1. Perbaiki Link Dulu
    clean_url = unshorten_url(url)
    
    # Buat folder unik
    unique_id = str(uuid.uuid4())
    base_folder = Path("temp_downloads")
    target_dir = base_folder / unique_id
    target_dir.mkdir(parents=True, exist_ok=True)

    found_files = [] 

    try:
        # === KASUS 1: INSTAGRAM ===
        if "instagram.com" in clean_url:
            L = instaloader.Instaloader(
                save_metadata=False, 
                download_videos=True,
                download_video_thumbnails=False,
                download_geotags=False, 
                download_comments=False,
                compress_json=False,
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            )
            
            if "/p/" in clean_url: shortcode = clean_url.split("/p/")[1].split("/")[0]
            elif "/reel/" in clean_url: shortcode = clean_url.split("/reel/")[1].split("/")[0]
            else: return []

            post = instaloader.Post.from_shortcode(L.context, shortcode)
            L.download_post(post, target=target_dir)

        # === KASUS 2: TIKTOK (SLIDE & VIDEO) & YOUTUBE ===
        else:
            # Settingan Download
            outtmpl = str(target_dir / "%(title)s_%(id)s.%(ext)s")
            
            ydl_opts = {
                "outtmpl": outtmpl,
                "quiet": True,
                "no_warnings": True,
                "ignoreerrors": True,
                "http_headers": CUSTOM_HEADERS,
                "format": "best", # Kualitas terbaik
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # Ini akan mendownload Video ATAU semua Slide foto
                ydl.download([clean_url])
        
        # === SCAN & BERSIHKAN FILE ===
        # Ambil semua hasil download yang valid
        allowed_ext = ('.jpg', '.jpeg', '.png', '.mp4', '.webm', '.webp')
        
        for f in os.listdir(target_dir):
            file_path = target_dir / f
            
            if f.lower().endswith(allowed_ext):
                found_files.append(str(file_path))
            else:
                # Hapus file sampah (json, txt, description)
                try: os.remove(file_path)
                except: pass
        
        # Urutkan biar rapi
        found_files.sort()
        return found_files 

    except Exception as e:
        print(f"Error Download: {e}")
        return []
