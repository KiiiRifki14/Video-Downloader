import streamlit as st
import backend
import os
import shutil

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Ki.Downloader", page_icon="⚡", layout="wide")

# --- 2. CSS SUPER UPDATE (Input Gede & Tombol Tengah) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');

    /* BASE SETTINGS */
    .stApp {
        background-color: #050505;
        font-family: 'Inter', sans-serif;
    }
    header, footer, #MainMenu {visibility: hidden;}

    /* CONTAINER UTAMA (Focus Mode) */
    .block-container {
        max-width: 600px; /* Dipersempit biar fokus di tengah HP */
        padding-top: 2rem;
        padding-bottom: 5rem;
    }

    /* HEADER */
    .logo-text { font-size: 20px; font-weight: 800; color: white; }
    .logo-text span { color: #4c4cff; }
    .private-badge {
        background: #111; color: #666; padding: 4px 10px;
        border-radius: 20px; font-size: 10px; border: 1px solid #222;
    }

    /* JUDUL */
    .hero-title {
        text-align: center; font-size: 32px; font-weight: 800;
        color: white; margin-top: 40px; margin-bottom: 5px;
    }
    .hero-title span { color: #4c4cff; }
    .hero-desc { text-align: center; color: #666; font-size: 13px; margin-bottom: 40px; }

    /* --- UPDATE: INPUT BOX JADI LEBIH GEDE --- */
    .stTextInput > div > div > input {
        background-color: #121212;
        color: white;
        border: 2px solid #222; /* Border ditebalkan dikit */
        border-radius: 25px; /* Lebih bulat (Pill Shape) */
        font-size: 18px; /* Huruf lebih besar */
        text-align: center;
        transition: all 0.3s;
    }
    .stTextInput > div > div > input:focus {
        border-color: #4c4cff;
        box-shadow: 0 0 20px rgba(76, 76, 255, 0.4);
        background-color: #1a1a1a;
    }

    /* --- UPDATE: TOMBOL --- */
    /* Kita atur tombol biar efeknya 'nendang' */
    div[data-testid="stButton"] > button {
        background: linear-gradient(90deg, #4c4cff 0%, #3535ff 100%);
        color: white;
        border: none;
        padding: 15px 0px;
        font-weight: 800;
        font-size: 16px;
        border-radius: 50px;
        box-shadow: 0 10px 30px rgba(76, 76, 255, 0.2);
        transition: 0.3s;
    }
    div[data-testid="stButton"] > button:hover {
        transform: scale(1.05);
        box-shadow: 0 15px 40px rgba(76, 76, 255, 0.4);
    }
    
    /* RESULT CARD */
    .result-card {
        background-color: #111; border: 1px solid #222;
        border-radius: 20px; padding: 25px; margin-top: 30px;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. HEADER ---
c1, c2 = st.columns([1, 1])
with c1: st.markdown('<div class="logo-text">Ki<span>.downloader</span></div>', unsafe_allow_html=True)
with c2: st.markdown('<div style="text-align:right"><span class="private-badge">🔒 Personal Only</span></div>', unsafe_allow_html=True)

# --- 4. HERO ---
st.markdown("""
    <div class="hero-title">Video <span>Downloader</span></div>
    <div class="hero-desc">Download Video TikTok • Instagram • YouTube (HD)</div>
""", unsafe_allow_html=True)

# --- 5. INPUT AREA (YANG DIPERBESAR) ---
if 'video_info' not in st.session_state: st.session_state.video_info = None
if 'current_url' not in st.session_state: st.session_state.current_url = ""

# Input Link
url_input = st.text_input("URL", placeholder="Tempel Link Video Disini...", label_visibility="collapsed")

st.write("") # Jarak Spasi

# --- 6. TOMBOL (LOGIKA TENGAH MENGGUNAKAN COLUMNS) ---
# Trik: Kita pakai 3 kolom. [Kosong - TOMBOL - Kosong]
# Rasio [0.5, 2, 0.5] artinya tombol akan mengambil porsi terbesar di tengah.
col_left, col_center, col_right = st.columns([0.2, 2, 0.2])

with col_center:
    # use_container_width=True adalah KUNCI agar tombol memenuhi kolom tengah
    cek_clicked = st.button("🔍 CEK VIDEO SEKARANG", use_container_width=True)

# Logika Tombol
if cek_clicked:
    if url_input:
        st.session_state.current_url = url_input
        st.session_state.download_ready = None 
        with st.spinner("Sedang mencari di server..."):
            info = backend.get_video_info(url_input)
            if info:
                st.session_state.video_info = info
            else:
                st.error("❌ Video tidak ditemukan!")
                st.session_state.video_info = None
    else:
        st.warning("⚠️ Masukkan link dulu, Bos!")

# --- 7. HASIL (RESULT) ---
if st.session_state.video_info:
    info = st.session_state.video_info
    
    st.markdown('<div class="result-card">', unsafe_allow_html=True)
    
    # Kolom Gambar & Info
    c_img, c_info = st.columns([1, 2])
    with c_img:
        if info.get('thumbnail'):
            st.image(info.get('thumbnail'), use_container_width=True)
    
    with c_info:
        st.markdown(f"<h4 style='color:white; margin:0 0 10px 0;'>{info.get('title', 'Video')}</h4>", unsafe_allow_html=True)
        st.markdown(f"<p style='color:#888; font-size:12px;'>Durasi: {info.get('duration_string','-')} | Format: MP4</p>", unsafe_allow_html=True)
        
        # Tombol Download File (Juga Full Width di kolom ini)
        if st.button("⚡ DOWNLOAD FILE", key="dl_proc", use_container_width=True):
            with st.spinner("Mengunduh..."):
                file_path = backend.download_video(st.session_state.current_url)
                if file_path and os.path.exists(file_path):
                    with open(file_path, "rb") as f: file_data = f.read()
                    try: shutil.rmtree(os.path.dirname(file_path)) 
                    except: pass
                    st.session_state.download_ready = file_data
                    st.session_state.download_name = os.path.basename(file_path)
                    st.rerun()
                else:
                    st.error("Gagal.")

        # Tombol Final Save
        if 'download_ready' in st.session_state and st.session_state.download_ready:
            st.write("")
            st.success("Selesai! Simpan sekarang:")
            st.download_button(
                label="⬇️ SIMPAN KE GALERI HP",
                data=st.session_state.download_ready,
                file_name=st.session_state.download_name,
                mime="video/mp4",
                type="primary",
                use_container_width=True
            )

    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("<div style='text-align:center; margin-top:50px; color:#333; font-size:12px;'>Ki.Downloader © 2026</div>", unsafe_allow_html=True)

