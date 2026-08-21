import random
import urllib.parse
from google import genai
from google.genai import types
import streamlit as st

# --- SAYFA YAPILANDIRMASI ---
st.set_page_config(page_title="Lorvantis AI", page_icon="🤖", layout="centered")

# --- SENİN AQ. ANAHTARLARIN (Buraya tam ve eksiksiz yapıştır) ---
API_KEYS = [
    
    "AQ.Ab8RN6KFJ0o55aNdOwiyU81NhqkfC_GGvEDmf1thsIJ8dJILkQ",
    "AQ.Ab8RN6LquOdh5DyS7PQ2pBTb0XWEIfwQ7lfa0vPOBRSYvnQEiA",
    "AQ.Ab8RN6LLyC-O-9s0Y87RO5cigQgzaVXdOPko2469LvyLHE0vcg",
    "AQ.Ab8RN6Kog_LmYfy0QMKS_vPLS29PLBQxdwKLOuhQZ7Eiehk0wg",
]

# --- OTURUM DURUMU GÜVENLİK KONTROLÜ ---
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


# --- RESMİ GOOGLE-GENAI SDK MOTORU (AQ. UYUMLU) ---
def get_ai_response(prompt, mode="soru"):
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

  errors = []
  for idx, key in enumerate(API_KEYS]:
    if not key or "..." in key:
      continue
    try:
      # Resmi Google GenAI SDK istemcisi
      client = genai.Client(api_key=key)

      response = client.models.generate_content(
          model="gemini-1.5-flash",
          contents=prompt,
          config=types.GenerateContentConfig(
              system_instruction=system_instruction,
          ),
      )

      reply = response.text
      if mode == "soru":
        return (
            f"{reply}\n\n**Bu konu hakkında öğrenmek istediğin başka bir şey var"
            " mı?**"
        )
      return reply

    except Exception as e:
      errors.append(f"Key {idx + 1} Hata: {str(e)}")
      continue

  return (
      "⚠️ **Sistem Bağlantı Hatası:** Anahtarlar doğrulanamadı.\n\n"
      + " | ".join(errors)
  )


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
    st.session_state.hangman_word = random.choice([
        "fenerbahce",
        "python",
        "yapayzeka",
        "streamlit",
        "yazilim",
    ])
    st.session_state.hangman_guesses = []
    return (
        "🎯 **Adam Asmaca Başladı!**\n\nKelime:"
        f" `{' '.join(['_' for _ in st.session_state.hangman_word])}`"
    )

  if st.session_state.mode == "adamasmaca":
    if len(lower_input) == 1 and lower_input.isalpha():
      if lower_input not in st.session_state.hangman_guesses:
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
