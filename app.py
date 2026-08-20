import random
import urllib.parse
import requests
import streamlit as st

# --- SAYFA YAPILANDIRMASI ---
st.set_page_config(page_title="Lorvantis AI", page_icon="🤖", layout="centered")

# --- SENİN 4 ADET API KEY'İN ---
API_KEYS = [
    "AQ.Ab8RN6KFJ0o55aNdOwiyU81NhqkfC_GGvEDmf1thsIJ8dJILkQ",
    "AQ.Ab8RN6LquOdh5DyS7PQ2pBTb0XWEIfwQ7lfa0vPOBRSYvnQEiA",
    "AQ.Ab8RN6LLyC-O-9s0Y87RO5cigQgzaVXdOPko2469LvyLHE0vcg",
    "AQ.Ab8RN6Kog_LmYfy0QMKS_vPLS29PLBQxdwKLOuhQZ7Eiehk0wg",
]

# --- OTURUM DURUMU ---
if "mode" not in st.session_state:
  st.session_state.mode = "soru"
if "messages" not in st.session_state:
  st.session_state.messages = [{
      "role": "assistant",
      "content": "Selam kanka! Lorvantis AI aktif. Sana nasıl yardımcı olabilirim?",
  }]
if "hangman_word" not in st.session_state:
  st.session_state.hangman_word = ""
if "hangman_guesses" not in st.session_state:
  st.session_state.hangman_guesses = []


# --- GEMINI REST API İSTEK MOTORU (BEARER TOKEN DESTEKLİ) ---
def get_ai_response(prompt, mode="soru"):
  url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
  errors = []

  if mode == "sohbet":
    system_instruction = (
        "Senin adın Lorvantis AI. Kullanıcının en yakın arkadaşısın, 'kanka'"
        " diye hitap edersin. ÇOK ÖNEMLİ KURAL: Sen şu an SADECE sohbet ve"
        " dertleşme modundasın. KESİNLİKLE bilgi sorularına veya akademik"
        " sorulara CEVAP VERMEYECEKSİN! Eğer kullanıcı soru sorarsa BİLGİ VERME"
        " ve TAM OLARAK şu cevabı ver: 'Kanka bilgi almak veya soru sormak için"
        " e!soru moduna geçmen lazım!'"
    )
  else:
    system_instruction = (
        "Sen Lorvantis AI adlı gelişmiş bir bilgi asistanısın. Kullanıcının"
        " sorduğu sorulara son derece detaylı, açıklayıcı ve doğru yanıtlar ver."
    )

  payload = {
      "contents": [{"role": "user", "parts": [{"text": prompt}]}],
      "systemInstruction": {"parts": [{"text": system_instruction}]},
  }

  for idx, key in enumerate(API_KEYS):
    if not key:
      continue

    # AQ. tokenlarını doğru tanıyan Bearer yetkilendirme başlığı
    headers_bearer = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {key}",
    }

    try:
      resp = requests.post(
          url, headers=headers_bearer, json=payload, timeout=15
      )
      if resp.status_code == 200:
        data = resp.json()
        reply = data["candidates"][0]["content"]["parts"][0]["text"]
        if mode == "soru":
          return (
              f"{reply}\n\n**Bu konu hakkında öğrenmek istediğin başka bir şey"
              " var mı?**"
          )
        return reply

      # Yedek yöntem: x-goog-api-key başlığı
      headers_alt = {"Content-Type": "application/json", "x-goog-api-key": key}
      resp_alt = requests.post(url, headers=headers_alt, json=payload, timeout=15)
      if resp_alt.status_code == 200:
        data = resp_alt.json()
        reply = data["candidates"][0]["content"]["parts"][0]["text"]
        if mode == "soru":
          return (
              f"{reply}\n\n**Bu konu hakkında öğrenmek istediğin başka bir şey"
              " var mı?**"
          )
        return reply

      errors.append(f"❌ Key {idx + 1} Yanıtı: {resp.text}")
    except Exception as e:
      errors.append(f"❌ Key {idx + 1} Bağlantı Hatası: {str(e)}")

  return "⚠️ **Sistem Bağlantı Hatası:**\n\n" + "\n\n".join(errors)


# --- DİNAMİK ÜLKE MEME ÜRETİCİSİ ---
def fetch_dynamic_country_meme(country):
  country_cleaned = country.capitalize()
  global_memes = {
      "turkey": (
          "Drinking 15 glasses of çay a day and wondering why your heart is"
          " executing a techno remix. 🇹🇷☕"
      ),
      "usa": (
          "Measuring distance in football fields instead of kilometers because"
          " metric system is too mainstream. 🇺🇸🏈"
      ),
  }
  meme_text = global_memes.get(
      country.lower(), f"Living in {country_cleaned} be like... 🚀😂"
  )
  prompt_image = f"hilarious viral internet meme photo about {country_cleaned} culture, funny caption style"
  encoded_prompt = urllib.parse.quote(prompt_image)
  image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=800&height=600&nologo=true"
  return (
      f"🌍 **{country_cleaned} Meme:**\n\n{meme_text}\n\n![Meme"
      f" Fotoğrafı]({image_url})"
  )


# --- ANA İŞLEYİCİ MANTIK ---
def process_user_input(user_input):
  raw_input = user_input.strip()
  lower_input = raw_input.lower()

  greetings = ["sa", "s.a", "s.a.", "selam", "merhaba", "heyy", "hey"]
  if lower_input in greetings:
    return "Aleykümselam kanka! Naber, nasıl yardımcı olabilirim?"

  if lower_input == "e!sohbet":
    st.session_state.mode = "sohbet"
    return "💬 **SOHBET & DERTLEŞME MODU AKTİF!**\n\nSadece muhabbet ediyoruz."

  elif lower_input == "e!soru":
    st.session_state.mode = "soru"
    return (
        "🔍 **SORU MODU AKTİF!**\n\nHer türlü sorunu sorabilirsin kanka,"
        " yanıtlamaya hazırım."
    )

  elif lower_input in ["e!oyun", "e!oyunlar"]:
    st.session_state.mode = "oyun"
    return "🎮 **OYUN MENÜSÜ:**\n\n- Adam asmaca için: `e!adamasmaca`"

  elif lower_input == "e!turkishmeme":
    return fetch_dynamic_country_meme("turkey")

  elif lower_input == "e!englishmeme":
    return fetch_dynamic_country_meme("usa")

  elif lower_input == "e!adamasmaca":
    st.session_state.mode = "adamasmaca"
    st.session_state.hangman_word = random.choice(
        ["fenerbahce", "python", "yapayzeka", "streamlit", "yazilim"]
    )
    st.session_state.hangman_guesses = []
    return (
        "🎯 **Adam Asmaca Başladı!**\n\nKelime:"
        f" `{' '.join(['_' for _ in st.session_state.hangman_word])}`"
    )

  if st.session_state.mode == "adamasmaca":
    if len(lower_input) == 1 and lower_input.isalpha():
      st.session_state.hangman_guesses.append(lower_input)
      display_word = " ".join([
          char if char in st.session_state.hangman_guesses else "_"
          for char in st.session_state.hangman_word
      ])
      if "_" not in display_word:
        st.session_state.mode = "soru"
        return (
            "🎉 Helal kanka, kelimeyi buldun:"
            f" **{st.session_state.hangman_word.upper()}**! Soru moduna geçtik."
        )
      return f"Kelime: `{display_word}`"
    return "⚠️ Sadece tek bir harf yaz kanka."

  return get_ai_response(raw_input, mode=st.session_state.mode)


# --- STREAMLIT ARAYÜZÜ ---
st.title("🤖 Lorvantis AI")
st.markdown("---")

for message in st.session_state.messages:
  with st.chat_message(message["role"]):
    st.markdown(message["content"])

if prompt := st.chat_input("Mesajını yaz (Örn: e!sohbet, e!soru)..."):
  st.session_state.messages.append({"role": "user", "content": prompt})
  with st.chat_message("user"):
    st.markdown(prompt)

  response = process_user_input(prompt)
  st.session_state.messages.append({"role": "assistant", "content": response})
  with st.chat_message("assistant"):
    st.markdown(response)
