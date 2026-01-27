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
    return "".join([c for c in title if c.isalpha() or c.isdigit() or c == ' ']).rstrip()

def detect_type(url):
    if "instagram.com/p/" in url:
        return "FOTO"
    return "VIDEO"

# --- STYLES: modern, muted, clean ---
st.markdown(
    """
    <style>
    :root{
        --bg-1: #f6faf8;
        --card-bg: rgba(255,255,255,0.96);
        --muted: #6b7280;
        --accent-1: #2a7f7f; /* teal */
        --accent-2: #8fbf9f; /* sage */
        --glass-border: rgba(0,0,0,0.06);
    }
    .stApp {
        background: linear-gradient(180deg, var(--bg-1) 0%, #eef7f6 100%);
        color: #0f1724;
        font-family: "Inter", "Segoe UI", system-ui, -apple-system, "Helvetica Neue", Arial;
    }
    .block-container {
        background: var(--card-bg);
        padding: 2.2rem 2rem;
        border-radius: 16px;
        box-shadow: 0 8px 24px rgba(15, 23, 36, 0.06);
        border: 1px solid var(--glass-border);
        max-width: 820px;
        margin: 2rem auto;
    }
    h1 {
        color: var(--accent-1);
        text-align: center;
        font-weight: 700;
        margin-bottom: 0.1rem;
        letter-spacing: -0.5px;
    }
    p.lead {
        color: var(--muted);
        text-align: center;
        margin-top: 0.2rem;
        margin-bottom: 1.2rem;
    }
    /* Input */
    .stTextInput > div > div > input {
        text-align: left;
        border-radius: 12px;
        border: 1px solid rgba(15,23,36,0.08);
        padding: 12px 14px;
        background: #fff;
    }
    .stTextInput > div > div > input:focus {
        border-color: var(--accent-1);
        box-shadow: 0 6px 18px rgba(42,127,127,0.08);
    }
    /* Button */
    .stButton > button {
        width: 100%;
        background: linear-gradient(90deg, var(--accent-1), var(--accent-2));
        color: white;
        border: none;
        border-radius: 10px;
        padding: 12px 14px;
        font-weight: 600;
        font-size: 15px;
        box-shadow: 0 6px 18px rgba(42,127,127,0.08);
    }
    .stButton > button:hover {
        transform: translateY(-1px);
    }
    /* Small helper text */
    .small-muted { color: var(--muted); font-size: 13px; text-align:center; margin-top:8px; }
    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True,
)

# --- LOTTIE (subtle size) ---
lottie_download = load_lottieurl("https://assets10.lottiefiles.com/packages/lf20_qp1q7mct.json")

# --- HEADER ---
with st.container():
    if lottie_download:
        st_lottie(lottie_download, height=120, key="nature_vibe", quality="low")
    st.markdown("<h1>🌿 Rifki Downloader</h1>", unsafe_allow_html=True)
    st.markdown("<p class='lead'>Simpan video TikTok, IG, & YouTube dengan mudah — cepat, bersih, dan aman.</p>", unsafe_allow_html=True)

# --- INPUT AREA ---
url = st.text_input("", placeholder="Tempel link di sini... (YouTube, TikTok, Instagram post)")

if url:
    tipe_konten = detect_type(url)
    st.write("")  # spacing

    if st.button(f"🚀 Mulai Download {tipe_konten}"):
        if tipe_konten == "VIDEO":
            with st.spinner("🔄 Sedang memproses di server..."):
                ydl_opts = {
                    'format': 'best',
                    'outtmpl': 'temp_video.%(ext)s',
                    'quiet': True,
                    'no_warnings': True,
                }
                try:
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(url, download=True)
                    if not info:
                        st.error("Gagal mengambil metadata video.")
                    else:
                        judul = clean_filename(info.get('title', 'video'))
                        ext = info.get('ext', 'mp4') or 'mp4'
                        temp_path = f"temp_video.{ext}"
                        if os.path.exists(temp_path):
                            st.success("✅ Selesai! Silakan simpan.")
                            with open(temp_path, "rb") as f:
                                st.download_button(
                                    label="⬇️ SIMPAN VIDEO KE GALERI",
                                    data=f,
                                    file_name=f"{judul}.{ext}",
                                    mime=f"video/{ext}",
                                    use_container_width=True,
                                )
                            try:
                                os.remove(temp_path)
                            except Exception:
                                pass
                        else:
                            st.error("File video tidak ditemukan setelah proses.")
                except Exception as e:
                    st.error(f"Error: {e}")

        elif tipe_konten == "FOTO":
            with st.spinner("📸 Sedang mengambil foto..."):
                temp_dir = "temp_ig_nature"
                if os.path.exists(temp_dir):
                    try:
                        shutil.rmtree(temp_dir)
                    except Exception:
                        pass
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
                        st.success("✅ Foto siap disimpan!")
                        with open(target_file, "rb") as f:
                            st.download_button(
                                label="⬇️ SIMPAN FOTO",
                                data=f,
                                file_name=f"IG_{shortcode}.jpg",
                                mime="image/jpeg",
                                use_container_width=True,
                            )
                        try:
                            shutil.rmtree(temp_dir)
                        except Exception:
                            pass
                    else:
                        st.error("Foto tidak ditemukan pada post tersebut.")
                except Exception as e:
                    st.error(f"Gagal: {e}")

# --- FOOTER HELPER ---
st.markdown("<div class='small-muted'>Tip: Tempel link lengkap (https://...) untuk hasil terbaik.</div>", unsafe_allow_html=True)
