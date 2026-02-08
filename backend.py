import yt_dlp
import instaloader
import os
import shutil
import uuid
from pathlib import Path

# --- KONFIGURASI "TOPENG" (Agar tidak dianggap Bot) ---
CUSTOM_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Referer': 'https://www.tiktok.com/',
}

# --- INFO VIDEO ---
def get_video_info(url):
    try:
        # Khusus Instagram
        if "instagram.com" in url:
            return {"title": "Instagram Post", "thumbnail": None, "duration_string": "Slide/Carousel", "ext": "Mixed"}
        
        # Khusus TikTok & YouTube
        ydl_opts = {
            "quiet": True, 
            "skip_download": True,
            "no_warnings": True,
            "ignoreerrors": True, # Penting: Jangan langsung error kalau ada 1 bagian gagal
            "http_headers": CUSTOM_HEADERS, # Pakai Topeng Browser
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            # Jika gagal total
            if not info: return None
            
            # Jika linknya adalah Slide TikTok, biasanya infonya ada di 'entries'
            if 'entries' in info:
                # Ambil info dari slide pertama saja sebagai perwakilan
                first_entry = info['entries'][0]
                return {
                    "title": info.get('title', 'TikTok Slide'),
                    "thumbnail": first_entry.get('thumbnail'),
                    "duration_string": "TikTok Slide",
                    "ext": "Album"
                }
                
            return info
            
    except Exception as e:
        print(f"Error Info: {e}")
        return None

# --- ENGINE DOWNLOAD (RETURN LIST FILE) ---
def download_video(url):
    # Buat folder unik
    unique_id = str(uuid.uuid4())
    base_folder = Path("temp_downloads")
    target_dir = base_folder / unique_id
    target_dir.mkdir(parents=True, exist_ok=True)

    found_files = [] 

    try:
        # === KASUS 1: INSTAGRAM ===
        if "instagram.com" in url:
            L = instaloader.Instaloader(
                save_metadata=False, 
                download_videos=True,
                download_video_thumbnails=False,
                download_geotags=False, 
                download_comments=False,
                compress_json=False,
                user_agent=CUSTOM_HEADERS['User-Agent']
            )
            
            if "/p/" in url: shortcode = url.split("/p/")[1].split("/")[0]
            elif "/reel/" in url: shortcode = url.split("/reel/")[1].split("/")[0]
            else: return []

            post = instaloader.Post.from_shortcode(L.context, shortcode)
            L.download_post(post, target=target_dir)

        # === KASUS 2: TIKTOK & YOUTUBE ===
        else:
            # Settingan Download
            outtmpl = str(target_dir / "%(title)s_%(id)s.%(ext)s")
            
            ydl_opts = {
                "outtmpl": outtmpl,
                "quiet": True,
                "no_warnings": True,
                "ignoreerrors": True,
                "http_headers": CUSTOM_HEADERS, # Pakai Topeng Browser
                # PENTING: Jangan convert slide jadi video, biarkan download aslinya
                "write_pages": True, 
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
        
        # === SCAN & BERSIHKAN FILE ===
        # Kita hanya ambil file gambar (jpg/png) dan video (mp4/webm)
        # Sambil menghapus file sampah .json atau .txt
        allowed_ext = ('.jpg', '.jpeg', '.png', '.mp4', '.webm', '.mp3', '.m4a')
        
        for f in os.listdir(target_dir):
            file_path = target_dir / f
            
            if f.endswith(allowed_ext):
                found_files.append(str(file_path))
            else:
                # Hapus file sampah (json description dll)
                try: os.remove(file_path)
                except: pass
        
        # Urutkan file biar rapi (Foto 1, Foto 2, dst)
        found_files.sort()
        
        return found_files 

    except Exception as e:
        print(f"Error Download: {e}")
        return []
