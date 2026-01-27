import streamlit as st
import backend
import os

st.set_page_config(page_title="Ki.downloader - Video Downloader", page_icon="🔵", layout="wide")

# --- CSS: Light Theme, Pill Inputs, Blue Accents ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800&display=swap');

:root {
  --bg-color: #ffffff;
  --text-color: #1a1a1a;
  --accent-blue: #1877f2; /* Ki.downloader Blue */
  --accent-blue-hover: #145dbf;
  --gray-bg: #f5f7fa;
  --border-color: #e1e4e8;
}

.stApp {
  background-color: var(--bg-color);
  font-family: 'Outfit', sans-serif;
  color: var(--text-color);
}
header {visibility: hidden;}
.block-container {
    padding-top: 1rem;
    padding-bottom: 2rem;
    max-width: 1000px;
}

/* 1. Header Navigation */
.nav-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem 0;
    margin-bottom: 2rem;
}
.logo-text {
    font-size: 24px;
    font-weight: 800;
    color: #1a1a1a;
}
.logo-text span { color: var(--accent-blue); }

.theme-btn {
    background: var(--accent-blue);
    color: white;
    padding: 8px 16px;
    border-radius: 20px;
    font-weight: 600;
    font-size: 13px;
    border: none;
}

/* 2. Hero Section */
.hero-section {
    text-align: center;
    padding: 3rem 0;
    position: relative;
}
.hero-title {
    font-size: 48px;
    font-weight: 800;
    margin-bottom: 1rem;
    line-height: 1.2;
}
.hero-title span {
    color: var(--accent-blue);
    position: relative;
}
.hero-title span::after {
    content: '';
    display: block;
    width: 100%;
    height: 6px;
    background: var(--accent-blue);
    opacity: 0.2;
    position: absolute;
    bottom: 5px;
    left: 0;
    border-radius: 4px;
}
.hero-desc {
    color: #666;
    max-width: 600px;
    margin: 0 auto 2rem auto;
    font-size: 16px;
    line-height: 1.6;
}

/* 3. Input Pill Container */
/* Center the container */
.pill-container-outer {
    max-width: 800px;
    margin: 0 auto 3rem auto;
    background: white;
    border: 1px solid var(--border-color);
    border-radius: 99px;
    padding: 8px; /* Inner padding around widgets */
    box-shadow: 0 10px 30px rgba(0,0,0,0.05);
}

/* Paste Button Styling (Custom Class) */
.paste-btn-container {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100%;
}

/* Layout Hacks for Streamlit Columns inside the Pill */
div[data-testid="column"] {
    display: flex;
    align-items: center; /* Vertically center items */
    justify-content: center;
}

/* Input Field Styling */
div[data-testid="stTextInput"] {
    width: 100%;
}
div[data-testid="stTextInput"] > div {
    border: none !important;
    background-color: transparent !important;
}
div[data-testid="stTextInput"] input {
    font-size: 16px;
    color: #333;
    padding: 0 10px; 
}
/* Remove focus border on the input itself since wrapper has border */
div[data-testid="stTextInput"] > div[data-baseweb="input"]:focus-within {
    box-shadow: none !important;
    border-color: transparent !important;
}

/* Download Button Styling */
div[data-testid="stButton"] button {
    background: var(--accent-blue);
    color: white;
    border-radius: 99px;
    padding: 12px 32px;
    font-weight: 700;
    border: none;
    box-shadow: 0 4px 15px rgba(24, 119, 242, 0.3);
    height: 100%;
    width: 100%;
    white-space: nowrap;
}
div[data-testid="stButton"] button:hover {
    background: var(--accent-blue-hover);
    color: white;
}
div[data-testid="stButton"] button:active {
    background: var(--accent-blue-hover);
    color: white;
}

/* 4. Warning Banner */
.warning-banner {
    background: #1a1a1a;
    color: white;
    text-align: center;
    padding: 8px 12px; /* Reduced padding */
    font-size: 12px; /* Smaller font */
    font-weight: 700;
    border-radius: 8px;
    margin: 1rem auto; /* Reduced margin */
    max-width: 800px; /* Reduced width */
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 10px;
}

/* 5. Info Section (What is...) */
.info-section {
    text-align: center;
    margin-top: 4rem;
}
.section-title {
    font-size: 32px;
    font-weight: 800;
    margin-bottom: 2rem;
}
.section-title span {
    border-bottom: 4px solid var(--accent-blue);
}

/* 6. Feature Cards (Blue) */
.feature-grid {
    display: flex;
    gap: 20px;
    margin-top: 2rem;
    flex-wrap: wrap;
}
.feature-card {
    background: var(--accent-blue);
    color: white;
    padding: 30px;
    border-radius: 16px;
    flex: 1;
    min-width: 300px;
    text-align: left;
    position: relative;
}
.feature-card h3 {
    font-size: 20px;
    font-weight: 700;
    margin-bottom: 12px;
    color: white !important;
}
.feature-card p {
    font-size: 14px;
    opacity: 0.9;
    line-height: 1.5;
    color: white !important;
}
.arrow-icon {
    position: absolute;
    bottom: 20px;
    right: 20px;
    background: white;
    color: var(--accent-blue);
    width: 30px;
    height: 30px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: bold;
}

/* Result Card (Minimalist) */
.result-card {
    background: white;
    border: 1px solid var(--border-color);
    border-radius: 16px;
    padding: 20px;
    display: flex;
    gap: 20px;
    max-width: 700px;
    margin: 0 auto;
    box-shadow: 0 10px 40px rgba(0,0,0,0.05);
}
.res-thumb img { border-radius: 10px; width: 100%; display: block; }
.res-title { font-weight: 700; font-size: 18px; margin-bottom: 8px; color: #1a1a1a; }
.res-meta { font-size: 13px; color: #666; margin-bottom: 16px; }

/* Footer */
.footer-dark {
    background: #1a1a1a;
    color: #888;
    padding: 3rem 1rem;
    margin-top: 5rem;
    text-align: center;
    border-radius: 20px 20px 0 0;
}
/* Reduce standard block gap */
div[data-testid="stVerticalBlock"] > div {
    gap: 0.5rem;
}
</style>
""", unsafe_allow_html=True)

# 1. Header
col1, col2 = st.columns([4,1])
with col1:
    st.markdown("""
    <div class="nav-header">
        <div class="logo-text">Ki<span>.downloader</span></div>
    </div>
    """, unsafe_allow_html=True)
with col2:
     st.markdown("""
    <div class="nav-header" style="justify-content: flex-end;">
        <button class="theme-btn">Dark 🌙</button>
    </div>
    """, unsafe_allow_html=True)

# 2. Hero
st.markdown("""
<div class="hero-section">
    <div class="hero-title">Video <span>Downloader</span></div>
    <div class="hero-desc">
        Try this unique tool for quick, hassle-free downloads. 
        Transform your offline video collection with this reliable and efficient downloader.
    </div>
</div>
""", unsafe_allow_html=True)

# 3. Input Bar (Pill Layout)
st.markdown('<div class="pill-container-outer">', unsafe_allow_html=True)
c_inp, c_paste, c_btn = st.columns([3, 0.5, 1])

with c_inp:
    # Input field
    url_input = st.text_input("", placeholder="https://youtube.com/watch?v=...", label_visibility="collapsed")

with c_paste:
    # Automatic Paste Button (Visual placeholder or functional if possible locally)
    # Since we can't easily paste from clipboard in pure Streamlit web, we add the button as requested.
    st.button("📋", help="Paste from clipboard (Ctrl+V)")

with c_btn:
    dl_clicked = st.button("Download")

st.markdown('</div>', unsafe_allow_html=True)

# --- Logic Handling ---
if dl_clicked and url_input:
    with st.spinner("Fetching info..."):
        info = backend.get_video_info(url_input)
        
        if info:
            st.markdown('<div class="result-card">', unsafe_allow_html=True)
            r_img, r_txt = st.columns([1, 1.5])
            
            with r_img:
                thumb = info.get('thumbnail', '')
                st.markdown(f'<div class="res-thumb"><img src="{thumb}"></div>', unsafe_allow_html=True)
            
            with r_txt:
                title = info.get('title', 'Unknown Title')
                st.markdown(f'<div class="res-title">{title}</div>', unsafe_allow_html=True)
                st.markdown('<div class="res-meta">Format: MP4 (Best)</div>', unsafe_allow_html=True)
                
                if st.button("Save Video", key="save_video"):
                     path = backend.download_video(url_input)
                     if path:
                         with open(path, "rb") as f:
                             st.download_button(
                                 label="⬇️ Click to Save",
                                 data=f,
                                 file_name=os.path.basename(path),
                                 mime="video/mp4"
                             )
                         st.success("Video ready!")
                     else:
                         st.error("Download failed.")
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.error("Invalid URL or Video not found.")

# 4. Warning Banner
st.markdown("""
<div class="warning-banner">
    ⚡ WE DO NOT ALLOW/SUPPORT THE DOWNLOAD OF COPYRIGHTED MATERIAL!
</div>
""", unsafe_allow_html=True)

# 5. Info Section
# Fixed indentation to prevent leaking code
st.markdown("""
<div class="info-section">
<div class="section-title">What is <span>Ki.downloader</span></div>
<p style="color:#666; max-width:700px; margin:0 auto;">
Ki.downloader is one of the most popular downloader tools on the internet. 
With this tool, you can download and convert videos from almost anywhere on the internet.
</p>
<div class="feature-grid">
<div class="feature-card">
<h3>Experience Buffer-Free Entertainment With Video Downloader</h3>
<p>The Video Downloader provides uninterrupted entertainment and buffer-free experience for your favorite content. This user-friendly tool allows you to download videos effortlessly.</p>
<div class="arrow-icon">></div>
</div>
<div class="feature-card">
<h3>Your One-Stop Solution to Video Downloading</h3>
<p>Tired of those annoying buffering pauses ruining your binge? Well, say hello to uninterrupted entertainment with Ki.downloader! This nifty tool not only lets you download...</p>
<div class="arrow-icon">></div>
</div>
</div>
</div>
""", unsafe_allow_html=True)

# 6. FAQ (Visual Only)
st.markdown("""
<div class="info-section" style="margin-top:5rem;">
<div class="section-title">Frequently Asked <span>Questions</span></div>
<div style="display:flex; justify-content:center; gap:40px; text-align:left;">
<div style="flex:1; background:#f9f9f9; padding:20px; border-radius:12px;">
<h4>VideoDownloader: FAQs ❓</h4>
<p style="font-size:14px; color:#555;">Are there any subscription plans?</p>
<hr style="border:0; border-top:1px solid #ddd;">
<p style="font-size:14px; color:#555;">Can the downloader be used without info?</p>
</div>
<div style="flex:1; background:#f9f9f9; padding:20px; border-radius:12px;">
<h4>Ki.downloader: FAQs ❓</h4>
<p style="font-size:14px; color:#555;">Is it a one-time purchase?</p>
<hr style="border:0; border-top:1px solid #ddd;">
<p style="font-size:14px; color:#555;">Can the downloader be used safely?</p>
</div>
</div>
</div>
""", unsafe_allow_html=True)

# 7. Dark Footer
st.markdown("""
<div class="footer-dark">
<h2>Ki.downloader</h2>
<p>Copyright © 2026 All Rights Reserved</p>
<div style="margin-top:20px; font-size:12px; color:#555;">
English • Deutsch • Polski • Français • Español • Bahasa Indonesia
</div>
</div>
""", unsafe_allow_html=True)
