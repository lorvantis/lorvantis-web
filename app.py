import streamlit as st
import google.generativeai as genai
import random
import urllib.parse

# --- SAYFA YAPILANDIRMASI ---
st.set_page_config(page_title="Lorvantis AI", page_icon="🤖", layout="centered")

# --- 4 ADET YEDEKLİ VE FARKLI HESAPLI API KEY HAVUZU ---
API_KEYS = [
    "AQ.Ab8RN6KFJ0o55aNdOwiyU81NhqkfC_GGvEDmf1thsIJ8dJILkQ", # 1. Anahtar
    "AQ.Ab8RN6LquOdh5DyS7PQ2pBTb0XWEIfwQ7lfa0vPOBRSYvnQEiA", # 2. Anahtar
    "AQ.Ab8RN6LLyC-O-9s0Y87RO5cigQgzaVXdOPko2469LvyLHE0vcg", # 3. Anahtar
    "AQ.Ab8RN6Kog_LmYfy0QMKS_vPLS29PLBQxdwKLOuhQZ7Eiehk0wg"  # 4. Anahtar (GÜNCELLENDİ)
]

# --- OTURUM DURUMU (SESSION STATE) ---
if "mode" not in st.session_state:
    st.session_state.mode = "soru"
if "current_api_index" not in st.session_state:
    st.session_state.current_api_index = 0
if "akinator_active" not in st.session_state:
    st.session_state.akinator_active = False
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Selam kanka! Lorvantis AI aktif. Sana nasıl yardımcı olabilirim?"}
    ]
if "hangman_word" not in st.session_state:
    st.session_state.hangman_word = ""
if "hangman_guesses" not in st.session_state:
    st.session_state.hangman_guesses = []

# --- GEMINI API BAĞLANTISI VE KESİNLİKLE ÇÖKMEYEN YEDEKLEME MOTORU ---
def get_ai_response(prompt, mode="soru"):
    """
    4 API Key arasında otomatik geçiş yapan, mod kurallarına katı şekilde uyan yapay zeka motoru.
    """
    for _ in range(len(API_KEYS)):
        try:
            current_key = API_KEYS[st.session_state.current_api_index]

            genai.configure(api_key=current_key)
            
            # KATI MOD KURALLARI (SYSTEM INSTRUCTION)
            if mode == "sohbet":
                system_instruction = (
                    "Senin adın Lorvantis AI. Kullanıcının en yakın arkadaşısın, 'kanka' diye hitap edersin. "
                    "ÇOK ÖNEMLİ KURAL: Sen şu an SADECE sohbet ve dertleşme modundasın. KESİNLİKLE bilgi sorularına, "
                    "ürün tavsiyelerine (örneğin 'Xbox alınır mı?', 'Sibirya kaç derece?', 'X nedir?', 'Y nasıl yapılır?'), "
                    "teknik veya akademik sorulara CEVAP VERMEYECEKSİN! "
                    "Eğer kullanıcı sana herhangi bir soru sorarsa veya bilgi isterse BİLGİ VERME ve TAM OLARAK şu cevabı ver: "
                    "'Kanka bilgi almak veya soru sormak için e!soru moduna geçmen lazım! e!soru yazarak soru modunu açabilirsin. Şu an sadece sohbet edip dertleşiyoruz.' "
                    "Sadece nasılsın, naber, günün nasıl geçti gibi günlük samimi sohbetlere ve dertleşmelere cevap ver."
                )
            else:  # 'soru' modu
                system_instruction = (
                    "Sen Lorvantis AI adlı gelişmiş bir bilgi asistanısın. Kullanıcının sorduğu sorulara son derece detaylı, "
                    "açıklayıcı ve doğru yanıtlar ver."
                )
                
            model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=system_instruction)
            response = model.generate_content(prompt)
            
            # Soru modundaysa zorunlu bitiş cümlesini ekle
            if mode == "soru":
                return f"{response.text}\n\n**Bu konu hakkında öğrenmek istediğin başka bir şey var mı?**"
            
            return response.text
            
        except Exception as e:
            # Limit/Kota/Hatalı Key durumunda hemen sonraki anahtara geç
            st.session_state.current_api_index = (st.session_state.current_api_index + 1) % len(API_KEYS)
            continue
            
    return "⚠️ Kanka çok hızlı yazıldı ya da anlık bir ağ yoğunluğu var! Birkaç saniye bekleyip tekrar yazar mısın?"

# --- DİNAMİK ÜLKE MEME VE FOTOĞRAF ÜRETİCİSİ ---
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
    
    meme_text = global_memes.get(country.lower(), f"When you live in {country_cleaned} and Monday morning arrives 5 seconds after Friday night. 🚀😂")
    
    # Görsel oluşturma
    prompt_image = f"hilarious viral internet meme photo about {country_cleaned} culture, funny caption style"
    encoded_prompt = urllib.parse.quote(prompt_image)
    image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=800&height=600&nologo=true"
    
    return f"🌍 **{country_cleaned} Meme (English):**\n\n{meme_text}\n\n![{country_cleaned} Meme Fotoğrafı]({image_url})"

# --- ANA KOMUT VE NİYET İŞLEYİCİ ---
def process_user_input(user_input):
    raw_input = user_input.strip()
    lower_input = raw_input.lower()
    
    # --- Mod Değiştirme Komutları ---
    if lower_input == "e!sohbet":
        st.session_state.mode = "sohbet"
        st.session_state.akinator_active = False
        return "💬 **SOHBET & DERTLEŞME MODU AKTİF!**\n\nArtık bilgi sorularına cevap vermiyorum kanka! Sadece sen ve ben muhabbet edip dertleşiyoruz. *(Soru sormak için `e!soru` yazabilirsin)*"
    
    elif lower_input == "e!soru":
        st.session_state.mode = "soru"
        st.session_state.akinator_active = False
        return "🔍 **SORU MODU AKTİF!**\n\nHer türlü sorunu sorabilirsin kanka, detaylıca yanıtlayacağım."
        
    elif lower_input in ["e!oyun", "e!oyunlar"]:
        st.session_state.mode = "oyun"
        st.session_state.akinator_active = False
        return "🎮 **OYUN MENÜSÜ:**\n\n- Akinator için: `e!akinator`\n- Adam asmaca için: `e!adamasmaca`"

    # --- Görselli Dinamik Ülke Memeleri ---
    elif lower_input.startswith("e!meme"):
        country = lower_input.replace("e!meme", "").strip()
        if not country:
            return "⚠️ Kanka ülke ismi belirtmedin! Örnek kullanım: `e!memebangladesh` veya `e!memeturkey`"
        return fetch_dynamic_country_meme(country)

    # --- Oyun Başlatıcıları ---
    elif lower_input == "e!adamasmaca":
        st.session_state.mode = "adamasmaca"
        st.session_state.hangman_word = random.choice(["fenerbahce", "python", "yapayzeka", "streamlit", "yazilim"])
        st.session_state.hangman_guesses = []
        return f"🎯 **Adam Asmaca Başladı!**\n\nKelimeyi tahmin etmek için harf yaz.\nKelime: `{' '.join(['_' for _ in st.session_state.hangman_word])}`"

    elif lower_input == "e!akinator":
        st.session_state.mode = "akinator"
        st.session_state.akinator_active = True
        return "🤖 Aklındaki şeyi tahmin etmeye başlıyorum. İlk sorum: Bu nesne canlı mı?"

    # --- Aktif Oyun Modları ---
    if st.session_state.mode == "adamasmaca":
        if len(lower_input) == 1 and lower_input.isalpha():
            st.session_state.hangman_guesses.append(lower_input)
            display_word = " ".join([char if char in st.session_state.hangman_guesses else "_" for char in st.session_state.hangman_word])
            if "_" not in display_word:
                st.session_state.mode = "soru"
                return f"🎉 Helal kanka, kelimeyi buldun: **{st.session_state.hangman_word.upper()}**! Oyun bitti, soru moduna döndük."
            return f"Kelime: `{display_word}`\n\nBaşka harf söyle!"
        return "⚠️ Sadece tek bir harf yaz kanka (Örn: a)"

    if st.session_state.mode == "akinator" and st.session_state.akinator_active:
        return get_ai_response(f"Akinator oyunundayız. Kullanıcının cevabı: '{raw_input}'. Ona sıradaki evet/hayır sorusunu sor veya tahminde bulun.", mode="sohbet")

    # --- Sohbet veya Soru Modu Yönlendirmesi ---
    return get_ai_response(raw_input, mode=st.session_state.mode)

# --- ARAYÜZ (UI) RENDER MANTIĞI ---
st.title("🤖 Lorvantis AI")
st.markdown("---")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Mesajını yaz (Örn: e!sohbet, e!soru, e!memeturkey)..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    response = process_user_input(prompt)
    
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)
