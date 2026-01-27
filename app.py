import streamlit as st
import yt_dlp
import instaloader
import os
import shutil
import time

st.set_page_config(page_title="Rifki Downloader", page_icon="🍃", layout="wide")

# --- CUSTOM CSS (Gradient hero, big input, feature cards, dark footer) ---
st.markdown("""
    <style>
    /* Page background */
    .stApp {
        background-color: #F7F7FB;
        font-family: 'Segoe UI', Roboto, Arial, sans-serif;
    }

    /* HERO: gradient purple -> blue */
    .hero {
        background: linear-gradient(135deg, #6A4CFF 0%, #3B82F6 100%);
        color: #ffffff;
        padding: 60px 30px;
        border-radius: 18px;
        box-shadow: 0 20px 40px rgba(59,130,246,0.15);
        margin-bottom: 30px;
    }
    .hero .title {
        font-size: 42px;
        font-weight: 800;
        margin-bottom: 8px;
        letter-spacing: -0.5px;
    }
    .hero .subtitle {
        font-size: 16px;
        color: rgba(255,255,255,0.92);
        margin-bottom: 22px;
    }

    /* Input area */
    .input-wrap {
        display:flex;
        gap:12px;
        align-items:center;
        justify-content:center;
        max-width:900px;
        margin: 0 auto;
    }
    .stTextInput > div > div > input {
        padding: 18px 20px;
        border-radius: 14px;
        border: none;
        font-size: 16px;
        box-shadow: 0 8px 20px rgba(16,24,40,0.08);
    }
    /* Make the input visually larger on desktop */
    @media (min-width: 900px) {
        .stTextInput > div > div > input { font-size:18px; padding:20px 24px; }
    }

    /* Primary CTA button style */
    .stButton > button {
        background: linear-gradient(90deg,#FFD166,#FFB86B);
        color: #1F2937;
        font-weight: 700;
        padding: 14px 22px;
        border-radius: 12px;
        border: none;
        box-shadow: 0 8px 18px rgba(255,184,107,0.18);
        transition: transform .12s ease;
    }
    .stButton > button:hover { transform: translateY(-3px); }

    /* Feature cards */
    .features {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 18px;
        margin-top: 22px;
    }
    .card {
        background: #ffffff;
        padding: 18px;
        border-radius: 12px;
        box-shadow: 0 8px 24px rgba(16,24,40,0.04);
        border: 1px solid rgba(59,130,246,0.06);
    }
    .card .num {
        font-size: 36px;
        font-weight: 800;
        color: rgba(59,130,246,0.08);
    }
    .card .ctitle {
        font-weight: 700;
        color: #0F172A;
        margin-top: 6px;
        margin-bottom: 8px;
    }
    .card .cdesc { color: #475569; font-size: 14px; }

    /* Footer */
    .site-footer {
        background: #0B1220;
        color: rgba(255,255,255,0.85);
        padding: 28px 20px;
        border-radius: 10px;
        margin-top: 30px;
    }
    .site-footer a { color: rgba(255,255,255,0.9); text-decoration: none; margin-right: 18px; }
    .site-footer .small { color: rgba(255,255,255,0.6); font-size: 13px; margin-top: 10px; }

    /* Hide default Streamlit footer/menu */
    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    .block-container {padding-top: 1rem; padding-left: 1rem; padding-right: 1rem;}
    </style>
""", unsafe_allow_html=True)

# --- HERO SECTION ---
st.markdown('<div class="hero">', unsafe_allow_html=True)
st.markdown('<div class="title">Unduh Video TikTok, Instagram & YouTube</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Simpan video tanpa watermark dalam kualitas HD. Tempel tautan di bawah lalu klik Download.</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# --- INPUT AREA (centered) ---
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown('<div class="input-wrap">', unsafe_allow_html=True)
    url = st.text_input("", placeholder="Tempel tautan video di sini... (contoh: https://...)", key="main_input")
    st.markdown('</div>', unsafe_allow_html=True)
    st.write("")  # spacing
    process_btn = st.button("DOWNLOAD SEKARANG ⬇️", use_container_width=True)

# --- BACKEND LOGIC (tetap seperti sebelumnya) ---
if process_btn:
    if not url:
        st.warning("⚠️ Harap masukkan link video terlebih dahulu!")
    else:
        tipe = "VIDEO"
        if "instagram.com/p/" in url:
            tipe = "FOTO"

        status_box = st.empty()
        progress_bar = st.progress(0)

        if tipe == "VIDEO":
            status_box.info("⏳ Sedang memproses video...")
            def clean_name(t): return "".join([c for c in t if c.isalnum() or c==' ']).rstrip()
            ydl_opts = {'format': 'best', 'outtmpl': 'temp_vid.%(ext)s', 'quiet': True}
            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    progress_bar.progress(30)
                    info = ydl.extract_info(url, download=True)
                    judul = clean_name(info.get('title', 'Video Result'))
                    ext = info.get('ext', 'mp4')
                    progress_bar.progress(100)
                if os.path.exists(f"temp_vid.{ext}"):
                    status_box.success("✅ Video Siap!")
                    with open(f"temp_vid.{ext}", "rb") as f:
                        st.download_button(
                            label=f"⬇️ SIMPAN VIDEO ({ext.upper()})",
                            data=f,
                            file_name=f"{judul}.{ext}",
                            mime=f"video/{ext}",
                            use_container_width=True
                        )
                    # optional cleanup
                    # os.remove(f"temp_vid.{ext}")
            except Exception as e:
                status_box.error(f"Gagal: {e}")

        elif tipe == "FOTO":
            status_box.info("📸 Mengambil foto...")
            if os.path.exists("temp_img"): shutil.rmtree("temp_img")
            try:
                L = instaloader.Instaloader(save_metadata=False, download_videos=False)
                shortcode = url.split("/p/")[1].split("/")[0]
                post = instaloader.Post.from_shortcode(L.context, shortcode)
                L.download_post(post, target="temp_img")
                target = None
                for f in os.listdir("temp_img"):
                    if f.endswith(".jpg"):
                        target = os.path.join("temp_img", f)
                        break
                if target:
                    status_box.success("✅ Foto Siap!")
                    with open(target, "rb") as f:
                        st.download_button(
                            label="⬇️ SIMPAN FOTO",
                            data=f,
                            file_name=f"IG_{shortcode}.jpg",
                            mime="image/jpeg",
                            use_container_width=True
                        )
                    shutil.rmtree("temp_img")
                else:
                    status_box.error("Foto tidak ditemukan.")
            except Exception as e:
                status_box.error("Gagal. Pastikan akun publik atau cek error: " + str(e))

# --- FEATURES / STEPS (three cards) ---
st.write("---")
st.markdown('<div class="features">', unsafe_allow_html=True)
st.markdown('''
<div class="card">
  <div class="num">1</div>
  <div class="ctitle">Temukan Video</div>
  <div class="cdesc">Buka TikTok/IG/YT, cari video yang ingin disimpan, lalu salin tautan.</div>
</div>
''', unsafe_allow_html=True)
st.markdown('''
<div class="card">
  <div class="num">2</div>
  <div class="ctitle">Tempel Tautan</div>
  <div class="cdesc">Tempel link di kolom atas, pastikan link valid.</div>
</div>
''', unsafe_allow_html=True)
st.markdown('''
<div class="card">
  <div class="num">3</div>
  <div class="ctitle">Download</div>
  <div class="cdesc">Klik tombol Download, lalu simpan file ke perangkatmu.</div>
</div>
''', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# --- FOOTER ---
st.markdown("""
<div class="site-footer">
  <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap;">
    <div>
      <a href="#">Contacts</a>
      <a href="#">TikTok Viewer</a>
      <a href="#">Twitter video downloader</a>
      <a href="#">Download video Instagram</a>
    </div>
    <div style="text-align:right;">
      <div style="font-weight:700">Bahasa Indonesia ▾</div>
    </div>
  </div>
  <div class="small">We are not affiliated with TikTok, Douyin or Bytedance. Created by Rifki team - video downloading experts.</div>
  <div class="small">Copyright 2018-2026</div>
</div>
""", unsafe_allow_html=True)
