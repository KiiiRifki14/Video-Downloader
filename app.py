import streamlit as st
import yt_dlp
import instaloader
import os
import shutil
import time
from pathlib import Path

st.set_page_config(page_title="Rifki Downloader", page_icon="🍃", layout="wide")

# --- CSS: dark theme, purple accents, nav tabs, preview card, controls ---
st.markdown("""
<style>
/* Page background */
.stApp {
  background: #0b0f1a;
  color: #e6eef8;
  font-family: Inter, 'Segoe UI', Roboto, Arial, sans-serif;
}

/* Top nav (tabs) */
.top-nav {
  display:flex;
  gap:12px;
  align-items:center;
  margin-bottom:18px;
}
.nav-item {
  color: rgba(255,255,255,0.85);
  padding:10px 14px;
  border-radius:10px;
  font-weight:600;
  background: transparent;
  border: 1px solid transparent;
}
.nav-item.active {
  background: linear-gradient(90deg,#6b46ff,#8b5cf6);
  box-shadow: 0 8px 30px rgba(139,92,246,0.12);
  color: #fff;
}

/* Hero area */
.hero {
  background: linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01));
  border: 1px solid rgba(255,255,255,0.03);
  padding: 26px;
  border-radius: 14px;
  margin-bottom: 18px;
}
.hero .title {
  font-size: 28px;
  font-weight: 800;
  color: #ffffff;
  margin-bottom: 6px;
}
.hero .desc {
  color: rgba(230,238,248,0.85);
  margin-bottom: 12px;
  font-size: 14px;
}

/* Warning */
.warn {
  background: rgba(255,255,255,0.02);
  border-left: 4px solid #ffb86b;
  padding: 10px 12px;
  border-radius: 8px;
  color: #ffd9b3;
  margin-bottom: 14px;
  font-weight:600;
}

/* Input row */
.input-row {
  display:flex;
  gap:12px;
  align-items:center;
  width:100%;
}
.input-box {
  flex:1;
  display:flex;
  align-items:center;
  gap:10px;
  background: rgba(255,255,255,0.02);
  padding: 10px 12px;
  border-radius: 12px;
  border: 1px solid rgba(255,255,255,0.03);
}
.input-box input {
  background: transparent;
  border: none;
  outline: none;
  color: #e6eef8;
  width:100%;
  font-size:15px;
}
.clip-icon {
  width:36px;
  height:36px;
  background: linear-gradient(90deg,#6b46ff,#8b5cf6);
  display:flex;
  align-items:center;
  justify-content:center;
  border-radius:8px;
  box-shadow: 0 8px 20px rgba(107,70,255,0.12);
}

/* Preview card */
.preview {
  display:flex;
  gap:16px;
  align-items:flex-start;
  margin-top:16px;
  background: linear-gradient(180deg, rgba(255,255,255,0.01), rgba(255,255,255,0.005));
  padding:14px;
  border-radius:12px;
  border: 1px solid rgba(255,255,255,0.03);
}
.thumb {
  width:160px;
  height:90px;
  background:#0f1724;
  border-radius:8px;
  overflow:hidden;
  flex-shrink:0;
}
.thumb img { width:100%; height:100%; object-fit:cover; display:block; }
.preview-meta { flex:1; }
.preview-title { font-weight:700; color:#fff; margin-bottom:6px; }
.preview-sub { color: rgba(230,238,248,0.75); font-size:13px; margin-bottom:8px; }

/* Format selector */
.format-row { display:flex; gap:10px; align-items:center; flex-wrap:wrap; margin-bottom:8px; }
.format-pill {
  background: rgba(255,255,255,0.02);
  padding:8px 12px;
  border-radius:999px;
  border:1px solid rgba(255,255,255,0.03);
  color:#e6eef8;
  font-weight:600;
  cursor:pointer;
}
.format-pill.selected {
  background: linear-gradient(90deg,#6b46ff,#8b5cf6);
  box-shadow: 0 8px 30px rgba(139,92,246,0.12);
  color:#fff;
}

/* Add format link */
.add-format {
  color:#9fb7ff;
  font-weight:700;
  cursor:pointer;
}

/* Download button */
.download-btn {
  background: linear-gradient(90deg,#7c3aed,#a78bfa);
  color: #fff;
  padding:12px 20px;
  border-radius:12px;
  font-weight:800;
  border:none;
  box-shadow: 0 12px 30px rgba(124,58,237,0.18);
}

/* Footer small */
.footer-note { color: rgba(230,238,248,0.55); font-size:13px; margin-top:18px; }

/* Responsive */
@media (max-width: 880px) {
  .preview { flex-direction:column; }
  .thumb { width:100%; height:180px; }
  .input-row { flex-direction:column; align-items:stretch; }
  .download-btn { width:100%; }
}
</style>
""", unsafe_allow_html=True)

# --- Top navigation (tabs) ---
st.markdown('<div class="top-nav">', unsafe_allow_html=True)
tabs = ["YouTube Video", "4k Video", "YouTube MP3", "YouTube Playlist", "YouTube WAV", "YouTube 1080p"]
# simple active on first
for i, t in enumerate(tabs):
    cls = "nav-item active" if i == 0 else "nav-item"
    st.markdown(f'<div class="{cls}">{t}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# --- Hero with title, description, and warning ---
st.markdown('<div class="hero">', unsafe_allow_html=True)
st.markdown('<div class="title">YouTube Video Downloader</div>', unsafe_allow_html=True)
st.markdown('<div class="desc">Try this unique tool for quick, hassle-free downloads from YouTube. Transform your offline video collection with this reliable and efficient downloader.</div>', unsafe_allow_html=True)
st.markdown('<div class="warn">⚡ WE DO NOT ALLOW/SUPPORT THE DOWNLOAD OF COPYRIGHTED MATERIAL</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

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
