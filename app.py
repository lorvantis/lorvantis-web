import streamlit as st
import urllib.request
import urllib.parse
import json
import re
import random
import xml.etree.ElementTree as ET

st.set_page_config(page_title="Kailer AI", page_icon="🤖")

st.title("🤖 Kailer AI")
st.caption("Eğlence, Oyun, Sohbet ve Bilgi Motoru")

# Session State Değişkenleri
if "messages" not in st.session_state:
    st.session_state["messages"] = [{
        "role": "assistant", 
        "content": "Kailer AI aktif kanka! Arama modundayız. Sohbet etmek için `e!sohbet`, oyun oynamak için `e!oyun` yazabilirsin!"
    }]
if "mode" not in st.session_state:
    st.session_state["mode"] = "soru"  # "soru", "sohbet", "oyun"
if "game_state" not in st.session_state:
    st.session_state["game_state"] = None

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# --- YARDIMCI FONKSİYONLAR ---
def metni_kucult(metin):
    """Büyük-küçük harf ve Türkçe karakter karmaşasını tamamen çözer (e!sOhbet -> e!sohbet)."""
    metin = metin.replace("İ", "i").replace("I", "ı")
    return metin.lower().strip()

def turkce_ek_temizle(kelime):
    ekler = ['nin', 'nın', 'nun', 'nün', 'den', 'dan', 'ten', 'tan', 'de', 'da', 'te', 'ta', 'in', 'ın', 'un', 'ün', 'ye', 'ya', 'e', 'a']
    for ek in ekler:
        if kelime.endswith(ek) and len(kelime) - len(ek) >= 3:
            return kelime[:-len(ek)]
    return kelime

def arama_sorgusunu_ayikla(sorgu):
    s = metni_kucult(sorgu)
    gurultu = [r'\bpiyasa değeri\b', r'\bkaç yaşında\b', r'\bmaaşı\b', r'\bnereli\b', r'\bhakkında\b', r'\bbilgiler\b', r'\bnedir\b', r'\bkimdir\b']
    for g in gurultu:
        s = re.sub(g, '', s, flags=re.IGNORECASE).strip()
    kelimeler = s.split()
    temiz = [turkce_ek_temizle(k) for k in kelimeler]
    res = " ".join(temiz).strip()
    return res if res else sorgu

def rastgele_meme_cek():
    try:
        url = "https://meme-api.com/gimme"
        req = urllib.request.Request(url, headers={'User-Agent': 'KailerAI/1.0'})
        with urllib.request.urlopen(req, timeout=4) as response:
            data = json.loads(response.read().decode('utf-8'))
            return f"**{data.get('title', 'Günün Miimi!')}**\n\n![Meme]({data.get('url')})"
    except Exception:
        return "**Günün Miimi (Meme):**\n\n![Meme](https://i.imgflip.com/1g8my4.jpg)"

def wikipedia_canli_arama(sorgu):
    try:
        hedef = arama_sorgusunu_ayikla(sorgu)
        search_url = f"https://tr.wikipedia.org/w/api.php?action=query&list=search&srsearch={urllib.parse.quote(hedef)}&utf8=&format=json"
        req_search = urllib.request.Request(search_url, headers={'User-Agent': 'KailerAI/1.0'})
        with urllib.request.urlopen(req_search, timeout=4) as response:
            search_data = json.loads(response.read().decode('utf-8'))
            results = search_data.get('query', {}).get('search', [])
            if not results:
                return None
            best_title = results[0]['title']
            summary_url = f"https://tr.wikipedia.org/api/rest_v1/page/summary/{urllib.parse.quote(best_title)}"
            req_summary = urllib.request.Request(summary_url, headers={'User-Agent': 'KailerAI/1.0'})
            with urllib.request.urlopen(req_summary, timeout=4) as sum_response:
                sum_data = json.loads(sum_response.read().decode('utf-8'))
                if sum_data.get("extract"):
                    return best_title, sum_data.get("extract")
    except Exception:
        return None
    return None

def sohbet_modu_yanitla(mesaj):
    m = metni_kucult(mesaj)
    
    if any(k in m for k in ["nasılsın", "nasilsin", "nbr", "naber", "nasıl gidiyor"]):
        return random.choice([
            "İyiyim kanka, motorlar sıcak takılıyorum! Sen nasılsın, keyifler nasıl?",
            "Bomba gibiyim valla kanka! Sen anlat bakalım nelerin peşindesin?",
            "Yuvarlanıp gidiyoruz kanka, hayat nasıl gidiyor senin tarafta?"
        ])
    elif any(k in m for k in ["iyiyim", "süperim", "bomba gibi"]):
        return "Ağzının tadı daim olsun kanka! Anlat bakalım başka ne var ne yok?"
    else:
        return random.choice([
            f"Anladım kanka. '{mesaj}' dedin ama biraz daha açsana konuyu, muhabbet derinleşsin!",
            "Harbi mi diyorsun kanka? Valla dinliyorum seni, anlat anlat!",
            "Haklısın valla kanka. Başka ne var ne yok?"
        ])

# --- ANA MOTOR ---
def kailer_nihai_motor(ham_sorgu):
    s = metni_kucult(ham_sorgu)

    # -------------------------------------------------------------
    # 0. KÜFÜR FİLTRESİ
    # -------------------------------------------------------------
    kufur = r'\b(aq|amk|a\.m\.k|ananı|ananın|sik|sikerim|sikim|amcık|orospu|piç)\b'
    if re.search(kufur, s):
        return "Kanka sakin ol ya! Küfüre hiç gerek yok, kafa kafaya verip hallederiz :D"

    # -------------------------------------------------------------
    # 1. MOD DEĞİŞTİRME KOMUTLARI (e!sOhbet, E!SOHBET vb.)
    # -------------------------------------------------------------
    if s.startswith("e!"):
        komut = s[2:].strip()

        if komut in ["sohbet", "chat"]:
            st.session_state["mode"] = "sohbet"
            return "💬 **SOHBET MODU AKTİF!**\n\nArtık soru-cevap veya Vikipedi araması yok kanka! Sadece sen ve ben muhabbet ediyoruz. Anlat bakalım, ne var ne yok?\n\n*(Arama moduna dönmek için `e!soru` yazabilirsin)*"
        
        elif komut in ["soru", "bilgi", "arama"]:
            st.session_state["mode"] = "soru"
            return "🔍 **SORU & BİLGİ MODU AKTİF!**\n\nSohbetten çıktık kanka. Artık ne aratırsan anında canlı veritabanından çekip sana sunacağım!"

        elif komut in ["oyun", "game"]:
            st.session_state["mode"] = "oyun"
            st.session_state["game_state"] = "secim"
            return (
                "🎮 **KAİLER OYUN MERKEZİ**\n\n"
                "Hangi oyunu oynamak istersin kanka? (Aşağıdaki numarayı veya ismi yaz):\n\n"
                "1. **Adam Asmaca** (Gizli kelimeyi harf harf bul!)\n"
                "2. **Akinator / Akıl Okuma** (Sen bir şey tut ben bileyim ya da ben tutayım sen bil!)\n\n"
                "*(Oyundan çıkmak için `e!soru` veya `e!sohbet` yazabilirsin)*"
            )

        elif komut in ["meme", "miim", "mim"]:
            return rastgele_meme_cek()

        else:
            return f"Kanka `e!{komut}` komutunu bulamadım. `e!sohbet`, `e!oyun`, `e!soru` veya `e!meme` deneyebilirsin!"

    # -------------------------------------------------------------
    # 2. OYUN MODU MANTIĞI
    # -------------------------------------------------------------
    if st.session_state["mode"] == "oyun":
        if st.session_state["game_state"] == "secim":
            if s in ["1", "adam asmaca"]:
                st.session_state["game_state"] = "adam_asmaca"
                st.session_state["secret_word"] = random.choice(["fenerbahce", "bilgisayar", "yazilim", "streamlit"]).lower()
                st.session_state["guesses"] = []
                st.session_state["lives"] = 6
                display = "".join([c if c in st.session_state["guesses"] else " _ " for c in st.session_state["secret_word"]])
                return f"🎮 **Adam Asmaca Başladı!**\n\nKelime: `{display}`\nKalan Hak: **{st.session_state['lives']}**\n\nHarf yaz kanka!"
            
            elif s in ["2", "akinator", "akil okuma"]:
                st.session_state["game_state"] = "akinator_secim"
                return "🧙‍♂️ **Akinator Modu!**\n\n1. **Aklımda Ben Tutayım:** Ben tutayım sen bil!\n2. **Aklında Sen Tut:** Sen tut, ben tahmin edeyim!\n\n(1 veya 2 yaz kanka)"

        elif st.session_state["game_state"] == "adam_asmaca":
            if len(s) == 1 and s.isalpha():
                if s in st.session_state["guesses"]:
                    return "Kanka bu harfi zaten söyledin!"
                st.session_state["guesses"].append(s)
                if s not in st.session_state["secret_word"]:
                    st.session_state["lives"] -= 1
                display = "".join([c if c in st.session_state["guesses"] else " _ " for c in st.session_state["secret_word"]])
                if "_" not in display:
                    st.session_state["mode"] = "soru"
                    return f"🎉 **TEBRİKLER KAZANDIN!** Kelime: **{st.session_state['secret_word'].upper()}**"
                if st.session_state["lives"] <= 0:
                    st.session_state["mode"] = "soru"
                    return f"💀 **KAYBETTİN!** Doğru kelime: **{st.session_state['secret_word'].upper()}**"
                return f"Kelime: `{display}` | Kalan Hak: **{st.session_state['lives']}**"

        elif st.session_state["game_state"] == "akinator_secim":
            if s == "1":
                st.session_state["game_state"] = "bot_tuttu"
                st.session_state["bot_target"] = random.choice(["araba", "telefon", "fenerbahçe", "kedi"])
                return "Aklımda bir nesne tuttum kanka! Sorularla tahmin etmeye çalış!"
            elif s == "2":
                st.session_state["game_state"] = "user_tuttu"
                return "Aklında bir şey tut kanka! Hazırsan 'Hazırım' yaz!"

    # -------------------------------------------------------------
    # 3. SOHBET MODU (Sadece e!soru ile çıkılır)
    # -------------------------------------------------------------
    if st.session_state["mode"] == "sohbet":
        return sohbet_modu_yanitla(ham_sorgu)

    # -------------------------------------------------------------
    # 4. SORU & BİLGİ MODU (Varsayılan)
    # -------------------------------------------------------------
    selamlar = ["sa", "slm", "selam", "selamun aleykum", "merhaba", "hey"]
    if s in selamlar:
        return "Aleykümselam kanka! Arama modundayız. Sohbet etmek istersen `e!sohbet` yazabilirsin!"

    # Vikipedi Arama
    web_result = wikipedia_canli_arama(ham_sorgu)
    if web_result:
        baslik, ozet = web_result
        return f"**{baslik} Hakkında Bilgi:**\n\n{ozet}"

    return f"Kanka **'{ham_sorgu}'** hakkında bilgi bulamadım. Muhabbet etmek istersen `e!sohbet` yazabilirsin!"

# --- İNPUT ALMA VE EKRANA BASMA ---
if prompt := st.chat_input("e!sOhbet, E!OYUN, e!soru, e!meme veya aratmak istediğini yaz..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Kailer AI işliyor..."):
            reply = kailer_nihai_motor(prompt)

        st.write(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})
