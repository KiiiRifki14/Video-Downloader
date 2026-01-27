import streamlit as st
import yt_dlp
import instaloader
import os
import shutil
import time

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Rifki Downloader", page_icon="🍃", layout="wide")

# --- 2. CSS CUSTOM (THEME: GREEN & REFERENCE LAYOUT) ---
st.markdown("""
    <style>
    /* Background Halaman Utama (Putih Bersih seperti web modern) */
    .stApp {
        background-color: #FDFEF8;
        font-family: 'Segoe UI', sans-serif;
    }

    /* KOTAK UTAMA (HERO SECTION) - Menggantikan Kotak Ungu di referensi */
    .hero-container {
        background-color: #31694E; /* Hijau Hutan (Gantiin Ungu) */
        padding: 4rem 2rem;
        border-radius: 20px;
        text-align: center;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 10px 25px rgba(49, 105, 78, 0.3);
    }

    /* Judul di dalam Kotak Hijau */
    .hero-title {
        font-size: 3rem;
        font-weight: 800;
        margin-bottom: 10px;
        color: #F0E491; /* Cream Kuning */
    }
    
    .hero-subtitle {
        font-size: 1.2rem;
        margin-bottom: 30px;
        color: #E8F5E9;
    }

    /* INPUT BOX CUSTOM */
    /* Kita hack style input box Streamlit biar mirip referensi */
    .stTextInput > div > div > input {
        padding: 20px;
        border-radius: 10px;
        border: none;
        font-size: 18px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }

    /* TOMBOL DOWNLOAD (Mirip tombol di sebelah input) */
    .stButton > button {
        background-color: #F0E491; /* Kuning Cream */
        color: #31694E; /* Teks Hijau Tua */
        font-weight: bold;
        font-size: 18px;
        padding: 15px 30px;
        border-radius: 10px;
        border: none;
        width: 100%;
        transition: 0.3s;
    }
    .stButton > button:hover {
        background-color: #ffffff;
        transform: scale(1.02);
    }

    /* BAGIAN TUTORIAL (Langkah-langkah) */
    .tutorial-header {
        text-align: center;
        color: #31694E;
        font-weight: bold;
        font-size: 1.5rem;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    
    /* Kartu Langkah (Step Cards) */
    .step-card {
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #BBC863;
        height: 100%;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
    }
    .step-number {
        font-size: 3rem;
        font-weight: 900;
        color: #E0E0E0; /* Abu-abu pudar */
        line-height: 1;
    }
    .step-title {
        font-weight: bold;
        font-size: 1.2rem;
        color: #31694E;
        margin-bottom: 10px;
    }
    .step-desc {
        font-size: 0.9rem;
        color: #555;
    }

    /* Menghilangkan elemen bawaan */
    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    .block-container {padding-top: 1rem;}
    </style>
""", unsafe_allow_html=True)

# --- 3. LAYOUT UTAMA (HERO SECTION) ---
# Membuat kotak hijau besar
st.markdown('<div class="hero-container">', unsafe_allow_html=True)
st.markdown('<div class="hero-title">Rifki Downloader</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-subtitle">Download video TikTok, Instagram, & YouTube Tanpa Watermark (Gratis)</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Layout Input di tengah (Kita pakai kolom biar rapih di tengah layarnya)
col_spacer1, col_main, col_spacer2 = st.columns([1, 2, 1])

with col_main:
    # INPUT LINK
    url = st.text_input("", placeholder="Tempel tautan video di sini...")
    
    # TOMBOL DOWNLOAD
    # Kita taruh tombol agak berjarak
    st.write("")
    process_btn = st.button("DOWNLOAD SEKARANG ⬇️", use_container_width=True)


# --- 4. LOGIKA DOWNLOAD (Backend) ---
if process_btn:
    if not url:
        st.warning("⚠️ Harap masukkan link video terlebih dahulu!")
    else:
        # Deteksi Tipe
        tipe = "VIDEO"
        if "instagram.com/p/" in url:
            tipe = "FOTO"

        # Tampilkan Loading
        status_box = st.empty()
        progress_bar = st.progress(0)
        
        # --- LOGIKA VIDEO ---
        if tipe == "VIDEO":
            status_box.info("⏳ Sedang memproses video...")
            
            # Fungsi Bersih Nama File
            def clean_name(t): return "".join([c for c in t if c.isalnum() or c==' ']).rstrip()

            ydl_opts = {'format': 'best', 'outtmpl': 'temp_vid.%(ext)s', 'quiet': True}
            
            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    progress_bar.progress(30)
                    info = ydl.extract_info(url, download=True)
                    judul = clean_name(info.get('title', 'Video Result'))
                    ext = info.get('ext', 'mp4')
                    progress_bar.progress(100)
                
                if os.path.exists(f"temp_vid.{ext}"):
                    status_box.success("✅ Video Siap!")
                    # Tombol Simpan
                    with open(f"temp_vid.{ext}", "rb") as f:
                        st.download_button(
                            label=f"⬇️ SIMPAN VIDEO ({ext.upper()})",
                            data=f,
                            file_name=f"{judul}.{ext}",
                            mime=f"video/{ext}",
                            use_container_width=True
                        )
            except Exception as e:
                status_box.error(f"Gagal: {e}")

        # --- LOGIKA FOTO ---
        elif tipe == "FOTO":
            status_box.info("📸 Mengambil foto...")
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
                    status_box.success("✅ Foto Siap!")
                    with open(target, "rb") as f:
                        st.download_button(
                            label="⬇️ SIMPAN FOTO",
                            data=f,
                            file_name=f"IG_{shortcode}.jpg",
                            mime="image/jpeg",
                            use_container_width=True
                        )
                    shutil.rmtree("temp_img")
                else:
                    status_box.error("Foto tidak ditemukan.")
            except:
                status_box.error("Gagal. Pastikan akun publik.")


# --- 5. BAGIAN TUTORIAL (LAYOUT SEPERTI REFERENSI) ---
st.write("---") # Garis pemisah
st.markdown('<div class="tutorial-header">Cara Download Video TikTok/IG/YT:</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="step-card">
        <div class="step-number">1</div>
        <div class="step-title">Temukan Video</div>
        <div class="step-desc">
            Buka aplikasi TikTok, Instagram, atau YouTube di HP kamu. Cari video yang ingin kamu simpan.
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="step-card">
        <div class="step-number">2</div>
        <div class="step-title">Salin Tautan</div>
        <div class="step-desc">
            Ketuk tombol <b>Bagikan (Share)</b>, lalu pilih menu <b>Salin Tautan (Copy Link)</b>.
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="step-card">
        <div class="step-number">3</div>
        <div class="step-title">Download</div>
        <div class="step-desc">
            Tempel link di kolom bagian atas situs ini, lalu klik tombol <b>Download Sekarang</b>.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
