import streamlit as st
import urllib.request
import urllib.parse
import json
import time
import base64
import streamlit.components.v1 as components
from PIL import Image
import io

# Sayfa ayarları
st.set_page_config(page_title="Lorvantis AI", page_icon="🤖", layout="centered")

# --- CSS: MESAJ BARI DÜZENLEMELERİ ---
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
        /* Minik resim önizlemesi tasarımı */
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
    st.session_state.chats = {"Varsayılan Sohbet": [{"role": "assistant", "content": "Selam kanka! Ne arıyoruz, ne soruyorsun?"}]}
if "current_chat" not in st.session_state:
    st.session_state.current_chat = "Varsayılan Sohbet"
if "temp_image" not in st.session_state:
    st.session_state.temp_image = None
if "ready_image" not in st.session_state:
    st.session_state.ready_image = None

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
    st.caption(f"Aktif Oda: {st.session_state.current_chat} | Sınırsız Web & Görsel")
with col_menu:
    st.markdown("<br>", unsafe_allow_html=True)
    with st.popover("⋮"):
        if st.button("🗑️ Sohbeti Sil", use_container_width=True):
            st.session_state.chats[st.session_state.current_chat] = [{"role": "assistant", "content": "Sohbeti tamamen temizledik kanka. Sıradaki soru gelsin!"}]
            st.rerun()

# --- GEÇMİŞ MESAJLARI GÖSTERME ---
for msg in st.session_state.chats[st.session_state.current_chat]:
    st.chat_message(msg["role"]).write(msg["content"])

# --- FOTOĞRAF YÜKLEME VE ONAY PENCERESİ (MODAL SİMÜLASYONU) ---
with st.popover("➕"):
    tab1, tab2 = st.tabs(["🖼️ Galeriden", "📸 Kamera"])
    with tab1:
        uploaded_file = st.file_uploader("Seç", type=["png", "jpg", "jpeg"])
        if uploaded_file:
            st.session_state.temp_image = uploaded_file.getvalue()
    with tab2:
        camera_file = st.camera_input("Çek")
        if camera_file:
            st.session_state.temp_image = camera_file.getvalue()

# Eğer resim çekildiyse/yüklendiyse özel onay ekranı göster
if st.session_state.temp_image:
    st.markdown("---")
    st.info("📷 Görsel alındı! Ne yapmak istersin?")
    st.image(st.session_state.temp_image, width=200)
    
    col_iptal, col_yolla = st.columns(2)
    with col_iptal:
        if st.button("❌ İptal Et", use_container_width=True):
            st.session_state.temp_image = None
            st.rerun()
    with col_yolla:
        if st.button("✅ Mesajla Yolla", use_container_width=True):
            st.session_state.ready_image = st.session_state.temp_image
            st.session_state.temp_image = None
            st.rerun()

# Eğer resim onaylandıysa mesaj barının üstünde küçük thumbnail göster
if st.session_state.ready_image:
    b64_img = encode_image(st.session_state.ready_image)
    st.markdown(
        f'<img src="data:image/jpeg;base64,{b64_img}" class="img-thumbnail">', 
        unsafe_allow_html=True
    )

# --- SOHBET BARI VE YANIT SİSTEMİ ---
if prompt := st.chat_input("Lorvantis'e yaz..."):
    
    # Kullanıcı mesajını hazırla
    user_display = prompt
    img_b64_to_send = None
    
    if st.session_state.ready_image:
        user_display = f"🖼️ [Görsel Eklendi] {prompt}"
        img_b64_to_send = encode_image(st.session_state.ready_image)
        st.session_state.ready_image = None # Gönderdikten sonra temizle
        
    st.session_state.chats[st.session_state.current_chat].append({"role": "user", "content": user_display})
    st.chat_message("user").write(user_display)

    # Yapay zeka API kısmı
    with st.chat_message("assistant"):
        with st.status("Lorvantis web'i tarıyor...", expanded=True) as status:
            reply = ""
            success = False
            
            # API 1. DENEME: Çoklu Model (Resim varsa POST at)
            if img_b64_to_send:
                try:
                    status.update(label="Görsel ve soru analiz ediliyor...", state="running")
                    messages = [
                        {"role": "system", "content": "Sen Lorvantis'sin. Kullanıcıya 'kanka' de. Bu görseli ve soruyu analiz edip en doğru, uzun ve güncel web bilgisini ver."},
                        {"role": "user", "content": [
                            {"type": "text", "text": prompt},
                            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_b64_to_send}"}}
                        ]}
                    ]
                    
                    payload = {"messages": messages, "model": "searchgpt", "search": True}
                    req = urllib.request.Request(
                        "https://text.pollinations.ai/",
                        data=json.dumps(payload).encode('utf-8'),
                        headers={'Content-Type': 'application/json'}
                    )
                    with urllib.request.urlopen(req, timeout=15) as response:
                        if response.getcode() == 200:
                            result = response.read().decode('utf-8').strip()
                            if len(result) > 10:
                                reply = result
                                success = True
                except Exception:
                    pass # Hata alırsak diğer yönteme (sadece metin) geçecek

            # API 2. DENEME: Sağlam GET İsteği (Sadece Text / Resim başarısız olursa)
            if not success:
                status.update(label="Soru webde aranıyor...", state="running")
                try:
                    prefix = "Sen Lorvantis'sin. Kanka diliyle, webden en güncel ve uzun cevabı ver. Soru: "
                    safe_prompt = urllib.parse.quote(prefix + prompt)
                    url = f"https://text.pollinations.ai/{safe_prompt}?search=true"
                    
                    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                    with urllib.request.urlopen(req, timeout=15) as response:
                        if response.getcode() == 200:
                            result = response.read().decode('utf-8').strip()
                            if len(result) > 10:
                                reply = result
                                success = True
                except Exception:
                    pass

            # HİÇBİRİ ÇALIŞMAZSA (Kesin Çözüm / Çökme Önleyici)
            if not success:
                reply = "Kanka şu an internette veya görsel sunucularında devasa bir anlık kopukluk var. Bağlantıyı yeniliyorum, aynı soruyu yazısız veya sadece yazıyla bir saniye sonra tekrar patlatır mısın? 🚀"
                
            status.update(label="Lorvantis çözdü!", state="complete", expanded=False)

        st.write(reply)
        st.session_state.chats[st.session_state.current_chat].append({"role": "assistant", "content": reply})

# --- OTOMATİK EN AŞAĞI KAYDIRMA (JS) ---
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
