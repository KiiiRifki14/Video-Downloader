import streamlit as st
import yt_dlp
import instaloader
import os
import shutil
import time
import requests
from streamlit_lottie import st_lottie

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Rifki Downloader", page_icon="⚡", layout="centered")

# --- FUNGSI LOAD ANIMASI LOTTIE ---
def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# --- CSS: ANIMASI BACKGROUND & TAMPILAN ---
st.markdown("""
    <style>
    /* 1. Background Bergerak (Animated Gradient) */
    .stApp {
        background: linear-gradient(-45deg, #ee7752, #e73c7e, #23a6d5, #23d5ab);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
    }
    
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* 2. Card Putih Transparan (Glassmorphism) */
    .block-container {
        background-color: rgba(255, 255, 255, 0.95); /* Putih agak transparan */
        padding: 3rem 2rem;
        border-radius: 25px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.2);
        margin-top: 2rem;
    }

    /* 3. Judul Keren */
    h1 {
        color: #2c3e50;
        text-align: center;
        font-family: 'Segoe UI', sans-serif;
        font-weight: 800;
        margin-bottom: 0;
    }
    
    /* 4. Tombol Utama dengan Efek Tekan */
    .stButton > button {
        width: 100%;
        background: linear-gradient(90deg, #4b6cb7 0%, #182848 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 15px;
        font-weight: bold;
        transition: transform 0.1s;
    }
    .stButton > button:active {
        transform: scale(0.95);
    }
    
    /* Hilangkan footer */
    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# --- LOAD ANIMASI ---
# Ini URL animasi Lottie (Bisa diganti cari di lottiefiles.com)
lottie_download = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_S8d8sK.json")

# --- TAMPILAN ATAS (Header) ---
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    # Menampilkan animasi di tengah
    if lottie_download:
        st_lottie(lottie_download, height=200, key="coding")

st.markdown("<h1 style='text-align: center;'>⚡ Ultra Downloader</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #555;'>Paste link TikTok, IG, atau YouTube di bawah</p>", unsafe_allow_html=True)

# --- FUNGSI TOOLS ---
def clean_filename(title):
    return "".join([c for c in title if c.isalpha() or c.isdigit() or c==' ']).rstrip()

def detect_type(url):
    if "instagram.com/p/" in url:
        return "FOTO"
    return "VIDEO"

# --- INPUT AREA ---
url = st.text_input("", placeholder="🔗 Tempel Link di sini...")

if url:
    tipe_konten = detect_type(url)
    st.write("") 

    if st.button(f"🚀 Mulai Download {tipe_konten}"):
        
        # --- LOGIKA VIDEO ---
        if tipe_konten == "VIDEO":
            status = st.info("🔄 Sedang memproses...")
            bar = st.progress(10)
            
            ydl_opts = {
                'format': 'best',
                'outtmpl': 'temp_video.%(ext)s',
                'quiet': True,
            }
            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    bar.progress(50)
                    info = ydl.extract_info(url, download=True)
                    judul = clean_filename(info.get('title', 'video'))
                    ext = info.get('ext', 'mp4')
                    bar.progress(100)
                
                if os.path.exists(f"temp_video.{ext}"):
                    status.success("✅ Selesai!")
                    with open(f"temp_video.{ext}", "rb") as f:
                        st.download_button(
                            label="⬇️ SIMPAN VIDEO",
                            data=f,
                            file_name=f"{judul}.{ext}",
                            mime=f"video/{ext}",
                            use_container_width=True,
                            type="primary"
                        )
            except Exception as e:
                status.error(f"Error: {e}")

        # --- LOGIKA FOTO ---
        elif tipe_konten == "FOTO":
            status = st.info("📸 Mengambil foto...")
            temp_dir = "temp_ig"
            if os.path.exists(temp_dir): shutil.rmtree(temp_dir)
            
            try:
                L = instaloader.Instaloader(save_metadata=False, download_videos=False)
                shortcode = url.split("/p/")[1].split("/")[0]
                post = instaloader.Post.from_shortcode(L.context, shortcode)
                L.download_post(post, target=temp_dir)
                
                target_file = None
                for f in os.listdir(temp_dir):
                    if f.endswith(".jpg"):
                        target_file = os.path.join(temp_dir, f)
                        break
                
                if target_file:
                    status.success("✅ Foto Ditemukan!")
                    with open(target_file, "rb") as f:
                        st.download_button(
                            label="⬇️ SIMPAN FOTO",
                            data=f,
                            file_name=f"IG_{shortcode}.jpg",
                            mime="image/jpeg",
                            use_container_width=True,
                            type="primary"
                        )
                    shutil.rmtree(temp_dir)
                else:
                    status.error("Foto tidak ketemu.")
            except Exception as e:
                status.error(f"Gagal: {e}")

