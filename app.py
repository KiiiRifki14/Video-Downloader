import streamlit as st
import yt_dlp
import instaloader
import os
import shutil
import time
import requests
from streamlit_lottie import st_lottie

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Rifki Downloader", page_icon="🍃", layout="centered")

# --- 2. FUNGSI UTILITIES ---
def load_lottieurl(url):
    try:
        r = requests.get(url)
        if r.status_code != 200: return None
        return r.json()
    except: return None

def clean_filename(title):
    return "".join([c for c in title if c.isalpha() or c.isdigit() or c==' ']).rstrip()

def detect_type(url):
    if "instagram.com/p/" in url: return "FOTO"
    return "VIDEO"

# --- 3. CSS: TEMA EARTHY GREEN CARD ---
st.markdown("""
    <style>
    /* BACKGROUND HALAMAN: Gradasi Cream ke Hijau Muda */
    .stApp {
        background: linear-gradient(180deg, #F0E491 0%, #BBC863 100%);
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    /* KARTU UTAMA (Card Container) */
    /* Ini adalah kotak tengah yang mirip contoh gambar, pakai Hijau Tua (#31694E) */
    .block-container {
        background-color: #31694E;
        padding: 3rem 2rem;
        border-radius: 30px; /* Sudut membulat */
        box-shadow: 0 20px 50px rgba(49, 105, 78, 0.4); /* Bayangan halus */
        margin-top: 2rem;
    }

    /* TEXT STYLE */
    h1 {
        color: #F0E491 !important; /* Judul warna Cream biar kontras */
        text-align: center;
        font-weight: 800;
        font-size: 2.2rem;
        margin-bottom: 5px;
        text-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }
    p {
        color: #BBC863 !important; /* Sub-judul warna Hijau Muda */
        text-align: center;
        font-size: 1rem;
        margin-bottom: 30px;
    }

    /* INPUT BOX (Kolom Link) */
    .stTextInput > div > div > input {
        background-color: #ffffff;
        color: #31694E;
        border: none;
        border-radius: 15px;
        padding: 18px;
        text-align: center;
        font-size: 16px;
        box-shadow: inset 0 2px 5px rgba(0,0,0,0.1);
    }
    /* Efek saat diklik */
    .stTextInput > div > div > input:focus {
        box-shadow: 0 0 0 3px #BBC863;
    }

    /* TOMBOL UTAMA (Button) */
    /* Warna #F0E491 (Cream) agar POP di atas background hijau tua */
    .stButton > button {
        width: 100%;
        background-color: #F0E491;
        color: #31694E; /* Teks tombol hijau tua */
        border: none;
        padding: 18px 0px;
        font-size: 18px;
        font-weight: 900;
        border-radius: 15px;
        margin-top: 15px;
        transition: all 0.3s ease;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    
    /* Efek Hover Tombol */
    .stButton > button:hover {
        background-color: #ffffff; /* Berubah putih saat disentuh */
        color: #658C58;
        transform: translateY(-3px);
        box-shadow: 0 8px 20px rgba(0,0,0,0.3);
    }

    /* Progress Bar Custom Colors */
    .stProgress > div > div > div > div {
        background-color: #F0E491;
    }
    
    /* Hide Footer */
    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    
    </style>
""", unsafe_allow_html=True)

# --- 4. TAMPILAN UTAMA ---
# Animasi Simple & Bersih (Icon Download)
lottie_url = "https://assets9.lottiefiles.com/packages/lf20_S8d8sK.json" 
lottie_json = load_lottieurl(lottie_url)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if lottie_json:
        st_lottie(lottie_json, height=120, key="icon")

st.markdown("<h1>Rifki Downloader</h1>", unsafe_allow_html=True)
st.markdown("<p>Paste Link TikTok • Instagram • YouTube</p>", unsafe_allow_html=True)

# --- 5. LOGIKA APLIKASI ---
# Input Link
url = st.text_input("", placeholder="Tempel link video di sini...")

# Tombol SELALU MUNCUL (Full Width)
if st.button("MULAI DOWNLOAD ⬇️", use_container_width=True):
    
    if not url:
        st.warning("⚠️ Masukkan link dulu dong!")
    else:
        tipe = detect_type(url)
        
        # --- PROSES VIDEO ---
        if tipe == "VIDEO":
            status_area = st.empty()
            status_area.info("🔄 Sedang mencari video...")
            bar = st.progress(10)
            
            ydl_opts = {'format': 'best', 'outtmpl': 'temp_vid.%(ext)s', 'quiet': True}
            
            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    bar.progress(50)
                    info = ydl.extract_info(url, download=True)
                    judul = clean_filename(info.get('title', 'Video'))
                    ext = info.get('ext', 'mp4')
                    bar.progress(100)
                
                if os.path.exists(f"temp_vid.{ext}"):
                    status_area.success("✅ Berhasil!")
                    with open(f"temp_vid.{ext}", "rb") as f:
                        st.download_button(
                            label="SIMPAN KE GALERI (HD)",
                            data=f,
                            file_name=f"{judul}.{ext}",
                            mime=f"video/{ext}",
                            use_container_width=True
                        )
            except Exception as e:
                status_area.error(f"Gagal: {e}")

        # --- PROSES FOTO ---
        elif tipe == "FOTO":
            status_area = st.empty()
            status_area.info("📸 Sedang mengambil foto...")
            if os.path.exists("temp_img"): shutil.rmtree("temp_img")
            
            try:
                L = instaloader.Instaloader(save_metadata=False, download_videos=False)
                shortcode = url.split("/p/")[1].split("/")[0]
                post = instaloader.Post.from_shortcode(L.context, shortcode)
                L.download_post(post, target="temp_img")
                
                target = None
                for f in os.listdir("temp_img"):
                    if f.endswith(".jpg"):
                        target = os.path.join("temp_img", f)
                        break
                
                if target:
                    status_area.success("✅ Foto siap!")
                    with open(target, "rb") as f:
                        st.download_button(
                            label="SIMPAN FOTO",
                            data=f,
                            file_name=f"IG_{shortcode}.jpg",
                            mime="image/jpeg",
                            use_container_width=True
                        )
                    shutil.rmtree("temp_img")
                else:
                    status_area.error("Foto tidak ditemukan.")
            except Exception as e:
                status_area.error("Gagal ambil foto.")
