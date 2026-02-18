import streamlit as st
import backend
import os
import shutil

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(page_title="SaveFrom Style - Rifki Downloader", page_icon="📥", layout="wide")

# --- 2. CSS: SAVEFROM CLONE STYLE ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap');

    /* Background & Font Utama */
    .stApp {
        background-color: #FFFFFF;
        font-family: 'Roboto', sans-serif;
        color: #333;
    }

    /* HEADER MENU (NAVBAR) */
    .nav-top {
        display: flex;
        justify-content: center;
        gap: 20px;
        padding: 15px 0;
        border-bottom: 1px solid #EEEEEE;
        margin-bottom: 40px;
    }
    .nav-top a {
        text-decoration: none;
        color: #555;
        font-size: 14px;
        font-weight: 500;
    }

    /* AREA INPUT & TOMBOL (PILL SHAPE) */
    .main-container {
        max-width: 940px;
        margin: 0 auto;
        text-align: center;
    }

    /* Customizing the Streamlit Input & Button to merge them */
    div[data-testid="column"] {
        display: flex;
        align-items: center;
    }
    
    .stTextInput > div > div > input {
        border-radius: 4px 0 0 4px !important;
        border: 1px solid #00AD55 !important;
        padding: 25px !important;
        font-size: 16px !important;
    }

    .stButton > button {
        background-color: #00AD55 !important; /* Hijau SaveFrom */
        color: white !important;
        border-radius: 0 4px 4px 0 !important;
        border: 1px solid #00AD55 !important;
        padding: 24px 40px !important;
        font-weight: bold !important;
        font-size: 16px !important;
        width: 100%;
    }
    .stButton > button:hover {
        background-color: #008f45 !important;
    }

    /* TUTORIAL SECTION */
    .how-to-section {
        margin-top: 60px;
        text-align: left;
        padding: 0 20px;
    }
    .how-to-section h2 {
        color: #000;
        font-size: 28px;
        margin-bottom: 20px;
    }
    .how-to-section p {
        color: #666;
        line-height: 1.6;
    }

    /* INFO STEPS */
    .step-box {
        background: #f9f9f9;
        padding: 20px;
        border-radius: 8px;
        margin-bottom: 15px;
        border-left: 5px solid #00AD55;
    }

    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# --- 3. HEADER NAV ---
st.markdown("""
    <div class="nav-top">
        <a href="#">YouTube</a>
        <a href="#">Facebook</a>
        <a href="#">Instagram</a>
        <a href="#">TikTok</a>
        <a href="#" style="color: #00AD55;">Pasang Helper</a>
    </div>
""", unsafe_allow_html=True)

# --- 4. AREA UTAMA (INPUT) ---
st.markdown('<div class="main-container">', unsafe_allow_html=True)

# Judul Utama di bawah Nav
st.markdown("<h2 style='text-align: center; margin-bottom: 30px;'>Unduh Video dan Musik dengan Cepat</h2>", unsafe_allow_html=True)

# Layout Input + Tombol (Merapat)
# Kita pakai kolom kecil di sisi kiri/kanan sebagai margin
col_left, col_input, col_btn, col_right = st.columns([0.1, 3, 0.8, 0.1])

with col_input:
    url_input = st.text_input("", placeholder="Tempel tautan video Anda di sini", label_visibility="collapsed")

with col_btn:
    # Tombol Unduh Hijau
    dl_clicked = st.button("Unduh")

# Logika Proses
if dl_clicked:
    if url_input:
        with st.spinner("Sedang memproses tautan..."):
            info = backend.get_video_info(url_input)
            if info:
                st.session_state.video_info = info
                st.session_state.current_url = url_input
            else:
                st.error("Gagal memproses link.")
    else:
        st.warning("Masukkan URL terlebih dahulu.")

# --- 5. RESULT AREA ---
if 'video_info' in st.session_state and st.session_state.video_info:
    info = st.session_state.video_info
    
    st.write("---")
    res_col1, res_col2 = st.columns([1, 2])
    
    with res_col1:
        if info.get('thumbnail'):
            st.image(info.get('thumbnail'), use_container_width=True)
    
    with res_col2:
        st.subheader(info.get('title', 'Video Content'))
        
        # Tombol Proses Download Real
        if st.button("🚀 Klik untuk Download File"):
            with st.spinner("Mengambil file dari server..."):
                files = backend.download_video(st.session_state.current_url)
                if files:
                    st.session_state.file_list = files
                    st.rerun()
    
    # Menampilkan file-file yang sudah di-download (Mode Galeri)
    if 'file_list' in st.session_state and st.session_state.file_list:
        for i, file_path in enumerate(st.session_state.file_list):
            file_name = os.path.basename(file_path)
            with open(file_path, "rb") as f:
                st.download_button(
                    label=f"⬇️ Simpan Media #{i+1} ({file_name})",
                    data=f,
                    file_name=file_name,
                    use_container_width=True,
                    key=f"btn_{i}"
                )

# --- 6. TUTORIAL & FAQ (Persis SaveFrom) ---
st.markdown("""
    <div class="how-to-section">
        <h2>Unduh Video dengan Mudah Menggunakan Rifki Downloader</h2>
        <p>Platform pengunduh video yang terpercaya. Cukup salin URL video, tempelkan, dan klik tombol Unduh.</p>
        
        <div class="step-box">
            <strong>Langkah 1:</strong> Salin link video yang ingin Anda simpan ke perangkat.
        </div>
        <div class="step-box">
            <strong>Langkah 2:</strong> Masukkan URL yang sudah disalin ke dalam kolom di atas.
        </div>
        <div class="step-box">
            <strong>Langkah 3:</strong> Klik "Unduh" dan pilih file yang ingin disimpan.
        </div>
        
        <h2 style="margin-top:40px;">Pertanyaan yang Sering Diajukan</h2>
        <p><b>Bagaimana cara mengunduh video?</b><br>
        Gunakan kolom pencarian di halaman utama kami untuk menempelkan link dari platform populer seperti TikTok, YouTube, atau Instagram.</p>
    </div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
