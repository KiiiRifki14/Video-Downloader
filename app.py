import streamlit as st
import yt_dlp
import instaloader
import os
import shutil
import time

# --- KONFIGURASI HALAMAN (Tampilan Bersih) ---
st.set_page_config(page_title="Universal Downloader", page_icon="📥", layout="centered")

# --- CSS: MODERN MINIMALIST STYLE ---
st.markdown("""
    <style>
    /* 1. Background Halaman: Abu-abu sangat muda (Clean) */
    .stApp {
        background-color: #F8F9FA;
        color: #212529;
    }
    
    /* 2. Judul Utama */
    h1 {
        color: #111111;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    /* 3. Input Box (Kotak Link) */
    .stTextInput > div > div > input {
        text-align: center;
        background-color: #FFFFFF;
        color: #333333;
        border: 1px solid #E0E0E0;
        border-radius: 12px;
        padding: 15px;
        font-size: 16px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05); /* Bayangan halus */
    }
    .stTextInput > div > div > input:focus {
        border-color: #000000;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
    }

    /* 4. Tombol Utama (Elegan Hitam) */
    .stButton > button {
        width: 100%;
        background-color: #111111;
        color: white;
        border-radius: 12px;
        font-weight: 600;
        padding: 0.8rem 1rem;
        border: none;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .stButton > button:hover {
        background-color: #333333;
        transform: translateY(-2px); /* Efek naik sedikit saat di-hover */
        box-shadow: 0 6px 12px rgba(0,0,0,0.15);
    }

    /* 5. Menghilangkan elemen pengganggu */
    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    
    /* 6. Kotak Info/Success biar warnanya soft */
    .stAlert {
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# --- JUDUL & HEADER ---
st.markdown("<h1 style='text-align: center;'>📥 Universal Downloader</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #666; font-size: 14px;'>Download Video TikTok, Instagram, & YouTube dengan mudah.</p>", unsafe_allow_html=True)
st.markdown("---") # Garis pemisah tipis

# --- FUNGSI PEMBERSIH FILENAME ---
def clean_filename(title):
    return "".join([c for c in title if c.isalpha() or c.isdigit() or c==' ']).rstrip()

# --- INPUT URL ---
# Kita buat label kosong agar tampilan lebih bersih
url = st.text_input("", placeholder="Tempel Link (Paste Link) di sini...")

# --- LOGIKA AUTO DETECT ---
def detect_type(url):
    if "instagram.com/p/" in url:
        return "FOTO"
    return "VIDEO" 

# --- EKSEKUSI PROGRAM ---
if url:
    tipe_konten = detect_type(url)
    
    # Beri jarak sedikit
    st.write("") 
    
    # Tombol Proses
    if st.button(f"Start Download ({tipe_konten})"):
        
        # --- 1. PROSES VIDEO ---
        if tipe_konten == "VIDEO":
            status_box = st.empty() # Kotak status dinamis
            status_box.info("🔄 Sedang menghubungkan ke server...")
            
            ydl_opts = {
                'format': 'best',
                'outtmpl': 'temp_video.%(ext)s',
                'quiet': True,
            }
            
            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    judul = clean_filename(info.get('title', 'video_result'))
                    ext = info.get('ext', 'mp4')
                
                # Cek File
                video_file = f"temp_video.{ext}"
                if os.path.exists(video_file):
                    status_box.success("✅ Siap didownload!")
                    
                    # TOMBOL DOWNLOAD FINAL (Style Khusus)
                    with open(video_file, "rb") as file:
                        st.download_button(
                            label=f"⬇️ Simpan Video ke Galeri",
                            data=file,
                            file_name=f"{judul}.{ext}",
                            mime=f"video/{ext}",
                            use_container_width=True
                        )
                else:
                    status_box.error("Gagal mengambil video.")
                    
            except Exception as e:
                status_box.error(f"Error: {e}")

        # --- 2. PROSES FOTO INSTAGRAM ---
        elif tipe_konten == "FOTO":
            status_box = st.empty()
            status_box.info("📸 Mengambil foto...")
            
            temp_dir = "temp_ig_photo"
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
                
            L = instaloader.Instaloader(
                save_metadata=False, 
                download_videos=False,
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
            )
            
            try:
                shortcode = url.split("/p/")[1].split("/")[0]
                post = instaloader.Post.from_shortcode(L.context, shortcode)
                L.download_post(post, target=temp_dir)
                
                target_file = None
                for file in os.listdir(temp_dir):
                    if file.endswith(".jpg"):
                        target_file = os.path.join(temp_dir, file)
                        break
                
                if target_file:
                    status_box.success("✅ Foto siap!")
                    with open(target_file, "rb") as file:
                        st.download_button(
                            label="⬇️ Simpan Foto ke Galeri",
                            data=file,
                            file_name=f"IG_{shortcode}.jpg",
                            mime="image/jpeg",
                            use_container_width=True
                        )
                    shutil.rmtree(temp_dir)
                else:
                    status_box.error("Foto tidak ditemukan (Akun Private?).")
            except Exception as e:
                status_box.error(f"Gagal: {e}")
