import random
import urllib.parse
import google.generativeai as genai
import streamlit as st

# --- SAYFA YAPILANDIRMASI ---
st.set_page_config(page_title="Lorvantis AI", page_icon="🤖", layout="centered")

# --- 4 ADET DAHİLİ API KEY HAVUZU ---
API_KEYS = [
    "AQ.Ab8RN6KFJ0o55aNdOwiyU81NhqkfC_GGvEDmf1thsIJ8dJILkQ",
    "AQ.Ab8RN6LquOdh5DyS7PQ2pBTb0XWEIfwQ7lfa0vPOBRSYvnQEiA",
    "AQ.Ab8RN6LLyC-O-9s0Y87RO5cigQgzaVXdOPko2469LvyLHE0vcg",
    "AQ.Ab8RN6Kog_LmYfy0QMKS_vPLS29PLBQxdwKLOuhQZ7Eiehk0wg",
]

# --- OTURUM DURUMU (SESSION STATE) ---
if "mode" not in st.session_state:
  st.session_state.mode = "soru"
if "akinator_active" not in st.session_state:
  st.session_state.akinator_active = False
if "messages" not in st.session_state:
  st.session_state.messages = [{
      "role": "assistant",
      "content": (
          "Selam kanka! Lorvantis AI aktif. Sana nasıl yardımcı olabilirim?"
      ),
  }]
if "hangman_word" not in st.session_state:
  st.session_state.hangman_word = ""
if "hangman_guesses" not in st.session_state:
  st.session_state.hangman_guesses = []


# --- GEMINI API BAĞLANTISI VE TEŞHİS MOTORU ---
def get_ai_response(prompt, mode="soru"):
  errors = []
  for idx, key in enumerate(API_KEYS):
    if not key:
      continue
    try:
      genai.configure(api_key=key)

      # KATI MOD KURALLARI (SYSTEM INSTRUCTION)
      if mode == "sohbet":
        system_instruction = (
            "Senin adın Lorvantis AI. Kullanıcının en yakın arkadaşısın, 'kanka'"
            " diye hitap edersin. ÇOK ÖNEMLİ KURAL: Sen şu an SADECE sohbet ve"
            " dertleşme modundasın. KESİNLİKLE bilgi sorularına, teknik veya"
            " akademik sorulara CEVAP VERMEYECEKSİN! Eğer kullanıcı soru"
            " sorarsa BİLGİ VERME ve TAM OLARAK şu cevabı ver: 'Kanka bilgi"
            " almak veya soru sormak için e!soru moduna geçmen lazım! e!soru"
            " yazarak soru modunu açabilirsin. Şu an sadece sohbet edip"
            " dertleşiyoruz.'"
        )
      else:  # 'soru' modu
        system_instruction = (
            "Sen Lorvantis AI adlı gelişmiş bir bilgi asistanısın. Kullanıcının"
            " sorduğu sorulara son derece detaylı, açıklayıcı ve doğru yanıtlar"
            " ver."
        )

      model = genai.GenerativeModel(
          "gemini-1.5-flash", system_instruction=system_instruction
      )
      response = model.generate_content(prompt)

      if mode == "soru":
        return (
            f"{response.text}\n\n**Bu konu hakkında öğrenmek istediğin başka"
            " bir şey var mı?**"
        )

      return response.text

    except Exception as e:
      errors.append(f"❌ Key {idx + 1} Hatası: {str(e)}")
      continue

  # Hata oluşursa arkada ne olduğunu doğrudan ekrana yazdırır
  return "⚠️ **Sistem Bağlantı Hatası:**\n\n" + "\n\n".join(errors)


# --- DİNAMİK ÜLKE MEME ÜRETİCİSİ ---
def fetch_dynamic_country_meme(country):
  country_cleaned = country.capitalize()

  global_memes = {
      "bangladesh": (
          "When you try to cross the Dhaka street in rush hour and realize"
          " you're actually starring in an action movie. 🇧🇩💥"
      ),
      "turkey": (
          "Drinking 15 glasses of çay a day and wondering why your heart is"
          " executing a techno remix. 🇹🇷☕"
      ),
      "usa": (
          "Measuring distance in football fields instead of kilometers because"
          " metric system is too mainstream. 🇺🇸🏈"
      ),
      "germany": (
          "When someone doesn't separate their recycling bins properly:"
          " *Internal System Error*. 🇩🇪♻️"
      ),
      "france": "Surrendering to a croissant at 3 AM like a true champion. 🇫🇷🥐",
      "japan": (
          "Waiting for a train that is delayed by exactly 2 seconds and"
          " questioning the fabric of reality. 🇯🇵🚄"
      ),
  }

  meme_text = global_memes.get(
      country.lower(),
      f"When you live in {country_cleaned} and Monday morning arrives 5 seconds"
      " after Friday night. 🚀😂",
  )

  prompt_image = (
      f"hilarious viral internet meme photo about {country_cleaned} culture,"
      " funny caption style"
  )
  encoded_prompt = urllib.parse.quote(prompt_image)
  image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=800&height=600&nologo=true"

  return (
      f"🌍 **{country_cleaned} Meme (English):**\n\n{meme_text}\n\n![{country_cleaned}"
      f" Meme Fotoğrafı]({image_url})"
  )


# --- ANA İŞLEYİCİ MANTIK ---
def process_user_input(user_input):
  raw_input = user_input.strip()
  lower_input = raw_input.lower()

  # 1. Selamlaşma Filtresi (API'ye gitmez)
  greetings = [
      "sa",
      "s.a",
      "s.a.",
      "selam",
      "selamunaleykum",
      "selamünaleyküm",
      "merhaba",
      "heyy",
      "hey",
  ]
  if lower_input in greetings:
    return "Aleykümselam kanka! Naber, nasıl yardımcı olabilirim?"

  # 2. Mod Değiştiriciler
  if lower_input == "e!sohbet":
    st.session_state.mode = "sohbet"
    st.session_state.akinator_active = False
    return (
        "💬 **SOHBET & DERTLEŞME MODU AKTİF!**\n\nArtık bilgi sorularına cevap"
        " vermiyorum kanka! Sadece muhabbet ediyoruz."
    )

  elif lower_input == "e!soru":
    st.session_state.mode = "soru"
    st.session_state.akinator_active = False
    return (
        "🔍 **SORU MODU AKTİF!**\n\nHer türlü sorunu sorabilirsin kanka,"
        " yanıtlamaya hazırım."
    )

  elif lower_input in ["e!oyun", "e!oyunlar"]:
    st.session_state.mode = "oyun"
    st.session_state.akinator_active = False
    return (
        "🎮 **OYUN MENÜSÜ:**\n\n- Akinator için: `e!akinator`\n- Adam asmaca"
        " için: `e!adamasmaca`"
    )

  # 3. Görselli Memeler
  elif lower_input.startswith("e!meme"):
    country = lower_input.replace("e!meme", "").strip()
    if not country:
      return "⚠️ Kanka ülke ismi belirtmedin! Örn: `e!memeturkey`"
    return fetch_dynamic_country_meme(country)

  # 4. Oyun Başlatıcılar
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

  elif lower_input == "e!akinator":
    st.session_state.mode = "akinator"
    st.session_state.akinator_active = True
    return (
        "🤖 Aklındaki şeyi tahmin etmeye başlıyorum. İlk sorum: Bu nesne canlı"
        " mı?"
    )

  # 5. Oyun İç Mantıkları
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

  if st.session_state.mode == "akinator" and st.session_state.akinator_active:
    return get_ai_response(
        "Akinator oyunundayız. Kullanıcının cevabı: "
        f"'{raw_input}'. Ona sıradaki evet/hayır sorusunu sor veya tahminde"
        " bulun.",
        mode="sohbet",
    )

  # 6. Genel Yapay Zeka Cevabı
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
