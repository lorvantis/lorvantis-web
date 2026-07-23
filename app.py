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

# --- YAN MENÜ ---
with st.sidebar:
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
    st.caption("Türkiye’nin Web YapayZekası")
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

# --- SOHBET BARI VE YANIT SİSTEMİ ---
if prompt := st.chat_input("Lorvantis'e yaz..."):
    
    user_display = prompt
    img_b64_to_send = None
    
    if st.session_state.ready_image:
        user_display = f"🖼️ [Görsel Eklendi] {prompt}"
        img_b64_to_send = encode_image(st.session_state.ready_image)
        st.session_state.ready_image = None 
        
    st.session_state.chats[st.session_state.current_chat].append({"role": "user", "content": user_display})
    st.chat_message("user").write(user_display)

    with st.chat_message("assistant"):
        with st.status("Lorvantis yanıtı hazırlıyor...", expanded=True) as status:
            reply = ""
            success = False
            
            # --- 1. AKILLI YEREL SELAMLAŞMA VE TEŞEKKÜR KONTROLÜ ---
            clean_prompt = prompt.lower().strip(".,!?")
            greetings = ["selam", "slm", "merhaba", "mrb", "selamın aleyküm", "selamun aleyküm", "sa", "aleykümselam"]
            thanks = ["tşk", "teşekkürler", "teşekkür ederim", "sağol", "sagol", "teşekkür", "eyvallah"]
            
            if not img_b64_to_send:
                if clean_prompt in greetings:
                    reply = "Aleykümselam kanka, hoş geldin! Nasılsın, ne var ne yok, nasıl yardımcı olabilirim?"
                    success = True
                elif clean_prompt in thanks:
                    reply = "Rica ederim kanka, ne demek! Başka bir sorun varsa buradayım."
                    success = True
            
            # --- 2. HIZLI GPT / OPENAI BAĞLANTISI (TEK DENEME, ANINDA YANIT) ---
            if not success:
                headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
                try:
                    if img_b64_to_send:
                        payload = {
                            "messages": [
                                {"role": "system", "content": "Sen Lorvantis'sin. Türkiye’nin web yapay zekasısın. Kullanıcıya 'kanka' de. Bu görseli ve soruyu analiz edip en doğru ve detaylı cevabı ver."},
                                {"role": "user", "content": [
                                    {"type": "text", "text": prompt},
                                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_b64_to_send}"}}
                                ]}
                            ],
                            "model": "openai"
                        }
                    else:
                        payload = {
                            "messages": [
                                {"role": "system", "content": "Sen Lorvantis'sin. Türkiye’nin web yapay zekasısın. Kullanıcıya 'kanka' de ve soruya detaylı, akıcı, web destekli cevap ver."},
                                {"role": "user", "content": prompt}
                            ],
                            "model": "openai"
                        }
                    
                    res = requests.post("https://text.pollinations.ai/", json=payload, headers=headers, timeout=12)
                    
                    if res.status_code == 200:
                        result = res.text.strip()
                        if result and len(result) > 2:
                            reply = result
                            success = True
                except Exception:
                    pass
            
            # --- 3. GÜVENLİ YEDEK ---
            if not success:
                reply = f"Kanka şu an sunucu anlık yoğunluk verdi ama bağlantı hazır! Soruyu bir kez daha gönderdiğinde direkt akacak: {prompt}"
            
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
