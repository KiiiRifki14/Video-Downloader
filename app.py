import streamlit as st
import backend
import os
import shutil

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Ki.Downloader", page_icon="⚡", layout="wide")

# --- 2. CSS SUPER CLEAN (DARK BLUE THEME) ---
st.markdown("""
    <style>
    /* IMPORT FONT KEREN */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');

    /* BASE SETTINGS */
    .stApp {
        background-color: #050505; /* Hitam Pekat */
        font-family: 'Inter', sans-serif;
    }
    
    /* MENGHILANGKAN ELEMENT BAWAAN */
    header {visibility: hidden;}
    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    
    /* CONTAINER TENGAH (Supaya rapi di HP dan Laptop) */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 5rem;
        max-width: 800px;
    }

    /* HEADER & LOGO */
    .logo-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 3rem;
    }
    .logo-text {
        font-size: 24px;
        font-weight: 800;
        color: white;
        letter-spacing: -1px;
    }
    .logo-text span { color: #4c4cff; } /* Biru Neon */

    /* STATUS PRIBADI (BADGE) */
    .private-badge {
        background-color: #1a1a1a;
        color: #888;
        padding: 5px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
        border: 1px solid #333;
    }

    /* JUDUL BESAR */
    .hero-title {
        text-align: center;
        font-size: 42px;
        font-weight: 800;
        color: white;
        line-height: 1.2;
        margin-bottom: 10px;
    }
    .hero-title span { color: #4c4cff; }
    
    .hero-subtitle {
        text-align: center;
        color: #666;
        font-size: 14px;
        margin-bottom: 2rem;
    }

    /* INPUT BOX YANG RAPI */
    .stTextInput > div > div > input {
        background-color: #161616;
        color: white;
        border: 1px solid #333;
        border-radius: 12px;
        padding: 25px 20px; /* Padding besar biar enak ditekan */
        font-size: 16px;
        text-align: center;
    }
    .stTextInput > div > div > input:focus {
        border-color: #4c4cff;
        box-shadow: 0 0 15px rgba(76, 76, 255, 0.3);
    }

    /* TOMBOL UTAMA (BIRU) */
    div[data-testid="stButton"] > button {
        width: 100%;
        background-color: #4c4cff;
        color: white;
        border: none;
        padding: 15px;
        font-weight: 700;
        font-size: 16px;
        border-radius: 12px;
        margin-top: 10px;
        transition: 0.2s;
    }
    div[data-testid="stButton"] > button:hover {
        background-color: #3535ff;
        box-shadow: 0 5px 20px rgba(76, 76, 255, 0.4);
    }
    
    /* TOMBOL DOWNLOAD FINAL (HIJAU/BIRU MUDA) */
    .download-btn-container {
        margin-top: 20px;
        text-align: center;
    }

    /* HASIL KARTU (RESULT CARD) */
    .result-card {
        background-color: #111;
        border: 1px solid #333;
        border-radius: 16px;
        padding: 20px;
        margin-top: 30px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.5);
    }
    .info-title {
        color: white; font-weight: 700; font-size: 18px; margin-bottom: 5px;
    }
    .info-meta {
        color: #888; font-size: 13px; margin-bottom: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. HEADER (Logo & Badge Pribadi) ---
# Menggunakan kolom agar logo di kiri, badge di kanan
col_head1, col_head2 = st.columns([1, 1])
with col_head1:
    st.markdown('<div class="logo-text">Ki<span>.downloader</span></div>', unsafe_allow_html=True)
with col_head2:
    st.markdown('<div style="text-align:right;"><span class="private-badge">🔒 Personal Use Only</span></div>', unsafe_allow_html=True)

st.write("") # Spasi
st.write("")

# --- 4. HERO SECTION (Judul) ---
st.markdown("""
    <div class="hero-title">Video <span>Downloader</span></div>
    <div class="hero-subtitle">Alat download pribadi. Tanpa iklan, tanpa watermark, cepat.</div>
""", unsafe_allow_html=True)

# --- 5. LOGIC & INPUT ---
# Session State Inisialisasi
if 'video_info' not in st.session_state: st.session_state.video_info = None
if 'current_url' not in st.session_state: st.session_state.current_url = ""

# Input URL
url_input = st.text_input("Link", placeholder="Paste link YouTube/TikTok/IG disini...", label_visibility="collapsed")

# Tombol Cek
if st.button("🔍 Cek Video"):
    if url_input:
        st.session_state.current_url = url_input
        st.session_state.download_ready = None # Reset download sebelumnya
        with st.spinner("Sedang mencari video..."):
            info = backend.get_video_info(url_input)
            if info:
                st.session_state.video_info = info
            else:
                st.error("Video tidak ditemukan atau link salah.")
                st.session_state.video_info = None

# --- 6. HASIL & DOWNLOAD ---
if st.session_state.video_info:
    info = st.session_state.video_info
    
    # Tampilan Kartu Hasil
    st.markdown('<div class="result-card">', unsafe_allow_html=True)
    
    # Layout Gambar & Teks
    c_img, c_txt = st.columns([1, 2])
    with c_img:
        st.image(info.get('thumbnail', ''), use_container_width=True)
    
    with c_txt:
        st.markdown(f'<div class="info-title">{info.get("title", "Video Title")}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="info-meta">Duration: {info.get("duration_string", "-")} • Ext: {info.get("ext", "mp4")}</div>', unsafe_allow_html=True)
        
        # LOGIKA DOWNLOAD (PERSIS YANG KITA PERBAIKI TADI)
        process_btn = st.button("⚡ Proses Download File", key="process_btn")
        
        if process_btn:
            with st.spinner("Mengunduh dari server..."):
                file_path = backend.download_video(st.session_state.current_url)
                
                if file_path and os.path.exists(file_path):
                    with open(file_path, "rb") as f:
                        file_data = f.read()
                    
                    # Bersihkan file server
                    try: shutil.rmtree(os.path.dirname(file_path)) 
                    except: pass
                        
                    # Simpan ke session agar tombol muncul
                    st.session_state.download_ready = file_data
                    st.session_state.download_name = os.path.basename(file_path)
                    st.rerun()
                else:
                    st.error("Gagal mendownload.")

        # JIKA FILE SUDAH SIAP, MUNCULKAN TOMBOL FINAL
        if 'download_ready' in st.session_state and st.session_state.download_ready:
            st.success("File siap! Klik tombol di bawah.")
            st.download_button(
                label="⬇️ SIMPAN KE GALERI",
                data=st.session_state.download_ready,
                file_name=st.session_state.download_name,
                mime="video/mp4",
                type="primary"
            )

    st.markdown('</div>', unsafe_allow_html=True)

# --- 7. FOOTER PRIBADI ---
st.markdown("""
    <div style="text-align: center; margin-top: 50px; color: #444; font-size: 12px;">
    Milik Rifki • Dibuat dengan Python
    </div>
""", unsafe_allow_html=True)
