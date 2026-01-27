import streamlit as st
import backend
import os
import shutil

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Ki.Downloader", page_icon="⚡", layout="wide")

# --- 2. CSS PREMIUM (Sangat Rapi) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');

    /* BACKGROUND UTAMA */
    .stApp {
        background-color: #050505;
        font-family: 'Inter', sans-serif;
    }

    /* MENGHILANGKAN ELEMENT BAWAAN */
    header {visibility: hidden;}
    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}

    /* CONTAINER UTAMA (Agar tidak terlalu lebar di PC, pas di HP) */
    .block-container {
        max-width: 700px;
        padding-top: 3rem;
        padding-bottom: 5rem;
    }

    /* HEADER */
    .logo-text {
        font-size: 22px;
        font-weight: 800;
        color: white;
    }
    .logo-text span { color: #4c4cff; }

    /* BADGE PRIBADI */
    .private-badge {
        background: rgba(255, 255, 255, 0.1);
        color: #888;
        padding: 6px 12px;
        border-radius: 20px;
        font-size: 11px;
        font-weight: 600;
        border: 1px solid #333;
        display: inline-block;
    }

    /* JUDUL BESAR */
    .hero-title {
        text-align: center;
        font-size: 38px;
        font-weight: 800;
        color: white;
        margin-top: 30px;
        margin-bottom: 5px;
    }
    .hero-title span { color: #4c4cff; }
    
    .hero-desc {
        text-align: center;
        color: #666;
        font-size: 14px;
        margin-bottom: 40px;
    }

    /* INPUT BOX (Custom Style) */
    .stTextInput > div > div > input {
        background-color: #121212;
        color: white;
        border: 1px solid #333;
        border-radius: 15px;
        padding: 25px 15px;
        font-size: 16px;
        text-align: center; /* Teks input di tengah */
    }
    .stTextInput > div > div > input:focus {
        border-color: #4c4cff;
        box-shadow: 0 0 15px rgba(76, 76, 255, 0.2);
    }

    /* TOMBOL UTAMA (BIRU) */
    /* Kita targetkan tombol di dalam columns nanti */
    div[data-testid="stButton"] > button {
        background-color: #4c4cff;
        color: white;
        border: none;
        padding: 12px 24px;
        font-weight: 700;
        font-size: 16px;
        border-radius: 50px; /* Tombol bulat lonjong */
        width: 100%;
        transition: 0.2s;
        box-shadow: 0 4px 15px rgba(76, 76, 255, 0.3);
    }
    div[data-testid="stButton"] > button:hover {
        background-color: #3535ff;
        transform: scale(1.02);
    }
    
    /* CARD HASIL */
    .result-card {
        background-color: #111;
        border: 1px solid #222;
        border-radius: 20px;
        padding: 20px;
        margin-top: 30px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.3);
    }
    
    /* LOADING SPINNER CUSTOM COLOR */
    .stSpinner > div {
        border-top-color: #4c4cff !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. HEADER (Logo & Badge) ---
# Menggunakan kolom agar rapi kanan-kiri
col_h1, col_h2 = st.columns([1, 1])
with col_h1:
    st.markdown('<div class="logo-text">Ki<span>.downloader</span></div>', unsafe_allow_html=True)
with col_h2:
    st.markdown('<div style="text-align: right;"><span class="private-badge">🔒 Personal Use Only</span></div>', unsafe_allow_html=True)

# --- 4. HERO (Judul) ---
st.markdown("""
    <div class="hero-title">Video <span>Downloader</span></div>
    <div class="hero-desc">TikTok • Instagram • YouTube (No Watermark)</div>
""", unsafe_allow_html=True)

# --- 5. INPUT & BUTTON (BAGIAN PENTING) ---

# Inisialisasi State
if 'video_info' not in st.session_state: st.session_state.video_info = None
if 'current_url' not in st.session_state: st.session_state.current_url = ""

# Input Full Width
url_input = st.text_input("URL", placeholder="Paste link di sini...", label_visibility="collapsed")

st.write("") # Spasi dikit

# --- TRIK MENENGAHKAN TOMBOL ---
# Kita bagi layar jadi 3 kolom: [Kosong, TOMBOL, Kosong]
# Rasio [1, 2, 1] membuat tombol di tengah punya lebar 50% dari layar (pas di HP)
c1, c2, c3 = st.columns([1, 2, 1])

with c2: # Kita taruh tombol HANYA di kolom tengah
    cek_clicked = st.button("🔍 Cek Video Sekarang")

# Logika Tombol
if cek_clicked:
    if url_input:
        st.session_state.current_url = url_input
        st.session_state.download_ready = None 
        with st.spinner("Sedang mencari video..."):
            info = backend.get_video_info(url_input)
            if info:
                st.session_state.video_info = info
            else:
                st.error("Link tidak valid atau video tidak ditemukan.")
                st.session_state.video_info = None
    else:
        st.warning("⚠️ Link belum diisi, bos!")


# --- 6. HASIL (RESULT CARD) ---
if st.session_state.video_info:
    info = st.session_state.video_info
    
    st.markdown('<div class="result-card">', unsafe_allow_html=True)
    
    # Layout Thumbnail & Info
    c_img, c_txt = st.columns([1, 2])
    
    with c_img:
        if info.get('thumbnail'):
            st.image(info.get('thumbnail'), use_container_width=True)
        else:
            st.markdown("🎬 No Preview")
            
    with c_txt:
        st.markdown(f"<h4 style='color:white; margin:0;'>{info.get('title', 'Video')}</h4>", unsafe_allow_html=True)
        st.markdown(f"<p style='color:#666; font-size:12px; margin-bottom:15px;'>Durasi: {info.get('duration_string', '-')} | Format: MP4</p>", unsafe_allow_html=True)
        
        # LOGIKA DOWNLOAD
        # Tombol Proses juga kita buat Full Width di dalam card
        if st.button("⚡ Download File", key="proc_dl", use_container_width=True):
            with st.spinner("Downloading..."):
                file_path = backend.download_video(st.session_state.current_url)
                
                if file_path and os.path.exists(file_path):
                    with open(file_path, "rb") as f:
                        file_data = f.read()
                    try: shutil.rmtree(os.path.dirname(file_path)) 
                    except: pass
                    
                    st.session_state.download_ready = file_data
                    st.session_state.download_name = os.path.basename(file_path)
                    st.rerun()
                else:
                    st.error("Gagal download.")

        # TOMBOL FINAL (MUNCUL SETELAH PROSES)
        if 'download_ready' in st.session_state and st.session_state.download_ready:
            st.write("") # Spasi
            st.success("Selesai! Klik tombol di bawah:")
            st.download_button(
                label="⬇️ SIMPAN KE GALERI",
                data=st.session_state.download_ready,
                file_name=st.session_state.download_name,
                mime="video/mp4",
                type="primary",
                use_container_width=True
            )

    st.markdown('</div>', unsafe_allow_html=True)

# --- 7. FOOTER ---
st.markdown("""
    <div style="text-align: center; margin-top: 60px; color: #333; font-size: 12px;">
    Ki.Downloader © 2026 • Private Tool
    </div>
""", unsafe_allow_html=True)
