import streamlit as st
import requests
import json
import base64
import streamlit.components.v1 as components

# Sayfa ayarları
st.set_page_config(page_title="Lorvantis AI", page_icon="🤖", layout="centered")

# --- CSS: MESAJ BARI VE ARAYÜZ DÜZENLEMELERİ ---
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

# --- VERİTABANI VE HAFIZA ---
if "chats" not in st.session_state:
    st.session_state.chats = {"Varsayılan Sohbet": [{"role": "assistant", "content": "Selam kanka. Ne aramıştın?"}]}
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

# --- YAN MENÜ VE API AYARI ---
with st.sidebar:
    st.title("⚙️ Ayarlar & Sohbet")
    
    # Gemini API Anahtar Girişi
    gemini_key = st.text_input("Gemini API Anahtarı:", type="password", help="Google AI Studio'dan ücretsiz alabilirsin kanka.")
    
    st.markdown("---")
    st.title("🗂️ Sohbetlerin")
    new_chat = st.text_input("Yeni Sohbet Başlığı:")
    if st.button("➕ Yeni Sohbet Aç"):
        if new_chat and new_chat not in st.session_state.chats:
            st.session_state.chats[new_chat] = [{"role": "assistant", "content": f"Selam! {new_chat} konusuna dalalım, dinliyorum kanka."}]
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
                st.session_state.chats = {"Yeni Sohbet": [{"role": "assistant", "content": "Her şeyi sildin kanka, yepyeni bir sayfa!"}]}
                st.session_state.current_chat = "Yeni Sohbet"
        st.rerun()

# --- ANA EKRAN ÜST MENÜ ---
col_title, col_menu = st.columns([8, 1])
with col_title:
    st.title("🤖 Lorvantis AI")
    st.caption("Türkiye’nin Web YapayZekası (Gemini Gücüyle)")
with col_menu:
    st.markdown("<br>", unsafe_allow_html=True)
    with st.popover("⋮"):
        if st.button("🗑️ Sohbeti Sil", use_container_width=True):
            st.session_state.chats[st.session_state.current_chat] = [{"role": "assistant", "content": "Sohbeti tamamen temizledik kanka. Sıradaki soru gelsin!"}]
            st.rerun()

# --- GEÇMİŞ MESAJLARI GÖSTERME ---
for msg in st.session_state.chats[st.session_state.current_chat]:
    st.chat_message(msg["role"]).write(msg["content"])

# --- FOTOĞRAF YÜKLEME ---
with st.popover("➕"):
    tab1, tab2 = st.tabs(["🖼️ Galeriden", "📸 Kamera"])
    with tab1:
        uploaded_file = st.file_uploader("Seç", type=["png", "jpg", "jpeg"], key=f"up_{st.session_state.uploader_key}")
        if uploaded_file:
            st.session_state.temp_image = uploaded_file.getvalue()
    with tab2:
        camera_file = st.camera_input("Çek", key=f"cam_{st.session_state.uploader_key}")
        if camera_file:
            st.session_state.temp_image = camera_file.getvalue()

# ONAY PENCERESİ
if st.session_state.temp_image:
    st.markdown("---")
    st.info("📷 Görsel alındı! Ne yapmak istersin?")
    st.image(st.session_state.temp_image, width=200)
    
    col_iptal, col_yolla = st.columns(2)
    with col_iptal:
        if st.button("❌ İptal Et", use_container_width=True):
            st.session_state.temp_image = None
            st.session_state.uploader_key += 1 
            st.rerun()
    with col_yolla:
        if st.button("✅ Mesajla Yolla", use_container_width=True):
            st.session_state.ready_image = st.session_state.temp_image
            st.session_state.temp_image = None
            st.session_state.uploader_key += 1
            st.rerun()

# KÜÇÜK RESİM (THUMBNAIL)
if st.session_state.ready_image:
    b64_img = encode_image(st.session_state.ready_image)
    st.markdown(
        f'<img src="data:image/jpeg;base64,{b64_img}" class="img-thumbnail">', 
        unsafe_allow_html=True
    )

# --- SOHBET BARI VE REQUESTS TABANLI GEMINI SİSTEMİ ---
if prompt := st.chat_input("Lorvantis'e yaz..."):
    if not gemini_key:
        st.error("Kanka çalışabilmem için sol menüden Gemini API anahtarını girmen gerekiyor!")
    else:
        user_display = prompt
        img_b64 = None
        
        if st.session_state.ready_image:
            user_display = f"🖼️ [Görsel Eklendi] {prompt}"
            img_b64 = encode_image(st.session_state.ready_image)
            st.session_state.ready_image = None 
            
        st.session_state.chats[st.session_state.current_chat].append({"role": "user", "content": user_display})
        st.chat_message("user").write(user_display)

        with st.chat_message("assistant"):
            with st.status("Lorvantis düşünüyor...", expanded=True) as status:
                reply = ""
                try:
                    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={gemini_key}"
                    
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
                            "parts": [{"text": "Sen Lorvantis'sin. Türkiye’nin web yapay zekasısın. Kullanıcıya kesinlikle 'kanka' diye hitap et. Sorulara son derece detaylı, akıcı, net ve doğru cevaplar ver."}]
                        },
                        "contents": [
                            {
                                "role": "user",
                                "parts": parts
                            }
                        ]
                    }

                    headers = {'Content-Type': 'application/json'}
                    res = requests.post(url, headers=headers, data=json.dumps(payload), timeout=30)
                    
                    if res.status_code == 200:
                        data = res.json()
                        reply = data["candidates"][0]["content"]["parts"][0]["text"].strip()
                    else:
                        reply = f"Kanka API hatası ({res.status_code}): Anahtarı doğru girdiğinden emin ol."
                except Exception as e:
                    reply = f"Kanka bir hata oluştu: {str(e)}"
                
                status.update(label="Lorvantis çözdü!", state="complete", expanded=False)

            st.write(reply)
            st.session_state.chats[st.session_state.current_chat].append({"role": "assistant", "content": reply})

# --- OTOMATİK EN AŞAĞI KAYDIRMA ---
components.html(
    """
    <script>
        const scroll = () => {
            const root = window.parent.document.getElementById("root");
            if (root) {
                root.scrollIntoView({ behavior: 'smooth', block: 'end' });
            }
        };
        setTimeout(scroll, 100);
    </script>
    """,
    height=0,
)
