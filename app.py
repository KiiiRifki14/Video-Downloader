import streamlit as st
import yt_dlp
import instaloader
import os
import shutil

# Judul Halaman Web
st.title("🚀 Video Downloader Pribadi")
st.write("Paste link TikTok, IG, atau YouTube di bawah ini.")

# Input Link dari User
url = st.text_input("Masukkan Link URL:")

# Pilihan Menu
option = st.selectbox(
    "Pilih Tipe Download:",
    ('Video (TikTok/YouTube)', 'Foto Instagram')
)

# Tombol Eksekusi
if st.button("Mulai Download"):
    if not url:
        st.error("Link tidak boleh kosong!")
    else:
        # --- LOGIKA DOWNLOAD VIDEO ---
        if option == 'Video (TikTok/YouTube)':
            st.info("Sedang memproses video... (Tunggu sebentar)")
            ydl_opts = {
                'format': 'best',
                'outtmpl': 'downloaded_video.%(ext)s', # Nama file sementara
                'ignoreerrors': True,
            }
            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                
                # Cari file yang barusan didownload (bisa mp4 atau webm)
                video_file = None
                for file in os.listdir("."):
                    if file.startswith("downloaded_video"):
                        video_file = file
                        break
                
                if video_file:
                    # Tampilkan Tombol Download ke HP
                    with open(video_file, "rb") as file:
                        btn = st.download_button(
                                label="⬇️ Download ke HP",
                                data=file,
                                file_name="video_hasil.mp4",
                                mime="video/mp4"
                            )
                    st.success("Selesai! Klik tombol di atas.")
                else:
                    st.error("Gagal menemukan file video.")
                    
            except Exception as e:
                st.error(f"Error: {e}")

        # --- LOGIKA DOWNLOAD FOTO IG ---
        elif option == 'Foto Instagram':
            st.info("Sedang mengambil foto IG...")
            L = instaloader.Instaloader(save_metadata=False, download_videos=False)
            try:
                if "/p/" in url:
                    shortcode = url.split("/p/")[1].split("/")[0]
                    post = instaloader.Post.from_shortcode(L.context, shortcode)
                    
                    dirname = f"ig_{shortcode}"
                    L.download_post(post, target=dirname)
                    
                    # Cari file jpg di dalam folder
                    target_file = None
                    for file in os.listdir(dirname):
                        if file.endswith(".jpg"):
                            target_file = os.path.join(dirname, file)
                            break
                    
                    if target_file:
                        with open(target_file, "rb") as file:
                            st.download_button(
                                label="⬇️ Simpan Foto",
                                data=file,
                                file_name=f"foto_ig_{shortcode}.jpg",
                                mime="image/jpeg"
                            )
                        st.success("Foto berhasil diambil!")
                        # Bersihkan folder sampah
                        shutil.rmtree(dirname)
                else:
                    st.warning("Link harus postingan foto (/p/)")
            except Exception as e:
                st.error(f"Gagal (Mungkin IP Server diblokir IG): {e}")