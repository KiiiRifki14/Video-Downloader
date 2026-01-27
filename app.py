import streamlit as st
import yt_dlp
import instaloader
import os
import shutil
import time
from pathlib import Path

st.set_page_config(page_title="Rifki Downloader", page_icon="🍃", layout="wide")

# --- CSS: Loader.fo inspired (Dark, Purple/Blue Gradient, Rounded) ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800&display=swap');

/* Global Variables */
:root {
  --bg-color: #0d0d0d;
  --card-bg: #161616;
  --accent-gradient: linear-gradient(90deg, #5356FF 0%, #378CE7 100%);
  --accent-color: #5356FF;
  --text-main: #ffffff;
  --text-muted: #888888;
}

/* Page Reset */
.stApp {
  background-color: var(--bg-color);
  font-family: 'Outfit', sans-serif;
  color: var(--text-main);
}
header {visibility: hidden;}
.block-container {
    padding-top: 2rem;
    padding-bottom: 5rem;
    max-width: 900px;
}

/* 1. Header / Top Bar */
.top-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 2rem;
}
.logo {
    font-size: 24px;
    font-weight: 800;
    color: #fff;
    display: flex;
    align-items: center;
    gap: 8px;
}
.logo span { color: #fff; }
.logo .highlight { color: #378CE7; } 

/* Nav Icons Bar (Horizontal) */
.nav-bar {
    display: flex;
    gap: 8px;
    background: transparent;
    overflow-x: auto;
    padding-bottom: 10px;
    margin-bottom: 3rem;
    justify-content: center;
}
.nav-item {
    display: flex;
    align-items: center;
    gap: 6px;
    background: transparent;
    padding: 8px 16px;
    border-radius: 8px;
    font-size: 13px;
    font-weight: 500;
    color: var(--text-muted);
    cursor: pointer;
    transition: 0.3s;
    border: 1px solid transparent;
}
.nav-item.active {
    background: transparent;
    color: #fff;
    border-bottom: 2px solid var(--accent-color);
    border-radius: 0;
}
.nav-item:hover {
    color: #fff;
}

/* 2. Hero Section */
.hero-container {
    text-align: center;
    margin-bottom: 3rem;
}
.hero-title {
    font-size: 48px;
    font-weight: 700;
    margin-bottom: 0.5rem;
    line-height: 1.2;
}
.hero-title span {
    background: var(--accent-gradient);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.hero-subtitle {
    font-size: 15px;
    color: var(--text-muted);
    max-width: 600px;
    margin: 0 auto 20px auto;
    line-height: 1.5;
}
.copyright-pill {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: rgba(255, 255, 255, 0.05);
    padding: 8px 16px;
    border-radius: 99px;
    font-size: 11px;
    color: #a0a0a0;
    font-weight: 600;
    border: 1px solid rgba(255,255,255,0.05);
}

/* 3. Input Styling - Target Streamlit Widget directly for the 'Box' look */
div[data-testid="stTextInput"] {
    background-color: var(--card-bg) !important;
    border: 1px solid #333 !important;
    border-radius: 14px !important;
    padding: 2px 10px !important;
    transition: 0.3s;
}
div[data-testid="stTextInput"]:focus-within {
    border-color: var(--accent-color) !important;
    box-shadow: 0 0 15px rgba(83, 86, 255, 0.2);
}
div[data-testid="stTextInput"] > div {
    background-color: transparent !important;
    border: none !important;
    color: white !important;
}
div[data-testid="stTextInput"] input {
    color: white !important;
    font-size: 15px;
}

/* Custom 'Go' Button Styling */
div[data-testid="stButton"] button {
    background: var(--accent-gradient);
    color: white;
    border: none;
    padding: 10px 24px;
    border-radius: 12px;
    font-weight: 700;
    font-size: 14px;
    margin-top: 2px; /* Alignment fix */
    width: 100%;
}
div[data-testid="stButton"] button:hover {
    border-color: transparent !important;
    color: white !important;
    opacity: 0.9;
}

/* 4. Result Card */
.result-card {
    background: var(--card-bg);
    border: 1px solid #333;
    border-radius: 20px;
    padding: 24px;
    margin-top: 2rem;
}
/* Flex is hard with Streamlit columns, we rely on layout but style the contents */
.result-thumb img {
    border-radius: 12px;
    display: block;
    width: 100%;
}
.video-title {
    font-size: 18px;
    font-weight: 700;
    margin-bottom: 1rem;
    line-height: 1.4;
    color: #fff;
}
.video-meta-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: rgba(0,0,0,0.3);
    padding: 10px 16px;
    border-radius: 8px;
    margin-bottom: 1rem;
}
.format-tag {
    font-weight: 600;
    font-size: 14px;
    display: flex;
    align-items: center;
    gap: 6px;
    color: #fff;
}
.size-tag {
    color: #fff;
    font-weight: 700;
}
.add-format-link {
    color: #378CE7;
    font-size: 13px;
    cursor: pointer;
    margin-bottom: 1rem;
    display: block;
}

/* Footer */
.footer-details {
    margin-top: 5rem;
    color: var(--text-muted);
}
.footer-details h3 {
    color: #fff;
    font-size: 20px;
    margin-bottom: 1rem;
}
.footer-details p {
    font-size: 14px;
    line-height: 1.6;
}
</style>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown("""
<div class="top-header">
    <div class="logo">Loader<span>.fo</span></div>
    <div style="display:flex; gap:10px;">
        <span style="font-size:18px;">🌙</span>
    </div>
</div>
""", unsafe_allow_html=True)

# --- Nav Tabs (Visual Only) ---
st.markdown("""
<div class="nav-bar">
    <div class="nav-item active">📺 YouTube Video Downloader</div>
    <div class="nav-item">🎞️ 4k Video Downloader</div>
    <div class="nav-item">🎵 YouTube to MP3</div>
    <div class="nav-item">📜 YouTube Playlist</div>
    <div class="nav-item">🎼 YouTube to Wav</div>
</div>
""", unsafe_allow_html=True)

# --- Hero ---
st.markdown("""
<div class="hero-container">
    <div class="hero-title">YouTube Video<br><span>Downloader</span></div>
    <div class="hero-subtitle">
        Try this unique tool for quick, hassle-free downloads from YouTube. 
        Transform your offline video collection with this reliable and efficient downloader.
    </div>
    <div class="copyright-pill">
        ⚡ WE DO NOT ALLOW/SUPPORT THE DOWNLOAD OF COPYRIGHTED MATERIAL!
    </div>
</div>
""", unsafe_allow_html=True)

# --- Input Area ---
# Styled using CSS targeting stTextInput and stButton
c_input, c_btn = st.columns([4, 1])
with c_input:
    # Emoji used as icon prefix in placeholder/label not easy, 
    # relying on the CSS style of the container to look 'premium'
    url = st.text_input("", placeholder="🔗  Paste URL here...", label_visibility="collapsed")

with c_btn:
    check_click = st.button("Download")

# --- Logic & Result Area ---
if url:
    st.markdown('<div class="result-card">', unsafe_allow_html=True)
    c_thumb, c_info = st.columns([1.2, 2])
    
    # 1. Fetch Info
    info = None
    preview_title = "Loading..."
    preview_thumb = ""
    selected_format_label = "MP4 1080p" # Fallback
    file_size_str = "Calculating..."
    
    try:
        ydl_opts = {"quiet": True, "skip_download": True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # lightweight fetch
            info = ydl.extract_info(url, download=False)
            preview_title = info.get("title", "Unknown Video")
            preview_thumb = info.get("thumbnail", "")
            
            # Find best format details
            formats = info.get("formats", [])
            # Priority: MP4 1080p -> MP4 720p -> Best MP4
            best = None
            for f in reversed(formats):
                if f.get("ext") == "mp4" and f.get("height", 0) >= 1080:
                    best = f
                    selected_format_label = "MP4 1080p"
                    break
            if not best:
                for f in reversed(formats):
                     if f.get("ext") == "mp4":
                        best = f
                        selected_format_label = "MP4 Auto"
                        break
            
            if best:
                val = best.get('filesize') or best.get('filesize_approx') or 0
                if val > 0:
                    file_size_str = f"{val/1024/1024:.1f} MB"
                else:
                    file_size_str = "~ MB"
            
    except Exception as e:
        preview_title = "Video not found or unavailable"
        st.error(f"Error fetching video: {e}")

    # 2. Render Card Content
    with c_thumb:
        img_src = preview_thumb if preview_thumb else 'https://via.placeholder.com/320x180?text=No+Thumbnail'
        st.markdown(f'<div class="result-thumb"><img src="{img_src}"></div>', unsafe_allow_html=True)
        
    with c_info:
        st.markdown(f'<div class="video-title">{preview_title}</div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="video-meta-row">
            <div class="format-tag"><span style="color:#5356FF;">📹</span> {selected_format_label}</div>
            <div class="size-tag">{file_size_str}</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="add-format-link">+ Add another format</div>', unsafe_allow_html=True)
        
        # Download Logic
        if st.button("Start Download", key="dl_real"):
            if info:
                with st.spinner("Processing..."):
                     try:
                        outtmpl = "downloaded_video.%(ext)s"
                        ydl_download_opts = {
                            "format": "bestvideo+bestaudio/best",
                            "outtmpl": outtmpl,
                            "quiet": True,
                            "noplaylist": True,
                        }
                        with yt_dlp.YoutubeDL(ydl_download_opts) as ydl_d:
                            ydl_d.download([url])
                        
                        # Find output
                        candidates = list(Path(".").glob("downloaded_video.*"))
                        if candidates:
                            final_file = str(candidates[0])
                            with open(final_file, "rb") as f:
                                st.download_button(
                                    label="⬇️ Save to Device",
                                    data=f,
                                    file_name=final_file,
                                    mime="video/mp4",
                                    use_container_width=True
                                )
                            st.success("Download Ready!")
                        else:
                            st.error("File download failed.")
                     except Exception as e:
                        st.error(f"Download Error: {e}")

    st.markdown('</div>', unsafe_allow_html=True) # End Card

# --- Footer ---
st.markdown("""
<br><br><br>
<div class="footer-details">
    <h3>YouTube Video Downloader</h3>
    <p>
        loader.fo is one of the most popular downloader tools on the internet. <br>
        With this tool, you can download and convert videos from almost anywhere on the internet.
    </p>
    <br>
    <div class="nav-bar" style="justify-content: flex-start; margin-bottom:0;">
       <span style="opacity:0.5; font-size:12px;">© 2026 Loader.fo Clone</span>
    </div>
</div>
""", unsafe_allow_html=True)
