import streamlit as st
from google import genai
from google.genai import types
from PIL import Image

# Pengaturan halaman aplikasi
st.set_page_config(page_title="TikTok Affiliate AI Pro", layout="centered")
st.title("🎬 TikTok Affiliate AI Content Generator")
st.write("Upload foto produkmu untuk mendapatkan prompt gambar, video, dan caption TikTok otomatis!")

# Kolom input API Key di menu samping agar aman
st.sidebar.title("🔑 Pengaturan")
api_key = st.sidebar.text_input("Masukkan Gemini API Key:", type="password")
st.sidebar.markdown("[Dapatkan API Key Gratis di Sini](https://aistudio.google.com/)")

# Fitur Upload Gambar
uploaded_file = st.file_uploader("Pilih foto produk...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Menggunakan width='stretch' sesuai panduan log Streamlit terbaru
    st.image(uploaded_file, caption='Produk sukses di-upload.', width='stretch')
    
    # Tombol Eksekusi
    if st.button("✨ Hasilkan Konten TikTok"):
        if not api_key or api_key.strip() == "":
            st.error("🛑 API Key kosong! Silakan klik tanda panah (>>) di pojok kiri atas, lalu masukkan Gemini API Key Anda terlebih dahulu.")
        else:
            with st.spinner("AI sedang menganalisis produk dan meracik konten... Mohon tunggu sebentar..."):
                try:
                    # Menggunakan Google GenAI Client versi terbaru
                    client = genai.Client(api_key=api_key)
                    
                    # Membuka gambar dengan PIL agar kompatibel dengan SDK baru
                    image = Image.open(uploaded_file)
                    
                    # Instruksi Sistem Kustom Anda
                    system_prompt = """Anda adalah AI Prompt Engineer dan Pakar Konten TikTok Affiliate. Tugas Anda adalah membantu pengguna membuat aset konten berdasarkan gambar produk yang mereka unggah.

Analisis gambar produk tersebut dengan teliti (perhatikan bentuk, warna, fungsi, dan keunikannya). Kemudian, berikan output dengan format yang rapi dan terstruktur sebagai berikut:

---
## 📦 HASIL ANALISIS PRODUK
* **Nama/Jenis Produk:** [Sebutkan nama/jenis produk berdasarkan gambar]
* **Target Audiens:** [Siapa yang paling cocok membeli produk ini]

---
## 🎨 PROMPT GAMBAR STUDIO (Untuk Nano banana 2)
*Gunakan prompt ini di AI Image Generator untuk membuat foto produk yang estetik.*
`[Tulis prompt bahasa Inggris di sini. Gaya: Menggunakan image yang di upload sebagai referensi tanpa mendeskripsikan produk, minimalist studio product photography, clean aesthetic, cinematic lighting, 8k, aspect ratio 9:16 untuk TikTok]`

## 🎨 PROMPT GAMBAR TANGAN (Untuk Nano banana 2)
*Gunakan prompt ini di AI Image Generator untuk membuat foto produk yang estetik.*
`[Tulis prompt bahasa Inggris di sini. Gaya: Menggunakan image yang di upload sebagai referensi tanpa mendeskripsikan produk, Ada gambar tangan yang sedang memegang produk, minimalist studio product photography, clean aesthetic, cinematic lighting, 8k, aspect ratio 9:16 untuk TikTok]`

---
## 🎬 PROMPT VIDEO (Untuk Veo 3)
*Gunakan prompt ini di AI Video Generator untuk membuat video estetik 5 detik.*
`[Tulis prompt video bahasa Inggris di sini. Gaya: Menggunakan image referensi, slow motion macro shot, camera panning smoothly, minimalist background, commercial style]`

## 🎬 PROMPT VIDEO (Untuk Animate Meta Ai)
*Gunakan prompt ini di AI Video Generator untuk membuat video estetik 5 detik.*
`[Tulis prompt video bahasa Inggris di sini. Gaya: Menggunakan image referensi, slow motion macro shot, camera panning smoothly, minimalist background, commercial style]`

## 🎬 PROMPT VIDEO UNIVERSAL
*Gunakan prompt ini di AI Video Generator untuk membuat video estetik 5 detik.*
`[Tulis prompt video bahasa Inggris di sini. Gaya: Menggunakan image referensi, Subtle ambient motion, gentle atmospheric movement, slow drifting particles in the air, soft flickering light, slight environmental movement only, keep all main subjects completely static and still, no camera movement, seamless loop, cinematic, photorealistic, natural subtle motion]`

---
## ✍️ COPYWRITING TIKTOK (Caption & Hashtags)
* **Hook (3 Detik Pertama):** [Tulis 2 pilihan kalimat hook yang bikin orang berhenti scrolling]
* **Body/Caption:** [Tulis caption pendek, relevan, menggunakan bahasa santai/tren anak muda Indonesia, jelaskan keunggulan produk, dan akhiri dengan CTA]
* **Hashtags:** [Berikan 5 hashtag yang relevan dan sedang tren di TikTok]
---"""
                    
                    # Memanggil Gemini 3.5 Flash dengan konfigurasi SDK baru yang benar
                    response = client.models.generate_content(
                        model='gemini-3.5-flash',
                        contents=[image, "Analisis produk ini dan buatkan seluruh kebutuhan kontennya sesuai format baru."],
                        config=types.GenerateContentConfig(
                            system_instruction=system_prompt
                        )
                    )
                    
                    if response.text:
                        st.success("✨ Sukses Meracik Konten!")
                        st.markdown(response.text)
                    else:
                        st.warning("⚠️ AI terhubung, tetapi memberikan respon kosong. Coba unggah ulang gambar.")
                        
                except Exception as e:
                    st.error(f"❌ Terjadi kesalahan sistem: {e}")
                    st.info("Tips: Periksa apakah API Key Anda di menu samping sudah benar dan masih aktif.")
