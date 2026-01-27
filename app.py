import streamlit as st
import backend
import os
import shutil

# --- Page Config ---
st.set_page_config(page_title="Ki.downloader - Video Downloader", page_icon="🔵", layout="wide")

# --- Session State ---
if 'theme' not in st.session_state:
    st.session_state.theme = 'light'
if 'video_info' not in st.session_state:
    st.session_state.video_info = None
if 'current_url' not in st.session_state:
    st.session_state.current_url = ""

def toggle_theme():
    st.session_state.theme = 'dark' if st.session_state.theme == 'light' else 'light'

# --- Theme Variables (Tetap sama seperti punyamu) ---
themes = {
    'light': {
        'bg_color': '#ffffff', 'text_color': '#1a1a1a', 'card_bg': '#ffffff',
        'element_bg': '#f0f2f5', 'border_color': '#e1e4e8', 'subtext': '#666666',
        'accent': '#1877f2', 'accent_hover': '#145dbf'
    },
    'dark': {
        'bg_color': '#0d0d0d', 'text_color': '#ffffff', 'card_bg': '#161616',
        'element_bg': '#262626', 'border_color': '#333333', 'subtext': '#aaaaaa',
        'accent': '#1877f2', 'accent_hover': '#145dbf'
    }
}
current_theme = themes[st.session_state.theme]

# --- CSS Injection (Saya sederhanakan dikit bagian input biar ga error di layout) ---
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800&display=swap');

:root {{
  --bg-color: {current_theme['bg_color']};
  --text-color: {current_theme['text_color']};
  --card-bg: {current_theme['card_bg']};
  --element-bg: {current_theme['element_bg']};
  --border-color: {current_theme['border_color']};
  --subtext-color: {current_theme['subtext']};
  --accent-blue: {current_theme['accent']};
  --accent-blue-hover: {current_theme['accent_hover']};
}}

.stApp {{ background-color: var(--bg-color); font-family: 'Outfit', sans-serif; color: var(--text-color); }}
header {{visibility: hidden;}}
.block-container {{ padding-top: 1rem; max-width: 1000px; }}

/* Navigation & Hero */
.nav-header {{ display: flex; justify-content: space-between; align-items: center; padding: 1rem 0; margin-bottom: 2rem; }}
.logo-text {{ font-size: 24px; font-weight: 800; color: var(--text-color); }}
.logo-text span {{ color: var(--accent-blue); }}

.hero-section {{ text-align: center; padding: 3rem 0; }}
.hero-title {{ font-size: 48px; font-weight: 800; margin-bottom: 1rem; color: var(--text-color); }}
.hero-title span {{ color: var(--accent-blue); }}
.hero-desc {{ color: var(--subtext-color); max-width: 600px; margin: 0 auto 2rem auto; line-height: 1.6; }}

/* Input Area */
.input-area {{
    max-width: 700px; margin: 0 auto 3rem auto;
    display: flex; gap: 10px;
}}

/* Result Card */
.result-card {{
    background: var(--card-bg); border: 1px solid var(--border-color);
    border-radius: 16px; padding: 20px; display: flex; gap: 20px;
    max-width: 700px; margin: 0 auto; box-shadow: 0 10px 40px rgba(0,0,0,0.05);
}}
.res-thumb img {{ border-radius: 10px; width: 100%; object-fit: cover; }}
.res-title {{ font-weight: 700; font-size: 18px; margin-bottom: 8px; color: var(--text-color); }}
.res-meta {{ font-size: 13px; color: var(--subtext-color); margin-bottom: 16px; }}

/* Custom Button Styles via CSS targeting Streamlit classes is safer done inline or simplistic */
</style>
""", unsafe_allow_html=True)

# --- UI Layout ---

# 1. Header
col1, col2 = st.columns([4,1])
with col1:
    st.markdown('<div class="nav-header"><div class="logo-text">Ki<span>.downloader</span></div></div>', unsafe_allow_html=True)
with col2:
    if st.button("🌓 Theme", key="theme_toggle"):
        toggle_theme()
        st.rerun()

# 2. Hero
st.markdown("""
<div class="hero-section">
    <div class="hero-title">Video <span>Downloader</span></div>
    <div class="hero-desc">Try this unique tool for quick, hassle-free downloads.</div>
</div>
""", unsafe_allow_html=True)

# 3. Input Section (Sederhana tapi Rapi)
c1, c2 = st.columns([4, 1])
with c1:
    url_input = st.text_input("URL", placeholder="Paste YouTube link here...", label_visibility="collapsed")
with c2:
    # Logic: Reset info jika URL berubah atau tombol diklik
    if st.button("Check Video", type="primary", use_container_width=True):
        if url_input:
            st.session_state.current_url = url_input
            with st.spinner("Searching..."):
                info = backend.get_video_info(url_input)
                if info:
                    st.session_state.video_info = info
                else:
                    st.error("Video not found.")
                    st.session_state.video_info = None

# 4. Result Section
if st.session_state.video_info:
    info = st.session_state.video_info
    
    # Tampilkan Card
    st.markdown('<div class="result-card">', unsafe_allow_html=True)
    
    # Kita bagi kolom di dalam visual card menggunakan st.columns
    r_img, r_txt = st.columns([1, 1.5])
    
    with r_img:
        st.image(info.get('thumbnail', ''), use_column_width=True)
    
    with r_txt:
        st.markdown(f"### {info.get('title', 'Unknown Title')}")
        st.caption(f"Duration: {info.get('duration_string', '-')} | Ext: {info.get('ext', 'mp4')}")
        
        # --- BAGIAN PENTING: LOGIKA DOWNLOAD ---
        # Kita melakukan download di Backend, lalu membaca file ke memory, 
        # baru dimasukkan ke tombol download_button agar tombol tidak hilang saat diklik.
        
        # Tombol trigger proses
        proc_btn = st.button("Prepare Download File", key="proc_dl")
        
        if proc_btn:
            with st.spinner("Downloading from YouTube servers..."):
                file_path = backend.download_video(st.session_state.current_url)
                
                if file_path and os.path.exists(file_path):
                    # Baca file ke RAM
                    with open(file_path, "rb") as f:
                        file_data = f.read()
                    
                    # Hapus file sementara di server (Cleanup) agar storage tidak penuh
                    # (Opsional: bisa dihapus nanti, tapi amannya begini)
                    try:
                        shutil.rmtree(os.path.dirname(file_path)) 
                    except:
                        pass
                        
                    # Simpan data file di session state agar tombol download muncul
                    st.session_state.download_ready = file_data
                    st.session_state.download_name = os.path.basename(file_path)
                    st.rerun() # Refresh halaman untuk memunculkan tombol final
                else:
                    st.error("Failed to download video.")

        # Jika file sudah siap di memory, tampilkan tombol download final
        if 'download_ready' in st.session_state:
            st.download_button(
                label="⬇️ DOWNLOAD FINAL FILE",
                data=st.session_state.download_ready,
                file_name=st.session_state.download_name,
                mime="video/mp4",
                type="primary"
            )
            
            # Tombol reset
            if st.button("Download Another Video"):
                del st.session_state.download_ready
                st.session_state.video_info = None
                st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# 5. Warning & Footer (Tetap sama)
st.markdown("<br><hr>", unsafe_allow_html=True)
st.markdown("""
<div style='text-align: center; color: #666;'>
    <small>⚡ WE DO NOT ALLOW/SUPPORT THE DOWNLOAD OF COPYRIGHTED MATERIAL!</small><br>
    Ki.downloader © 2026
</div>
""", unsafe_allow_html=True)
