import streamlit as st
import yt_dlp
import instaloader
import os
import shutil
import time
import requests
from streamlit_lottie import st_lottie

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Loader.fo Clone", page_icon="🎬", layout="wide")

# --- 2. FUNGSI UTILITIES ---
def clean_filename(title):
    return "".join([c for c in title if c.isalnum() or c==' ']).rstrip()

def detect_type(url):
    if "instagram.com/p/" in url: return "FOTO"
    return "VIDEO"

# --- 3. CSS: DARK MODE PREMIUM (Persis Referensi) ---
st.markdown("""
    <style>
    /* RESET & BACKGROUND UTAMA (Hitam Pekat) */
    .stApp {
        background-color: #050505;
        font-family: 'Inter', sans-serif;
    }
    
    /* CONTAINER TENGAH (Kartu Abu-abu Gelap) */
    /* Ini meniru kotak besar di tengah layar */
    div[data-testid="stVerticalBlock"] > div {
        max-width: 900px;
        margin: 0 auto;
    }

    /* HEADER TEXT */
    h1 {
        color: white;
        text-align: center;
        font-weight: 800;
        font-size: 3.5rem;
        margin-bottom: 0px;
        letter-spacing: -1px;
    }
    
    /* SUBTITLE */
    p {
        color: #888888;
        text-align: center;
        font-size: 1rem;
        margin-top: 10px;
    }

    /* INPUT BOX (Kolom Link) - Style Gelap Bulat */
    .stTextInput > div > div > input {
        background-color: #1F1F1F; /* Abu-abu gelap */
        color: white;
        border: 1px solid #333;
        border-radius: 12px;
        padding: 20px;
        font-size: 16px;
    }
    .stTextInput > div > div > input:focus {
        border-color: #4c4cff;
        box-shadow: 0 0 15px rgba(76, 76, 255, 0.2);
    }

    /* TOMBOL DOWNLOAD UTAMA (Warna Biru Neon) */
    .stButton > button {
        width: 100%;
        background-color: #4c4cff; /* Biru Neon sesuai gambar */
        color: white;
        border: none;
        padding: 15px;
        font-weight: 700;
        font-size: 16px;
        border-radius: 12px;
        transition: 0.3s;
    }
    .stButton > button:hover {
        background-color: #3b3bff;
        box-shadow: 0 0 20px rgba(76, 76, 255, 0.4);
    }

    /* RESULT CARD (Kartu Hasil Download) */
    .result-card {
        background-color: #161616;
        border: 1px solid #333;
        border-radius: 15px;
        padding: 20px;
        margin-top: 20px;
        display: flex;
        flex-direction: column;
    }

    /* Logo Text (Loader.fo style) */
    .logo-text {
        font-weight: 800;
        font-size: 24px;
        color: white;
        margin-bottom: 2rem;
    }
    .logo-accent { color: #4c4cff; }

    /* Hiding Streamlit Elements */
    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    
    </style>
""", unsafe_allow_html=True)

# --- 4. LAYOUT HEADER (LOGO) ---
col_logo, col_space = st.columns([1, 5])
with col_logo:
    st.markdown('<div class="logo-text">Rifki<span class="logo-accent">.fo</span></div>', unsafe_allow_html=True)

# --- 5. HERO SECTION (JUDUL) ---
st.markdown("<h1>YouTube Video <span style='color: #4c4cff;'>Downloader</span></h1>", unsafe_allow_html=True)
st.markdown("<p>Try this unique tool for quick downloads from YouTube, TikTok & IG.</p>", unsafe_allow_html=True)
st.write("") # Spacer

# --- 6. INPUT AREA (INPUT + BUTTON) ---
# Kita buat layout kolom biar input panjang, button kecil di kanan (opsional, atau full width)
# Di sini kita buat numpuk (stack) agar rapi di HP
url = st.text_input("", placeholder="🔗 Paste URL here...")

st.write("") # Jarak dikit

# Tombol Eksekusi
if st.button("Download Video", type="primary"):
    
    if not url:
        st.error("⚠️ Please paste a link first.")
    else:
        # --- LOGIKA DOWNLOAD ---
        tipe = detect_type(url)
        status_box = st.empty()
        
        # --- STYLE KARTU HASIL (RESULT CARD) ---
        # Kita pakai Container untuk membungkus hasil biar backgroundnya beda
        with st.container():
            st.markdown('<div style="background-color: #111; padding: 20px; border-radius: 15px; border: 1px solid #333;">', unsafe_allow_html=True)
            
            # 1. VIDEO ENGINE
            if tipe == "VIDEO":
                status_box.info("🔄 Fetching video info...")
                
                # Opsi yt-dlp
                ydl_opts = {
                    'format': 'best',
                    'outtmpl': 'temp_vid.%(ext)s',
                    'quiet': True,
                    'noplaylist': True
                }
                
                try:
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        # Ambil Info Dulu (Tanpa Download)
                        info = ydl.extract_info(url, download=False)
                        judul = info.get('title', 'Video Unknown')
                        thumbnail = info.get('thumbnail', '')
                        duration = info.get('duration_string', '0:00')
                        ext = info.get('ext', 'mp4')
                        
                        # TAMPILAN KARTU HASIL (Layout Kolom: Gambar | Teks)
                        c1, c2 = st.columns([1, 2])
                        
                        with c1:
                            if thumbnail:
                                st.image(thumbnail, use_container_width=True)
                            else:
                                st.markdown("🎬 No Preview")
                        
                        with c2:
                            st.markdown(f"<h3 style='color:white; margin:0;'>{judul}</h3>", unsafe_allow_html=True)
                            st.markdown(f"<p style='text-align:left; color:#888;'>Format: MP4 • Durasi: {duration}</p>", unsafe_allow_html=True)
                            
                        st.write("---") # Garis
                        
                        # PROSES DOWNLOAD
                        status_box.info("⬇️ Downloading to server...")
                        ydl.download([url])
                        
                        target_file = f"temp_vid.{ext}"
                        if os.path.exists(target_file):
                            status_box.success("✅ Ready!")
                            
                            # TOMBOL DOWNLOAD FINAL (BIRU FULL)
                            with open(target_file, "rb") as f:
                                st.download_button(
                                    label="Download Video Now",
                                    data=f,
                                    file_name=f"{clean_filename(judul)}.{ext}",
                                    mime=f"video/{ext}",
                                    use_container_width=True
                                )
                except Exception as e:
                    st.error(f"Error: {e}")

            # 2. FOTO ENGINE
            elif tipe == "FOTO":
                status_box.info("📸 Fetching image...")
                if os.path.exists("temp_img"): shutil.rmtree("temp_img")
                
                try:
                    L = instaloader.Instaloader(save_metadata=False, download_videos=False)
                    shortcode = url.split("/p/")[1].split("/")[0]
                    post = instaloader.Post.from_shortcode(L.context, shortcode)
                    
                    # Kolom Info Foto
                    c1, c2 = st.columns([1, 2])
                    with c1:
                        # Tampilkan foto dari URL langsung (preview)
                        st.image(post.url, use_container_width=True)
                    with c2:
                        st.markdown(f"<h3 style='color:white; margin:0;'>Instagram Photo</h3>", unsafe_allow_html=True)
                        st.markdown(f"<p style='text-align:left; color:#888;'>User: {post.owner_username}</p>", unsafe_allow_html=True)

                    st.write("---")
                    
                    # Download Real
                    L.download_post(post, target="temp_img")
                    target = None
                    for f in os.listdir("temp_img"):
                        if f.endswith(".jpg"):
                            target = os.path.join("temp_img", f)
                            break
                    
                    if target:
                        status_box.success("✅ Ready!")
                        with open(target, "rb") as f:
                            st.download_button(
                                label="Download Image Now",
                                data=f,
                                file_name=f"IG_{shortcode}.jpg",
                                mime="image/jpeg",
                                use_container_width=True
                            )
                        shutil.rmtree("temp_img")
                except Exception as e:
                    st.error(f"Failed: {e}")

            st.markdown('</div>', unsafe_allow_html=True) # Tutup container
