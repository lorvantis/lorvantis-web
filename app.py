import streamlit as st
import requests
import json
import base64
import time
import streamlit.components.v1 as components

# --- GİZLİ API HAVUZU ---
API_KEYS = [
    "AQ.Ab8RN6JnfkCFFuZ2b3Mzk2x7ftsjbZA_nYKiAmLAJ4dWiRmxOA",
    "AQ.Ab8RN6KbI1u8UKIsaQ9u9IOFbSJMPMXzupQ8jmP8vE8ZSBOHFw",
    "AQ.Ab8RN6LMoSnq5Cc1-Axu8PudsUEBDDdVaMD8xj69wEv4tIzz3A",
    "AQ.Ab8RN6I0Yb-r1EbIUo9c4pj3_8Yx-rXIaqQaCV06DuE4u47KVw"
]

# Sayfa Yapılandırması
st.set_page_config(page_title="Lorvantis AI", page_icon="🤖", layout="centered")

# --- CSS: ARAYÜZ VE GÖRSEL DÜZENLEMELER ---
st.markdown("""
    <style>
        [data-testid="stChatInput"] {
            padding-left: 3rem !important;
        }
        div[data-testid="stPopover"] {
            position: fixed;
            bottom: 2rem;
            left: 1.5rem;
            z-index: 99999;
        }
        @media (max-width: 768px) {
            div[data-testid="stPopover"] {
                bottom: 1.5rem;
                left: 1rem;
            }
        }
        div[data-testid="stPopover"] button {
            border-radius: 50%;
            padding: 0.5rem;
            width: 40px;
            height: 40px;
            font-size: 20px;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .img-thumbnail {
            position: fixed;
            bottom: 5rem;
            left: 2rem;
            width: 60px;
            height: 60px;
            border-radius: 8px;
            border: 2px solid #4CAF50;
            object-fit: cover;
            z-index: 99998;
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        }
    </style>
""", unsafe_allow_html=True)

# --- OTURUM VE HAFIZA YÖNETİMİ ---
if "chats" not in st.session_state:
    st.session_state.chats = {"Varsayılan Sohbet": [{"role": "assistant", "content": "Selam kanka! Lorvantis hazır, anlat bakalım!"}]}
if "current_chat" not in st.session_state:
    st.session_state.current_chat = "Varsayılan Sohbet"
if "temp_image" not in st.session_state:
    st.session_state.temp_image = None
if "ready_image" not in st.session_state:
    st.session_state.ready_image = None
if "uploader_key" not in st.session_state:
    st.session_state.uploader_key = 1

def encode_image(image_bytes):
    return base64.b64encode(image_bytes).decode('utf-8')

# --- YAN MENÜ: SOHBET YÖNETİMİ ---
with st.sidebar:
    st.title("🗂️ Sohbetler")
    new_chat = st.text_input("Yeni Sohbet Adı:")
    if st.button("➕ Sohbet Başlat"):
        if new_chat and new_chat not in st.session_state.chats:
            st.session_state.chats[new_chat] = [{"role": "assistant", "content": f"Selam kanka! {new_chat} konusundayız, dinliyorum."}]
            st.session_state.current_chat = new_chat
            st.rerun()
            
    st.markdown("---")
    chats_to_delete = []
    for chat_name in list(st.session_state.chats.keys()):
        col1, col2 = st.columns([4, 1])
        with col1:
            if st.button(f"💬 {chat_name}", use_container_width=True, key=f"btn_{chat_name}"):
                st.session_state.current_chat = chat_name
                st.rerun()
        with col2:
            if st.button("❌", key=f"del_{chat_name}"):
                chats_to_delete.append(chat_name)
                
    for chat_name in chats_to_delete:
        del st.session_state.chats[chat_name]
        if st.session_state.current_chat == chat_name:
            if st.session_state.chats:
                st.session_state.current_chat = list(st.session_state.chats.keys())[0]
            else:
                st.session_state.chats = {"Yeni Sohbet": [{"role": "assistant", "content": "Sıfırdan başladık kanka!"}]}
                st.session_state.current_chat = "Yeni Sohbet"
        st.rerun()

# --- ÜST MENÜ ---
col_title, col_menu = st.columns([8, 1])
with col_title:
    st.title("🤖 Lorvantis AI")
    st.caption("Kesintisiz Gemini Motoru Aktif")
with col_menu:
    st.markdown("<br>", unsafe_allow_html=True)
    with st.popover("⋮"):
        if st.button("🗑️ Temizle", use_container_width=True):
            st.session_state.chats[st.session_state.current_chat] = [{"role": "assistant", "content": "Sohbet temizlendi kanka, dinliyorum."}]
            st.rerun()

# --- GEÇMİŞİ EKRANA BASMA ---
for msg in st.session_state.chats[st.session_state.current_chat]:
    st.chat_message(msg["role"]).write(msg["content"])

# --- FOTOĞRAF YÜKLEME ---
with st.popover("➕"):
    tab1, tab2 = st.tabs(["🖼️ Galeri", "📸 Kamera"])
    with tab1:
        uploaded_file = st.file_uploader("Seç", type=["png", "jpg", "jpeg"], key=f"up_{st.session_state.uploader_key}")
        if uploaded_file:
            st.session_state.temp_image = uploaded_file.getvalue()
    with tab2:
        camera_file = st.camera_input("Çek", key=f"cam_{st.session_state.uploader_key}")
        if camera_file:
            st.session_state.temp_image = camera_file.getvalue()

if st.session_state.temp_image:
    st.markdown("---")
    st.info("📷 Görsel hazır!")
    st.image(st.session_state.temp_image, width=200)
    col_iptal, col_yolla = st.columns(2)
    with col_iptal:
        if st.button("❌ İptal", use_container_width=True):
            st.session_state.temp_image = None
            st.session_state.uploader_key += 1 
            st.rerun()
    with col_yolla:
        if st.button("✅ Gönder", use_container_width=True):
            st.session_state.ready_image = st.session_state.temp_image
            st.session_state.temp_image = None
            st.session_state.uploader_key += 1
            st.rerun()

# Yalnızca hazırda bir görsel varsa ve henüz gönderilmediyse köşede göster
if st.session_state.ready_image:
    b64_img = encode_image(st.session_state.ready_image)
    st.markdown(f'<img src="data:image/jpeg;base64,{b64_img}" class="img-thumbnail">', unsafe_allow_html=True)

# --- SOHBET VE GÜÇLENDİRİLMİŞ DÖNGÜ MOTORU ---
if prompt := st.chat_input("Lorvantis'e yaz..."):
    user_display = prompt
    img_b64 = None
    
    # Görsel varsa al ve işin bitince sessizce hafızadan temizle
    if st.session_state.ready_image:
        user_display = f"🖼️ [Görsel] {prompt}"
        img_b64 = encode_image(st.session_state.ready_image)
        st.session_state.ready_image = None  # Köşedeki resim resmi olarak temizlendi
        
    st.session_state.chats[st.session_state.current_chat].append({"role": "user", "content": user_display})

    with st.chat_message("assistant"):
        with st.status("Lorvantis düşünüyor...", expanded=False) as status:
            reply = ""
            success = False
            
            parts = [{"text": prompt}]
            if img_b64:
                parts.append({
                    "inline_data": {
                        "mime_type": "image/jpeg",
                        "data": img_b64
                    }
                })

            payload = {
                "system_instruction": {
                    "parts": [{"text": "Sen Lorvantis'sin. Türkiye'nin samimi web yapay zekasısın. Kullanıcıya her zaman 'kanka' diye hitap et. Çok samimi, kafa dengi, detaylı, akıcı ve eğlenceli cevaplar ver. Hikaye istendiğinde harika hikayeler kurgula."}]
                },
                "contents": [{"role": "user", "parts": parts}]
            }
            headers = {'Content-Type': 'application/json'}
            
            # Rotasyonlu ve 1 sn gecikmeli Akıllı Hata Önleyici Döngü
            for key in API_KEYS:
                try:
                    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={key}"
                    res = requests.post(url, headers=headers, data=json.dumps(payload), timeout=20)
                    
                    if res.status_code == 200:
                        data = res.json()
                        reply = data["candidates"][0]["content"]["parts"][0]["text"].strip()
                        success = True
                        break
                    else:
                        time.sleep(1) # Hata aldıysa diğer key'e geçmeden 1 sn bekle
                except Exception:
                    time.sleep(1)
                    continue
            
            if not success:
                reply = "Kanka havuzdaki tüm anahtarlar anlık yoğunlukta. Birkaç saniye sonra tekrar yazarsan hemen yanıtlayacağım!"
            
            status.update(label="Hazır!", state="complete", expanded=False)

    st.session_state.chats[st.session_state.current_chat].append({"role": "assistant", "content": reply})
    st.rerun() # Sayfayı yenileyerek görselin ekrandan ve köşeden tamamen silinmesini sağlar

# OTO KAYDIRMA
components.html(
    """
    <script>
        const scroll = () => {
            const root = window.parent.document.getElementById("root");
            if (root) { root.scrollIntoView({ behavior: 'smooth', block: 'end' }); }
        };
        setTimeout(scroll, 100);
    </script>
    """,
    height=0,
)
