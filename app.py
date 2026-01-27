import streamlit as st
import yt_dlp
import instaloader
import os
import shutil
import time
import requests
from streamlit_lottie import st_lottie

# --- KONFIGURASI HALAMAN BARU ---
st.set_page_config(page_title="Rifki Downloader", page_icon="🌿", layout="centered")

# --- FUNGSI LOAD ANIMASI LOTTIE ---
def load_lottieurl(url):
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None

# --- CSS: TEMA ALAM BERGERAK ---
st.markdown("""
    <style>
    /* 1. Background Gerak Nuansa Alam (Hutan & Air) */
    .stApp {
        /* Perpaduan warna hijau daun, biru air, dan sedikit cahaya matahari */
        background: linear-gradient(-45deg, #134E5E, #71B280, #2bc0e4, #eaecc6);
        background-size: 400% 400%;
        /* Animasi gerak lambat yang menenangkan (30 detik) */
        animation: gradient 30s ease infinite;
    }
    
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* 2. Card Putih Transparan (Agar tulisan terbaca jelas di atas background) */
    .block-container {
        background-color: rgba(255, 255, 255, 0.92); /* Putih agak transparan */
        padding: 3rem 2rem;
        border-radius: 25px;
        box-shadow: 0 20px 40px rgba(0,0,0,0.2);
        margin-top: 2rem;
        border: 1px solid rgba(255, 255, 255, 0.3);
    }

    /* 3. Judul Keren */
    h1 {
        color: #2E7D32; /* Hijau Tua */
        text-align: center;
        font-family: 'Segoe UI', sans-serif;
        font-weight: 800;
        margin-bottom: 0;
    }
    p {
        color: #555;
        text-align: center;
    }
    
    /* 4. Input Box */
    .stTextInput > div > div > input {
        text-align: center;
        border-radius: 15px;
        border: 2px solid #A5D6A7; /* Hijau muda */
        padding: 15px;
    }
    .stTextInput > div > div > input:focus {
        border-color: #2E7D32;
        box-shadow: 0 0 10px rgba(46, 125, 50, 0.3);
    }
    
    /* 5. Tombol Utama (Warna Alam Hijau-Biru) */
    .stButton > button {
        width: 100%;
        background: linear-gradient(90deg, #11998e 0%, #38ef7d 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 15px;
        font-weight: bold;
        font-size: 16px;
        transition: transform 0.1s;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
    .stButton > button:active {
        transform: scale(0.98);
    }
    
    /* Hilangkan footer */
    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# --- LOAD ANIMASI (Ganti jadi tema yang lebih kalem) ---
# Animasi orang santai dengan gadget
lottie_download = load_lottieurl("https://assets10.lottiefiles.com/packages/lf20_qp1q7mct.json")

# --- TAMPILAN ATAS (Header) ---
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if lottie_download:
        st_lottie(lottie_download, height=180, key="nature_vibe")

# --- JUDUL BARU ---
st.markdown("<h1 style='text-align: center;'>🌿 Rifki Downloader</h1>", unsafe_allow_html=True)
st.markdown("<p>Simpan video TikTok, IG, & YouTube dengan mudah.</p>", unsafe_allow_html=True)

# --- FUNGSI TOOLS ---
def clean_filename(title):
    return "".join([c for c in title if c.isalpha() or c.isdigit() or c==' ']).rstrip()

def detect_type(url):
    if "instagram.com/p/" in url:
        return "FOTO"
    return "VIDEO"

# --- INPUT AREA ---
url = st.text_input("", placeholder="Tempel Link di sini...")

if url:
    tipe_konten = detect_type(url)
    st.write("") 

    if st.button(f"🚀 Mulai Download {tipe_konten}"):
        
        # --- LOGIKA VIDEO ---
        if tipe_konten == "VIDEO":
            status = st.info("🔄 Sedang memproses di server...")
            bar = st.progress(10)
            
            ydl_opts = {
                'format': 'best',
                'outtmpl': 'temp_video.%(ext)s',
                'quiet': True,
            }
            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    bar.progress(40)
                    info = ydl.extract_info(url, download=True)
                    judul = clean_filename(info.get('title', 'video'))
                    ext = info.get('ext', 'mp4')
                    bar.progress(100)
                
                if os.path.exists(f"temp_video.{ext}"):
                    status.success("✅ Selesai! Silakan simpan.")
                    with open(f"temp_video.{ext}", "rb") as f:
                        st.download_button(
                            label="⬇️ SIMPAN VIDEO KE GALERI",
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
            status = st.info("📸 Sedang mengambil foto...")
            temp_dir = "temp_ig_nature"
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
                    status.success("✅ Foto siap disimpan!")
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
                    status.error("Foto tidak ditemukan.")
            except Exception as e:
                status.error(f"Gagal: {e}")
