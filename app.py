import streamlit as st
import yt_dlp
import instaloader
import os
import shutil
import time
import requests
from streamlit_lottie import st_lottie

# --- 1. KONFIGURASI HALAMAN (FULL WIDTH) ---
st.set_page_config(page_title="Rifki Downloader", page_icon="🚀", layout="centered")

# --- 2. FUNGSI LOAD ANIMASI ---
def load_lottieurl(url):
    try:
        r = requests.get(url)
        if r.status_code != 200: return None
        return r.json()
    except: return None

# --- 3. CSS: TEMA NEO-TECH GLASS ---
st.markdown("""
    <style>
    /* Background Gradient Gelap & Mewah */
    .stApp {
        background: linear-gradient(125deg, #0f0c29, #302b63, #24243e);
        background-size: 400% 400%;
        animation: gradientBG 15s ease infinite;
        color: white;
    }
    
    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* KARTU KACA (Glassmorphism Effect) */
    .block-container {
        background: rgba(255, 255, 255, 0.05); /* Sangat transparan */
        backdrop-filter: blur(15px); /* Efek Blur Kaca */
        -webkit-backdrop-filter: blur(15px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 3rem 2rem;
        margin-top: 2rem;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    }

    /* Judul & Teks */
    h1 {
        font-family: 'Inter', sans-serif;
        font-weight: 800;
        background: -webkit-linear-gradient(eee, #333);
        -webkit-background-clip: text;
        text-shadow: 0 0 20px rgba(255,255,255,0.3);
        text-align: center;
        margin-bottom: 0;
    }
    p {
        color: #b0b0b0; /* Abu-abu terang */
        text-align: center;
    }

    /* Input Box Custom */
    .stTextInput > div > div > input {
        background-color: rgba(0, 0, 0, 0.3);
        color: white;
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 10px;
        text-align: center;
        padding: 12px;
    }
    .stTextInput > div > div > input:focus {
        border-color: #00d2ff;
        box-shadow: 0 0 10px #00d2ff;
    }

    /* Tombol Utama (Gradient Neon) */
    .stButton > button {
        width: 100%;
        background: linear-gradient(90deg, #00d2ff 0%, #3a7bd5 100%);
        border: none;
        color: white;
        padding: 12px 24px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        font-weight: bold;
        border-radius: 8px;
        transition: 0.3s;
        box-shadow: 0 0 15px rgba(0, 210, 255, 0.4);
    }
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 0 25px rgba(0, 210, 255, 0.6);
    }

    /* Hilangkan Footer Bawaan */
    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# --- 4. HEADER & ANIMASI ROBOT ---
# Animasi Robot Tech
lottie_tech = load_lottieurl("https://assets3.lottiefiles.com/packages/lf20_w51pcehl.json")

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if lottie_tech:
        st_lottie(lottie_tech, height=180, key="tech_robot")

st.markdown("<h1>Rifki Downloader <span style='font-size:15px; vertical-align:top; color:#00d2ff;'>PRO</span></h1>", unsafe_allow_html=True)
st.markdown("<p>Premium Video Engine • TikTok • Instagram • YouTube</p>", unsafe_allow_html=True)
st.write("---")

# --- 5. LOGIKA UTAMA ---
def clean_filename(title):
    return "".join([c for c in title if c.isalpha() or c.isdigit() or c==' ']).rstrip()

def detect_type(url):
    if "instagram.com/p/" in url: return "FOTO"
    return "VIDEO"

# Input
url = st.text_input("", placeholder="Paste Link URL di sini...")

if url:
    tipe = detect_type(url)
    st.write("")
    
    # Tombol Aksi
    if st.button(f"⚡ PROSES {tipe} SEKARANG"):
        
        # --- DOWNLOAD VIDEO ---
        if tipe == "VIDEO":
            status = st.empty()
            status.info("📡 Menghubungkan ke satelit server...")
            bar = st.progress(10)
            
            ydl_opts = {'format': 'best', 'outtmpl': 'temp_vid.%(ext)s', 'quiet': True}
            
            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    bar.progress(50)
                    info = ydl.extract_info(url, download=True)
                    judul = clean_filename(info.get('title', 'Video Result'))
                    ext = info.get('ext', 'mp4')
                    bar.progress(100)
                
                if os.path.exists(f"temp_vid.{ext}"):
                    status.success("✅ Rendering Selesai!")
                    with open(f"temp_vid.{ext}", "rb") as f:
                        st.download_button(
                            label="⬇️ DOWNLOAD VIDEO HD",
                            data=f,
                            file_name=f"{judul}.{ext}",
                            mime=f"video/{ext}",
                            use_container_width=True
                        )
            except Exception as e:
                status.error(f"Error: {e}")

        # --- DOWNLOAD FOTO ---
        elif tipe == "FOTO":
            status = st.info("🔍 Scanning image...")
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
                    status.success("✅ Image Captured!")
                    with open(target, "rb") as f:
                        st.download_button(
                            label="⬇️ SAVE IMAGE",
                            data=f,
                            file_name=f"IG_{shortcode}.jpg",
                            mime="image/jpeg",
                            use_container_width=True
                        )
                    shutil.rmtree("temp_img")
                else:
                    status.error("Image not found.")
            except Exception as e:
                status.error("Gagal mengambil gambar.")
