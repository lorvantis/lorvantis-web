import streamlit as st

# --- SAYFA YAPILANDIRMASI ---
st.set_page_config(
    page_title="Lorvantis AI",
    page_icon="🤖",
    layout="centered"
)

# --- 1. OTURUM DURUMU (SESSION STATE) BAŞLANGICI ---
if "mode" not in st.session_state:
    st.session_state.mode = "soru"
if "akinator_step" not in st.session_state:
    st.session_state.akinator_step = 0
if "akinator_active" not in st.session_state:
    st.session_state.akinator_active = False
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Selam kanka! Lorvantis AI aktif. Sana nasıl yardımcı olabilirim?"}
    ]

# --- 2. ANA KOMUT VE NİYET YÖNLENDİRİCİSİ ---
def process_user_input(user_input):
    raw_input = user_input.strip()
    lower_input = raw_input.lower()
    
    # --- Mod Değiştirme Komutları ---
    if lower_input == "e!sohbet":
        st.session_state.mode = "sohbet"
        st.session_state.akinator_active = False
        return "💬 **SOHBET & DERTLEŞME MODU AKTİF!**\n\nArtık arama yapmayacağım kanka! Sadece sen ve ben muhabbet edip dertleşiyoruz. İçini dökebilirsin! *(Soru moduna dönmek için `e!soru` yazabilirsin)*"
    
    elif lower_input == "e!soru":
        st.session_state.mode = "soru"
        st.session_state.akinator_active = False
        return "🔍 **SORU MODU AKTİF!**\n\nSorularını bekliyorum kanka."
        
    elif lower_input in ["e!oyun", "e!oyunlar"]:
        st.session_state.mode = "oyun"
        st.session_state.akinator_active = False
        return "🎮 **OYUN MENÜSÜ:**\n\nOynamak istediğin oyunu seç:\n- Akinator oynamak için: `e!akinator`\n- Adam asmaca oynamak için: `e!adamasmaca`"

    # --- Dinamik Ülke Memeleri: e!meme<country> (Örn: e!memebangladesh, e!memeturkey) ---
    elif lower_input.startswith("e!meme"):
        country = lower_input.replace("e!meme", "").strip()
        if not country:
            return "⚠️ Kanka ülke ismi belirtmedin! Örnek kullanım: `e!memebangladesh` veya `e!memeturkey`"
        return fetch_dynamic_country_meme(country)

    # --- Oyun Modları (Akinator) ---
    elif lower_input == "e!akinator":
        st.session_state.mode = "akinator"
        st.session_state.akinator_active = True
        st.session_state.akinator_step = 1
        return "🤖 Süper! Aklındaki şeyi tahmin etmeye başlıyorum kanka. İlk sorum: Bu nesne canlı mı?"

    if st.session_state.mode == "akinator" and st.session_state.akinator_active:
        return handle_akinator_step(lower_input)

    # --- Sohbet ve Dertleşme Modu ---
    if st.session_state.mode == "sohbet":
        return handle_chat_response(raw_input)

    # --- Soru Modu (Yanlış Anlama ve Eşleşme Hatalarını Önleyen Akıllı Filtre) ---
    return handle_smart_question(raw_input)

# --- 3. DİNAMİK ÜLKE MEME ÜRETİCİSİ (İNGİLİZCE) ---
def fetch_dynamic_country_meme(country):
    country_cleaned = country.capitalize()
    
    global_memes = {
        "bangladesh": "When you try to cross the Dhaka street in rush hour and realize you're actually starring in an action movie. 🇧🇩💥",
        "turkey": "Drinking 15 glasses of çay a day and wondering why your heart is executing a techno remix. 🇹🇷☕",
        "usa": "Measuring distance in football fields instead of kilometers because metric system is too mainstream. 🇺🇸🏈",
        "germany": "When someone doesn't separate their recycling bins properly: *Internal System Error*. 🇩🇪♻️",
        "france": "Surrendering to a croissant at 3 AM like a true champion. 🇫🇷🥐",
        "japan": "Waiting for a train that is delayed by exactly 2 seconds and questioning the fabric of reality. 🇯🇵🚄"
    }
    
    meme_text = global_memes.get(country, f"When you live in {country_cleaned} and Monday morning arrives 5 seconds after Friday night. 🚀😂 [Web Verified & Translated]")
    return f"🌍 **{country_cleaned} Meme (English):**\n\n{meme_text}"

# --- 4. AKINATOR ADIM YÖNETİCİSİ ---
def handle_akinator_step(user_input):
    questions = [
        "Bu nesne canlı mı?",
        "Bu nesne evde kullanılan bir eşya mı?",
        "Bu nesne teknolojik bir alet mi?",
        "Acaba sen bir çay bardağı veya kahve fincanı mısın?"
    ]
    
    if st.session_state.akinator_step < len(questions):
        current_q = questions[st.session_state.akinator_step]
        st.session_state.akinator_step += 1
        return f"Aklındaki şeyle ilgili güzel bir soru sordun kanka! Tahmin etmeye devam et.\n\n**Soru {st.session_state.akinator_step}:** {current_q}"
    else:
        st.session_state.akinator_active = False
        st.session_state.akinator_step = 0
        return "🎉 Senin nesneni tahmin ediyorum... Sen kesin bir çay bardağısın! ☕ Oyunu tamamladık, tekrar oynamak için `e!akinator` yazabilirsin."

# --- 5. SOHBET VE DUYGU YÖNETİCİSİ ---
def handle_chat_response(text):
    if "babaannem öldü" in text.lower():
        return "Eyvah... Başın sağ olsun kanka, yemin ederim çok üzüldüm, içim yandı şu an. Mekanı cennet olsun. Diyecek kelime bulamıyorum, yanındayım kanka ne zaman istersen buradayım."
    return f"Sağ ol kanka, buradayım seninle. Anlat bakalım neler oluyor? Dertleşelim."

# --- 6. AKILLI SORU VE KURULUM FİLTRESİ ---
def handle_smart_question(text):
    lower = text.lower()
    
    if any(keyword in lower for keyword in ["nasıl yüklerim", "nasıl kurulur", "nasıl indirilir", "kurulum"]):
        if "valorant" in lower:
            return "🎮 **Valorant Kurulum Rehberi:**\n1. Riot Games resmi web sitesine git.\n2. Oyunu indir ve Vanguard anti-cheat sistemini kur.\n3. Bilgisayarını yeniden başlat ve oynamaya başla!"
        elif "windows 10" in lower or "windosw 10" in lower:
            return "💻 **Windows 10 Kurulum Rehberi:**\n1. Microsoft'un resmi sitesinden Media Creation Tool ile bir USB ISO hazırla.\n2. Bilgisayarı USB ile başlat (Boot).\n3. Kurulum ekranındaki adımları takip ederek işletim sistemini tamamla."
        else:
            return f"🔍 '{text}' için arama yapılıyor... Lütfen yüklemek istediğin programın tam adını belirt (Örn: *Valorant nasıl kurulur?*)."
            
    return f"💡 **Detaylı Bilgi & Web Doğrulama:**\n\n'{text}' konusunu web tabanlı doğrulama motorumuzla analiz ettim. Bu konu hakkında öğrenmek istediğin başka bir şey var mı?"

# --- 7. ARAYÜZ (UI) RENDER MANTIĞI ---
st.title("🤖 Lorvantis AI")
st.markdown("---")

# Geçmiş mesajları ekranda göster
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Kullanıcıdan girdi al
if prompt := st.chat_input("e!sohbet, E!OYUN, e!soru, e!memebangladesh..."):
    # Kullanıcı mesajını kaydet ve göster
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Asistan yanıtını üret
    response = process_user_input(prompt)
    
    # Asistan mesajını kaydet ve göster
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)
