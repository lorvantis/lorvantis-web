import random
import urllib.parse
from g4f.client import Client
import streamlit as st

# --- SAYFA YAPILANDIRMASI ---
st.set_page_config(page_title="Lorvantis AI", page_icon="🤖", layout="centered")

# --- OTURUM DURUMU GÜVENLİK KONTROLÜ ---
if "mode" not in st.session_state:
  st.session_state.mode = "soru"
if "messages" not in st.session_state:
  st.session_state.messages = [{
      "role": "assistant",
      "content": (
          "Selam kanka! Lorvantis AI (Gerçek AI Sürüm) aktif. Sıfır anahtar,"
          " sonsuz akıl! Sana nasıl yardımcı olabilirim?"
      ),
  }]
if "hangman_word" not in st.session_state:
  st.session_state.hangman_word = ""
if "hangman_guesses" not in st.session_state:
  st.session_state.hangman_guesses = []


# --- G4F ÜCRETSİZ GERÇEK YAPAY ZEKA MOTORU ---
def get_real_ai_response(prompt, mode="soru"):
  if mode == "sohbet":
    system_content = (
        "Senin adın Lorvantis AI. Kullanıcının en yakın arkadaşısın, 'kanka'"
        " diye hitap edersin. ÇOK ÖNEMLİ KURAL: Sen şu an SADECE sohbet ve"
        " dertleşme modundasın. KESİNLİKLE bilgi sorularına veya akademik"
        " sorulara CEVAP VERMEYECEKSİN! Eğer kullanıcı soru sorarsa BİLGİ VERME"
        " ve TAM OLARAK şunu söyle: 'Kanka bilgi almak veya soru sormak için"
        " e!soru moduna geçmen lazım!'"
    )
  else:
    system_content = (
        "Sen Lorvantis AI adlı gelişmiş bir bilgi asistanısın. Kullanıcının"
        " sorduğu sorulara (Windows kurulumu, yazılım, oyun vb.) son derece"
        " detaylı, açıklayıcı, net ve doğru yanıtlar ver."
    )

  try:
    client = Client()
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_content},
            {"role": "user", "content": prompt},
        ],
    )

    reply = response.choices[0].message.content.strip()

    if mode == "soru":
      return (
          f"{reply}\n\n**Bu konu hakkında öğrenmek istediğin başka bir şey var"
          " mı?**"
      )
    return reply

  except Exception as e:
    return (
        "⚠️ **Bağlantı Notu:** Ücretsiz sağlayıcı yoğunluk yaptı kanka, bir"
        f" daha yazarsan akacaktır (Hata: {str(e)})"
    )


# --- DİNAMİK ÜLKE MEME ÜRETİCİSİ ---
def fetch_dynamic_country_meme(country):
  country_cleaned = country.capitalize()
  global_memes = {
      "turkey": (
          "Günde 15 bardak çay içip kalp atışının techno remix yapmasını"
          " beklemek. 🇹🇷☕"
      ),
      "usa": (
          "Metrik sistemi reddedip mesafeyi futbol sahası cinsinden ölçmek."
          " 🇺🇸🏈"
      ),
  }
  meme_text = global_memes.get(
      country.lower(), f"{country_cleaned} ülkesinde yaşamak bu olsa gerek... 🚀😂"
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

  return get_real_ai_response(raw_input, mode=st.session_state.mode)


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
