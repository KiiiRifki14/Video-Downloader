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
.logo .highlight { color: #378CE7; } /* .fo equivalent color */

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
.nav-icon { font-size: 16px; }

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
    color: #378CE7; /* Fallback */
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

/* 3. Input Area */
.url-input-container {
    background: var(--card-bg);
    border-radius: 16px;
    padding: 8px;
    display: flex;
    align-items: center;
    gap: 10px;
    border: 1px solid #333;
    max-width: 700px;
    margin: 0 auto 3rem auto;
    box-shadow: 0 4px 20px rgba(0,0,0,0.3);
}
.link-icon-box {
    width: 40px;
    height: 40px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #888;
}
/* Streamlit text input override */
.stTextInput {
    width: 100%;
}
.stTextInput > div > div > input {
    background-color: transparent;
    color: #fff;
    border: none;
    font-size: 16px;
}
/* Focus state override */
.stTextInput > div > div > input:focus {
    box-shadow: none;
    border: none;
}
.paste-btn-wrapper {
    background: #378CE7; /* Fallback */
    background: var(--accent-gradient);
    width: 50px;
    height: 50px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    flex-shrink: 0;
}

/* 4. Result Card */
.result-card {
    background: var(--card-bg);
    border: 1px solid #333;
    border-radius: 20px;
    padding: 24px;
    display: flex;
    gap: 24px;
    align-items: flex-start;
    max-width: 700px;
    margin: 0 auto;
}
.result-thumb {
    width: 240px;
    border-radius: 12px;
    overflow: hidden;
    position: relative;
    flex-shrink: 0;
}
.result-thumb img {
    width: 100%;
    display: block;
    border-radius: 12px;
}
.result-info {
    flex: 1;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}
.video-title {
    font-size: 18px;
    font-weight: 700;
    margin-bottom: 2rem;
    line-height: 1.4;
}
.video-meta-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1rem;
    background: rgba(0,0,0,0.3);
    padding: 10px 16px;
    border-radius: 8px;
}
.format-tag {
    font-weight: 600;
    font-size: 14px;
    display: flex;
    align-items: center;
    gap: 6px;
}
.size-tag {
    color: #fff;
    font-weight: 700;
}
.add-format-link {
    color: #378CE7;
    font-size: 13px;
    text-decoration: none;
    margin-bottom: 1rem;
    display: inline-block;
    cursor: pointer;
}

/* Custom Button Styling via Styler is hard, we use st.button but inject style to target it */
div[data-testid="stButton"] button {
    width: 100%;
    background: var(--accent-gradient);
    color: white;
    border: none;
    padding: 12px 24px;
    border-radius: 12px;
    font-weight: 700;
    font-size: 16px;
    transition: 0.2s;
}
div[data-testid="stButton"] button:hover {
    opacity: 0.9;
    border: none;
    color: white;
}

/* Footer Details */
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

/* Floating Shapes (Background decoration) */
.shape {
    position: fixed;
    z-index: -1;
    opacity: 0.3;
    pointer-events: none;
}
</style>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown("""
<div class="top-header">
    <div class="logo">Loader<span>.fo</span></div>
    <div style="display:flex; gap:10px;">
        <!-- Theme toggle placeholder -->
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


# --- Input row: URL input with clipboard icon and Download button ---
col1, col2 = st.columns([3,1])
with col1:
    st.markdown('<div class="input-row">', unsafe_allow_html=True)
    # custom input container
    st.markdown('<div class="input-box">', unsafe_allow_html=True)
    st.markdown('<div class="clip-icon">📋</div>', unsafe_allow_html=True)
    url = st.text_input("", placeholder="Paste URL", key="url_input")
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
with col2:
    # primary download button (will trigger backend)
    download_click = st.button("Download", key="download_primary", help="Download selected format", args=None)

# --- Preview card (static until we fetch info) ---
# We'll show a sample preview if URL present; otherwise show placeholder
def sample_thumbnail_bytes():
    # return None to use placeholder color box
    return None

if url:
    # Try to fetch metadata via yt_dlp (lightweight extract only)
    preview_title = "Unknown video"
    preview_thumb = None
    selected_format = "MP4 1080p"
    filesize = "—"
    try:
        ydl_opts = {"quiet": True, "skip_download": True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            preview_title = info.get("title", preview_title)
            preview_thumb = info.get("thumbnail")
            # pick a best format label if available
            formats = info.get("formats", [])
            # try to find 1080p mp4
            for f in reversed(formats):
                if f.get("ext") == "mp4" and f.get("height") == 1080:
                    selected_format = "MP4 1080p"
                    filesize = f.get("filesize") or f.get("filesize_approx") or filesize
                    break
            # fallback: first mp4
            if filesize == "—":
                for f in formats:
                    if f.get("ext") == "mp4":
                        filesize = f.get("filesize") or f.get("filesize_approx") or filesize
                        selected_format = f.get("format_note") or selected_format
                        break
            # humanize filesize
            if isinstance(filesize, (int, float)):
                for unit in ['B','KB','MB','GB']:
                    if filesize < 1024:
                        filesize = f"{filesize:.1f} {unit}"
                        break
                    filesize /= 1024
    except Exception:
        preview_title = "Preview unavailable"

    # render preview
    st.markdown('<div class="preview">', unsafe_allow_html=True)
    if preview_thumb:
        st.markdown(f'<div class="thumb"><img src="{preview_thumb}" alt="thumb"></div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="thumb"></div>', unsafe_allow_html=True)
    st.markdown('<div class="preview-meta">', unsafe_allow_html=True)
    st.markdown(f'<div class="preview-title">{preview_title}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="preview-sub">Selected: <strong>{selected_format}</strong> • Size: {filesize}</div>', unsafe_allow_html=True)

    # format pills and add another format
    st.markdown('<div class="format-row">', unsafe_allow_html=True)
    formats_to_show = ["MP4 1080p", "MP4 720p", "MP4 480p", "MP3 128kbps"]
    for f in formats_to_show:
        cls = "format-pill selected" if f == selected_format else "format-pill"
        st.markdown(f'<div class="{cls}">{f}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="add-format">+ Add another format</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
else:
    # placeholder preview
    st.markdown('<div class="preview">', unsafe_allow_html=True)
    st.markdown('<div class="thumb"></div>', unsafe_allow_html=True)
    st.markdown('<div class="preview-meta">', unsafe_allow_html=True)
    st.markdown('<div class="preview-title">Paste a valid YouTube URL to see preview</div>', unsafe_allow_html=True)
    st.markdown('<div class="preview-sub">Supported formats: MP4, MP3, WAV, 4K</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- Backend download handling (triggered by button) ---
if download_click:
    if not url:
        st.warning("⚠️ Masukkan URL terlebih dahulu.")
    else:
        status = st.empty()
        progress = st.progress(0)
        status.info("Preparing download...")
        # choose default ydl options for mp4 best
        outtmpl = "temp_download.%(ext)s"
        ydl_opts = {
            "format": "bestvideo+bestaudio/best",
            "outtmpl": outtmpl,
            "quiet": True,
            "noplaylist": True,
        }
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                progress.progress(20)
                info = ydl.extract_info(url, download=True)
                progress.progress(80)
                # find downloaded file
                ext = info.get("ext", "mp4")
                filename = f"temp_download.{ext}"
                if not os.path.exists(filename):
                    # try to find any temp file
                    candidates = list(Path(".").glob("temp_download.*"))
                    filename = str(candidates[0]) if candidates else None
                if filename and os.path.exists(filename):
                    status.success("✅ Siap diunduh")
                    with open(filename, "rb") as f:
                        st.download_button(
                            label=f"⬇️ Download {info.get('title','video')}.{ext}",
                            data=f,
                            file_name=f"{info.get('title','video')}.{ext}",
                            mime=f"video/{ext}",
                            use_container_width=True
                        )
                    # cleanup optional
                    # os.remove(filename)
                else:
                    status.error("File tidak ditemukan setelah proses.")
                progress.progress(100)
        except Exception as e:
            status.error("Gagal mengunduh: " + str(e))
            progress.progress(0)

# --- Informational section (like reference) ---
st.markdown("---")
st.markdown("#### YouTube Video Downloader", unsafe_allow_html=True)
st.markdown("loader.io is one of the most popular downloader tools on the internet. With this tool, you can download and convert videos from almost anywhere on the net. Enter the page URL in the field above, choose the format, and click Download.", unsafe_allow_html=True)

# --- Footer note ---
st.markdown(f'<div class="footer-note">We are not affiliated with YouTube. Created by Rifki team - video downloading experts.</div>', unsafe_allow_html=True)
