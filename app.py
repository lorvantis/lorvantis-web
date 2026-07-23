import streamlit as st
import urllib.request
import urllib.parse
import json
import time
import base64
import streamlit.components.v1 as components

# Sayfa ayarları
st.set_page_config(page_title="Lorvantis AI", page_icon="🤖", layout="centered")

# --- CSS İLE MESAJ BARINA BUTON GÖMME HİLESİ ---
st.markdown("""
    <style>
        /* Mesaj barının sol tarafında buton için boşluk bırak */
        [data-testid="stChatInput"] {
            padding-left: 3rem !important;
        }
        
        /* + Butonunu zorla mesaj barının sol içine sabitle */
        div[data-testid="stPopover"] {
            position: fixed;
            bottom: 2rem;
            left: 1.5rem;
            z-index: 99999;
        }
        
        /* Mobilde ekran daraldığında hizalamayı bozmaması için */
        @media (max-width: 768px) {
            div[data-testid="stPopover"] {
                bottom: 1.5rem;
                left: 1rem;
            }
        }
        
        /* Butonun kendi tasarımını ufaltıp şıklaştırma */
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
    </style>
""", unsafe_allow_html=True)

# --- VERİTABANI VE HAFIZA (SESSION STATE) ---
if "chats" not in st.session_state:
    st.session_state.chats = {"Varsayılan Sohbet": [{"role": "assistant", "content": "Selam kanka! Ne arıyoruz, ne soruyorsun?"}]}
if "current_chat" not in st.session_state:
    st.session_state.current_chat = "Varsayılan Sohbet"

# --- YARDIMCI FONKSİYON: RESMİ BASE64'E ÇEVİRME ---
def encode_image(image_file):
    return base64.b64encode(image_file.getvalue()).decode('utf-8')

# --- YAN MENÜ (SOHBET GEÇMİŞİ VE SİLME) ---
with st.sidebar:
    st.title("🗂️ Sohbetlerin")
    
    # Yeni sohbet ekleme
    new_chat = st.text_input("Yeni Sohbet Başlığı:")
    if st.button("➕ Yeni Sohbet Aç"):
        if new_chat and new_chat not in st.session_state.chats:
            st.session_state.chats[new_chat] = [{"role": "assistant", "content": f"Selam! {new_chat} konusuna dalalım, dinliyorum kanka."}]
            st.session_state.current_chat = new_chat
            st.rerun()
            
    st.markdown("---")
    
    # Sohbetleri listeleme ve X ile silme
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
                
    # Silme işlemini uygula
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

# --- ALT KISIM: ➕ BUTONU (FOTOĞRAF/KAMERA) ---
img_base64 = None

# CSS ile yerini ayarladığımız Popover butonu (Artık solda barın üstünde görünecek)
with st.popover("➕"):
    tab1, tab2 = st.tabs(["🖼️ Galeriden Yükle", "📸 Kamera ile Çek"])
    with tab1:
        uploaded_file = st.file_uploader("Bir fotoğraf seç kanka", type=["png", "jpg", "jpeg"])
    with tab2:
        camera_file = st.camera_input("Buradan fotoğraf çekebilirsin")
    
    if uploaded_file:
        img_base64 = encode_image(uploaded_file)
        st.success("Fotoğraf yüklendi! Şimdi aşağıdan sorunu sorabilirsin.")
    elif camera_file:
        img_base64 = encode_image(camera_file)
        st.success("Fotoğraf çekildi! Şimdi aşağıdan sorunu sorabilirsin.")

# --- SOHBET BARI VE YANIT SİSTEMİ ---
if prompt := st.chat_input("Lorvantis'e bir soru sor veya görsel hakkında bir şey yaz..."):
    # Mesajı ekrana bas
    user_display = prompt
    if img_base64:
        user_display = f"🖼️ [Görsel Eklendi] {prompt}"
        
    st.session_state.chats[st.session_state.current_chat].append({"role": "user", "content": user_display})
    st.chat_message("user").write(user_display)

    # Yapay zeka yanıt kısmı
    with st.chat_message("assistant"):
        with st.status("Lorvantis web'in altını üstüne getiriyor...", expanded=True) as status:
            reply = ""
            success = False
            attempt = 0
            
            while not success and attempt < 3:
                attempt += 1
                status.update(label=f"Lorvantis derin analizde... (Aşama: {attempt})", state="running")
                
                try:
                    system_prompt = "Sen Lorvantis'sin. Türkiye'nin en akıllı web yapay zekasısın. Kullanıcıya 'kanka' diye hitap et, samimi ol. Asla 'bilmiyorum' deme, webde arama yapıp en güncel ve en doğru bilgiyi uzun uzun, detaylıca açıkla."
                    
                    messages = [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": prompt}
                    ]
                    
                    if img_base64:
                        messages[1]["content"] = [
                            {"type": "text", "text": prompt},
                            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_base64}"}}
                        ]
                    
                    payload = {
                        "messages": messages,
                        "model": "searchgpt", 
                        "search": True
                    }
                    
                    data = json.dumps(payload).encode('utf-8')
                    req = urllib.request.Request(
                        "https://text.pollinations.ai/",
                        data=data,
                        headers={'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'}
                    )
                    
                    with urllib.request.urlopen(req, timeout=20) as response:
                        if response.getcode() == 200:
                            result = response.read().decode('utf-8').strip()
                            if result and len(result) > 5:
                                reply = result
                                success = True
                                break
                except Exception as e:
                    time.sleep(1)
                    continue
            
            if not success:
                reply = "Kanka şu an internet hatlarında devasa bir yoğunluk var, sunucular cevap vermekte zorlanıyor. Bu soruyu birazdan tekrar fırlatır mısın bana? 🚀"
                
            status.update(label="Lorvantis çözdü!", state="complete", expanded=False)

        st.write(reply)
        st.session_state.chats[st.session_state.current_chat].append({"role": "assistant", "content": reply})

# --- OTOMATİK EN AŞAĞI KAYDIRMA SİSTEMİ (JS) ---
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
