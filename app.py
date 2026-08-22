import random
import urllib.parse
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
          "Selam kanka! Lorvantis AI (Yerel Canavar Sürüm) aktif. Hiçbir API"
          " hatası yok, taştan stabil! Sana nasıl yardımcı olabilirim?"
      ),
  }]
if "hangman_word" not in st.session_state:
  st.session_state.hangman_word = ""
if "hangman_guesses" not in st.session_state:
  st.session_state.hangman_guesses = []


# --- YEREL AKILLI YANIT MOTORU (SIFIR API / SIIR HATA) ---
def get_local_ai_response(prompt, mode="soru"):
  p = prompt.lower()

  if mode == "sohbet":
    return (
        "Kanka şu an dertleşme modundayız! Anlat bakalım, ne var ne yok, günün"
        " nasıl geçiyor?"
    )

  # Yerel akıllı anahtar kelime eşleştirme ve cevap sistemi
  if (
      "python" in p
      or "kod" in p
      or "hata" in p
      or "streamlit" in p
      or "yazılım" in p
  ):
    reply = (
        "Yazılım ve kodlama işlerinde en önemli kural sabırlı olmaktır"
        " kanka. Karşılaştığın hataları (özellikle terminal çıktılarını)"
        " dikkatlice okursan çözüm kendiliğinden ortaya çıkar. Python ve"
        " Streamlit ikilisiyle harika projeler çıkarabilirsin, vazgeçmek yok!"
    )
  elif (
      "fenerbahçe" in p
      or "fener" in p
      or "maç" in p
      or "kadıköy" in p
      or "futbol" in p
  ):
    reply = (
        "Reis fenerliyiz sonuna kadar! Tribünlerin coşkusu, o ruh bambaşka."
        " Sahada kim olursa olsun ruhunu koyduğunda bu iş biter."
    )
  elif "nasılsın" in p or "naber" in p:
    reply = (
        "Elhamdülillah kanka, yerel motorla çalışıyorum, kafam rahat, sıfır"
        " ping, sıfır hata! Sen nasılsın?"
    )
  elif "lorvantis" in p:
    reply = (
        "Lorvantis AI, dış dünyanın api kazıklarından kaçıp kendi öz"
        " sunucusunda (lokalde) kusursuzca koşan en kral yapay zekadır kanka!"
    )
  else:
    reply = (
        f"'{prompt}' konusuna gelirsek kanka; bu meseleyi mantıksal olarak"
        " ele aldığımızda temel adımları takip etmek en güvenlisidir. Detaylı"
        " bir araştırma veya farklı bir açıdan bakmak istersen adım adım"
        " çözeriz!"
    )

  if mode == "soru":
    return f"{reply}\n\n**Bu konu hakkında öğrenmek istediğin başka bir şey var mı?**"
  return reply


# --- DİNAMİK ÜLKE MEME ÜRETİCİSİ (Görsel API'si çalışır durumda) ---
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

  return get_local_ai_response(raw_input, mode=st.session_state.mode)


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
