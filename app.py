import streamlit as st
import yt_dlp
import instaloader
import os
import shutil
import requests
from streamlit_lottie import st_lottie

# --- PAGE CONFIG ---
st.set_page_config(page_title="Rifki Downloader", page_icon="🌿", layout="centered")

# --- HELPERS ---
def load_lottieurl(url):
    try:
        r = requests.get(url, timeout=6)
        if r.status_code != 200:
            return None
        return r.json()
    except Exception:
        return None

def clean_filename(title):
    return "".join([c for c in title if c.isalpha() or c.isdigit() or c in (' ', '-', '_')]).strip()

def detect_type(url):
    if "instagram.com/p/" in url:
        return "FOTO"
    return "VIDEO"

def safe_remove(path):
    try:
        if os.path.isdir(path):
            shutil.rmtree(path)
        elif os.path.exists(path):
            os.remove(path)
    except Exception:
        pass

# --- STYLES ---
st.markdown(
    """
    <style>
    :root{
        --bg-light: #f5f7f8;
        --card: rgba(255,255,255,0.95);
        --muted: #6b7280;
        --accent: #0f9d9a;
        --accent-2: #7fc6a4;
        --glass-border: rgba(15,23,36,0.06);
        --dark-bg: #0b1220;
        --dark-card: rgba(18,24,32,0.85);
        --dark-muted: #9aa6b2;
    }
    .stApp {
        background: linear-gradient(180deg, var(--bg-light) 0%, #eef7f6 100%);
        font-family: Inter, "Segoe UI", system-ui, -apple-system, "Helvetica Neue", Arial;
    }
    .block-container {
        max-width: 880px;
        margin: 2rem auto;
        padding: 2rem;
        border-radius: 14px;
        background: var(--card);
        box-shadow: 0 10px 30px rgba(12, 20, 30, 0.06);
        border: 1px solid var(--glass-border);
    }
    .header-row { display:flex; align-items:center; gap:14px; justify-content:center; margin-bottom:6px; }
    h1 { color: var(--accent); margin:0; font-weight:700; letter-spacing:-0.6px; }
    p.lead { color: var(--muted); margin-top:6px; margin-bottom:18px; text-align:center; }
    .stTextInput > div > div > input {
        border-radius: 10px; padding:12px 14px; border:1px solid rgba(15,23,36,0.06);
    }
    .stButton > button {
        width:100%; border-radius:10px; padding:11px 14px; font-weight:600;
        background: linear-gradient(90deg, var(--accent), var(--accent-2)); color:white; border:none;
        box-shadow: 0 8px 20px rgba(15,157,154,0.08);
    }
    .stButton > button:hover { transform: translateY(-2px); }
    .small-muted { color: var(--muted); font-size:13px; text-align:center; margin-top:10px; }
    footer {visibility:hidden;} #MainMenu {visibility:hidden;}
    /* Dark mode adjustments */
    .dark .stApp { background: #071018; }
    .dark .block-container { background: var(--dark-card); border: 1px solid rgba(255,255,255,0.03); color: #e6eef2; }
    .dark h1 { color: #4ad6c2; }
    .dark p.lead, .dark .small-muted { color: var(--dark-muted); }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- THEME SWITCH ---
if "theme" not in st.session_state:
    st.session_state.theme = "light"

col_theme = st.columns([1, 6, 1])
with col_theme[1]:
    theme = st.selectbox("Tema", options=["Light", "Dark"], index=0 if st.session_state.theme=="light" else 1)
    st.session_state.theme = "light" if theme == "Light" else "dark"
    if st.session_state.theme == "dark":
        st.markdown("<script>document.querySelector('body').classList.add('dark')</script>", unsafe_allow_html=True)
    else:
        st.markdown("<script>document.querySelector('body').classList.remove('dark')</script>", unsafe_allow_html=True)

# --- LOTTIE ---
lottie = load_lottieurl("https://assets10.lottiefiles.com/packages/lf20_qp1q7mct.json")

# --- HEADER ---
with st.container():
    st.markdown("<div class='block-container'>", unsafe_allow_html=True)
    header_cols = st.columns([1, 4, 1])
    with header_cols[1]:
        st.markdown("<div class='header-row'>", unsafe_allow_html=True)
        if lottie:
            st_lottie(lottie, height=90, key="hero", quality="low")
        st.markdown("<h1>Rifki Downloader</h1>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("<p class='lead'>Simpan video dan foto dari YouTube, TikTok, dan Instagram dengan cepat dan rapi.</p>", unsafe_allow_html=True)

        # --- INPUTS ---
        url = st.text_input("", placeholder="Tempel link lengkap di sini (https://...)")
        col_opts = st.columns([2, 1])
        with col_opts[0]:
            quality = st.selectbox("Kualitas video", options=["best", "720", "480", "360"], index=0)
        with col_opts[1]:
            st.write("")  # spacing
            st.write("")  # spacing

        st.write("")  # spacing

        # --- ACTION ---
        if st.button("🚀 Mulai Download"):
            if not url:
                st.warning("Masukkan link terlebih dahulu.")
            else:
                tipe = detect_type(url)
                if tipe == "VIDEO":
                    progress = st.progress(0)
                    with st.spinner("Memproses video..."):
                        ydl_opts = {
                            'format': 'best' if quality == 'best' else f'bestvideo[height<={quality}]+bestaudio/best',
                            'outtmpl': 'temp_video.%(ext)s',
                            'quiet': True,
                            'no_warnings': True,
                        }
                        try:
                            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                                info = ydl.extract_info(url, download=True)
                            progress.progress(60)
                            if not info:
                                st.error("Gagal mengambil metadata video.")
                            else:
                                title = clean_filename(info.get('title', 'video'))
                                ext = info.get('ext', 'mp4') or 'mp4'
                                temp_path = f"temp_video.{ext}"
                                if os.path.exists(temp_path):
                                    progress.progress(100)
                                    st.success("Selesai. Klik untuk menyimpan.")
                                    with open(temp_path, "rb") as f:
                                        st.download_button(
                                            label="⬇️ Simpan Video",
                                            data=f,
                                            file_name=f"{title}.{ext}",
                                            mime=f"video/{ext}",
                                            use_container_width=True,
                                        )
                                    safe_remove(temp_path)
                                else:
                                    st.error("File video tidak ditemukan setelah proses.")
                        except Exception as e:
                            st.error(f"Terjadi kesalahan: {e}")
                            safe_remove("temp_video.mp4")
                            safe_remove("temp_video.mkv")
                else:  # FOTO
                    with st.spinner("Mengambil foto dari Instagram..."):
                        temp_dir = "temp_ig"
                        safe_remove(temp_dir)
                        try:
                            L = instaloader.Instaloader(save_metadata=False, download_videos=False, quiet=True)
                            shortcode = url.split("/p/")[1].split("/")[0]
                            post = instaloader.Post.from_shortcode(L.context, shortcode)
                            L.download_post(post, target=temp_dir)
                            target_file = None
                            for fname in os.listdir(temp_dir):
                                if fname.lower().endswith((".jpg", ".jpeg", ".png")):
                                    target_file = os.path.join(temp_dir, fname)
                                    break
                            if target_file and os.path.exists(target_file):
                                st.success("Foto siap disimpan.")
                                with open(target_file, "rb") as f:
                                    st.download_button(
                                        label="⬇️ Simpan Foto",
                                        data=f,
                                        file_name=f"IG_{shortcode}.jpg",
                                        mime="image/jpeg",
                                        use_container_width=True,
                                    )
                                safe_remove(temp_dir)
                            else:
                                st.error("Tidak menemukan foto pada post tersebut.")
                                safe_remove(temp_dir)
                        except Exception as e:
                            st.error(f"Gagal mengambil foto: {e}")
                            safe_remove(temp_dir)

        st.markdown("<div class='small-muted'>Tip: Gunakan link lengkap dan pilih kualitas sesuai kebutuhan.</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
