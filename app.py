import streamlit as st
import time

st.set_page_config(page_title="Lorvantis AI", page_icon="🤖")
st.title("Lorvantis AI")

# 1. Oturum Hafızasını (Session State) Başlatma
if "messages" not in st.session_state:
    st.session_state.messages = []

if "is_processing" not in st.session_state:
    st.session_state.is_processing = False

if "uploader_key" not in st.session_state:
    st.session_state.uploader_key = 0

# 2. Geçmiş Mesajları Ekrana Çizdirme
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message.get("image"):
            st.image(message["image"], width=250)
        if message.get("content"):
            st.write(message["content"])

# 3. Görsel Yükleme Alanı
# Key parametresi dinamiktir; resim yollandıktan sonra alanı sıfırlamak için kullanılır.
uploaded_file = st.file_uploader(
    "Bir görsel ekleyin (İsteğe bağlı)", 
    type=["png", "jpg", "jpeg"], 
    key=f"uploader_{st.session_state.uploader_key}"
)

# 4. Sohbet Giriş Kutusu
prompt = st.chat_input("Lorvantis'e bir şeyler yazın...")

# 5. Mesaj Gönderme ve Hız Sınırı (Rate Limit) Yönetimi
if prompt or uploaded_file:
    # Eğer sistem zaten bir yanıt işliyorsa, hızlı basmaları engelle
    if st.session_state.is_processing:
        st.warning("Lorvantis henüz yanıtını bitirmedi, lütfen bekleyin!")
    else:
        st.session_state.is_processing = True

        # Kullanıcı verilerini hazırlama
        user_message = {"role": "user", "content": prompt if prompt else "", "image": None}
        
        if uploaded_file:
            user_message["image"] = uploaded_file.getvalue()

        # Ekrana Kullanıcı Mesajını Ekle
        st.session_state.messages.append(user_message)
        with st.chat_message("user"):
            if user_message["image"]:
                st.image(user_message["image"], width=250)
            if user_message["content"]:
                st.write(user_message["content"])

        # Görselin köşede/ekranda TAKILI KALMAMASI için uploader alanını sıfırla
        if uploaded_file:
            st.session_state.uploader_key += 1

        # Yapay Zekanın Yanıt Alanı
        with st.chat_message("assistant"):
            with st.spinner("Lorvantis düşünüyor..."):
                try:
                    # --- BURAYA KENDİ API ÇAĞRINI EKLEYECEKSİN ---
                    # Örnek: response = my_api_call(prompt, image)
                    time.sleep(1.5)  # Üst üste hızlı istek gitmesini önleyen kısa bekleme
                    ai_response = "Lorvantis yanıtı burada görünecek."
                    # ---------------------------------------------

                    st.write(ai_response)
                    st.session_state.messages.append({"role": "assistant", "content": ai_response})

                except Exception as e:
                    st.error(f"Hata oluştu: {e}")

        # İşlem bitti, kilidi aç ve sayfayı yenile ki yükleyici (uploader) temizlensin
        st.session_state.is_processing = False
        st.rerun()
