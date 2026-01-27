import streamlit as st
import yt_dlp
import instaloader
import os
import shutil
import time
import requests
from streamlit_lottie import st_lottie

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Rifki Downloader", page_icon="🚀", layout="centered")

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

# --- 3. CSS: TEMA DARK & TOMBOL PUTIH ---
st.markdown("""
    <style>
    /* Background Gradient Gelap */
    .stApp {
        background: linear-gradient(135deg, #000000 0%, #1a1a1a 100%);
        color: white;
    }
    
    /* Input Box */
    .stTextInput > div > div > input {
        background-color: #222;
        color: white;
        border: 1px solid #444;
        border-radius: 12px;
        text-align: center;
        padding: 15px;
        font-size: 16px;
    }
    .stTextInput > div > div > input:focus {
        border-color: #ffffff;
        box-shadow: 0 0 10px rgba(255, 255, 255, 0.2);
    }

    /* TOMBOL UTAMA (MODIFIKASI: Putih, Besar, Simetris) */
    .stButton > button {
        width: 100%;             /* Lebar penuh agar simetris dengan input */
        background-color: #ffffff; /* Warna Putih */
        color: #000000;          /* Teks Hitam */
        border: none;
        padding: 18px 0px;       /* Padding atas-bawah dibesarkan */
        font-size: 20px;         /* Ukuran font dibesarkan */
        font-weight: 800;        /* Font tebal */
        border-radius: 12px;
        margin-top: 10px;
        transition: all 0.3s;
        box-shadow: 0 5px 15px rgba(255, 255, 255, 0.15);
    }
    
    /* Efek Hover Tombol */
    .stButton > button:hover {
        background-color: #e0e0e0;
        transform: scale(1.02);
        box-shadow: 0 8px 20px rgba(255, 255, 255, 0.3);
    }
    
    /* Hide Footer */
    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    
    /* Judul */
    h1 {
        text-align: center; 
        font-family: 'Arial Black', sans-serif;
        margin-bottom: 0px;
    }
    </style>
""", unsafe_allow_html=True)

# --- 4. TAMPILAN UTAMA ---
# Animasi Robot
lottie_tech = load_lottieurl("https://assets3.lottiefiles.com/packages/lf20_w51pcehl.json")

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if lottie_tech:
        st_lottie(lottie_tech, height=150, key="tech")

st.markdown("<h1>Rifki Downloader</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>TikTok • Instagram • YouTube</p>", unsafe_allow_html=True)
st.write("---")

# --- 5. INPUT & TOMBOL (Button diluar If) ---
url = st.text_input("", placeholder="Paste Link di sini...")

# Tombol dibuat Full Width (use_container_width=True) agar simetris
if st.button("MULAI PROSES ⚡", use_container_width=True):
    
    if not url:
        st.warning("⚠️ Eits, link-nya belum ditempel!")
    else:
        tipe = detect_type(url)
        
        # --- LOGIKA DOWNLOAD VIDEO ---
        if tipe == "VIDEO":
            status = st.info("🔄 Sedang mencari video...")
            
            ydl_opts = {'format': 'best', 'outtmpl': 'temp_vid.%(ext)s', 'quiet': True}
            
            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    judul = clean_filename(info.get('title', 'Video'))
                    ext = info.get('ext', 'mp4')
                
                if os.path.exists(f"temp_vid.{ext}"):
                    status.success("✅ Selesai!")
                    with open(f"temp_vid.{ext}", "rb") as f:
                        st.download_button(
                            label="⬇️ DOWNLOAD VIDEO",
                            data=f,
                            file_name=f"{judul}.{ext}",
                            mime=f"video/{ext}",
                            use_container_width=True
                        )
            except Exception as e:
                status.error(f"Error: {e}")

        # --- LOGIKA DOWNLOAD FOTO ---
        elif tipe == "FOTO":
            status = st.info("📸 Sedang mengambil foto...")
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
                    status.success("✅ Foto siap!")
                    with open(target, "rb") as f:
                        st.download_button(
                            label="⬇️ DOWNLOAD FOTO",
                            data=f,
                            file_name=f"IG_{shortcode}.jpg",
                            mime="image/jpeg",
                            use_container_width=True
                        )
                    shutil.rmtree("temp_img")
                else:
                    status.error("Foto tidak ditemukan.")
            except Exception as e:
                status.error("Gagal mengambil gambar.")
