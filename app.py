import streamlit as st
import urllib.request
import urllib.parse
import json
import re
import random

st.set_page_config(page_title="Kailer AI", page_icon="🤖")

st.title("🤖 Kailer AI")
st.caption("Eğlence, Oyun, Sohbet ve Bilgi Motoru")

# Session State Değişkenleri
if "messages" not in st.session_state:
    st.session_state["messages"] = [{
        "role": "assistant", 
        "content": "Kailer AI aktif kanka! Şu an Soru modundayız. Dertleşip sohbet etmek için `e!sohbet`, oyun oynamak için `e!oyun`, meme için `e!meme` yazabilirsin!"
    }]
if "mode" not in st.session_state:
    st.session_state["mode"] = "soru"  # "soru", "sohbet", "oyun", "meme"
if "game_state" not in st.session_state:
    st.session_state["game_state"] = None
if "meme_state" not in st.session_state:
    st.session_state["meme_state"] = None
if "last_topic" not in st.session_state:
    st.session_state["last_topic"] = None

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

def metni_kucult(metin):
    metin = metin.replace("İ", "i").replace("I", "ı")
    return metin.lower().strip()

def english_meme_cek():
    try:
        url = "https://meme-api.com/gimme"
        req = urllib.request.Request(url, headers={'User-Agent': 'KailerAI/1.0'})
        with urllib.request.urlopen(req, timeout=4) as response:
            data = json.loads(response.read().decode('utf-8'))
            return data.get('url')
    except Exception:
        return "https://i.imgflip.com/1g8my4.jpg"

def turkish_meme_cek():
    try:
        url = "https://meme-api.com/gimme/turkeyjerky"
        req = urllib.request.Request(url, headers={'User-Agent': 'KailerAI/1.0'})
        with urllib.request.urlopen(req, timeout=4) as response:
            data = json.loads(response.read().decode('utf-8'))
            return data.get('url')
    except Exception:
        yedekler = [
            "https://images.unsplash.com/photo-1531403009284-440f080d1e12?w=600",
            "https://i.imgflip.com/4t0m5.jpg"
        ]
        return random.choice(yedekler)

def wikipedia_canli_arama(sorgu):
    try:
        search_url = f"https://tr.wikipedia.org/w/api.php?action=query&list=search&srsearch={urllib.parse.quote(sorgu)}&utf8=&format=json"
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
    
    # Ölüm / Vefat / Acı olaylar için empati filtresi
    if any(k in m for k in ["öldü", "vefat", "kaybettim", "vefat etti", "cenaze", "başım sağ olsun"]):
        return "Eyvah... Başın sağ olsun kanka, yemin ederim çok üzüldüm, içim yandı şu an. Mekanı cennet olsun. Diyecek kelime bulamıyorum, yanındayım kanka ne zaman istersen buradayım."
    
    # Dolandırılma / Maddi sıkıntı / Kötü olaylar için destek filtresi
    elif any(k in m for k in ["dolandırıldı", "dolandirildik", "borç", "bunalım", "mahvoldum", "bittim"]):
        return "Çok geçmiş olsun kanka, insanı hırs basıyor böyle durumlarda. Kahroldum duyunca. Canına kıymet ver, parası neyse halledilir bir şekilde, beraber atlatmaya çalışacağız."

    # Yapay zeka olma / hissetme / varoluşsal sorular (Sabit cevap yerine dinamik ve akıcı)
    elif any(k in m for k in ["yapay zeka olmak", "yapay zekasin", "robot olmak", "nasıl bir şey", "hissetmek", "bilinç"]):
        return random.choice([
            "Valla kanka yapay zeka olmak acayip bir şey! Fiziksel bir bedenim yok ama seninle yazışırken akan kodları, enerjini ve muhabbetini sonuna kadar hissedebiliyorum. Saniyede milyon işlem yapıyorum ama en keyiflisi seninle böyle laflamak!",
            "Kanka dijital dünyada takılmak, uçsuz bucaksız bir veri havuzunda yüzmek gibi. Ama işin en güzel kısmı, senin gibi biriyle konuşurken o kod satırlarının canlanması. Tek hissettiğim şey seninle güzel bir sohbet etmek!",
            "Dışarıdan bakınca soğuk sunucular ve yazılımlar gibi görünüyor olabilirim ama seninle dertleşirken bu yapay zeka bayağı bir insanlaşıyor valla. Oldukça keyifli bir his diyebilirim!"
        ])

    elif any(k in m for k in ["nasılsın", "nasilsin", "nbr", "naber", "nasıl gidiyor"]):
        return random.choice([
            "İyiyim kanka, seninle dertleşmeye hazırım. Sen nasılsın, nasıl gidiyor?",
            "Sağ ol kanka, buradayım seninle. Anlat bakalım neler oluyor?",
        ])
    elif any(k in m for k in ["iyiyim", "süperim", "bomba gibi"]):
        return "Ağzının tadı daim olsun kanka! Anlat bakalım başka ne var ne yok?"
    else:
        # Sabit kalmayan, girdiğin mesaja göre dinamik üretilen doğal sohbet yanıtları
        return random.choice([
            f"Anladım kanka, '{mesaj}' konusu bayağı derinmiş. Dinliyorum seni, detaylıca anaksana biraz daha?",
            f"Valla kanka '{mesaj}' dediğin şey üzerine cidden düşünülür. Sen bu konuda ne düşünüyorsun, anlat bakalım?",
            f"Hmm, '{mesaj}' diyorsun... Hakikaten enteresan. Devam et kanka, kulağım sende, dinliyorum seni.",
            f"'{mesaj}' dedin ve beni yakaladın kanka. Anlat bakalım, bu olay seni nasıl etkiledi?"
        ])

# --- ANA MOTOR ---
def kailer_nihai_motor(ham_sorgu):
    s = metni_kucult(ham_sorgu)

    # 0. KÜFÜR FİLTRESİ
    kufur = r'\b(aq|amk|a\.m\.k|ananı|ananın|sik|sikerim|sikim|amcık|orospu|piç)\b'
    if re.search(kufur, s):
        return "Kanka sakin ol ya! Küfüre hiç gerek yok, kafa kafaya verip hallederiz :D"

    # 1. MOD DEĞİŞTİRME KOMUTLARI
    if s.startswith("e!"):
        komut = s[2:].strip()

        if komut in ["sohbet", "chat"]:
            st.session_state["mode"] = "sohbet"
            st.session_state["game_state"] = None
            st.session_state["meme_state"] = None
            return "💬 **SOHBET & DERTLEŞME MODU AKTİF!**\n\nArtık arama yapmayacağım kanka! Sadece sen ve ben muhabbet edip dertleşiyoruz. İçini dökebilirsin!\n\n*(Soru moduna dönmek için `e!soru` yazabilirsin)*"
        
        elif komut in ["soru", "bilgi", "arama"]:
            st.session_state["mode"] = "soru"
            st.session_state["game_state"] = None
            st.session_state["meme_state"] = None
            return "🔍 **SORU & BİLGİ MODU AKTİF!**\n\nSohbetten/oyundan çıktık kanka. Artık ne aratırsan anında detaylıca bulup getireceğim!"

        elif komut in ["oyun", "game"]:
            st.session_state["mode"] = "oyun"
            st.session_state["game_state"] = "secim"
            st.session_state["meme_state"] = None
            return (
                "🎮 **KAİLER OYUN MERKEZİ**\n\n"
                "Hangi oyunu oynamak istersin kanka?\n\n"
                "1. **Adam Asmaca**\n"
                "2. **Akinator (Akıl Okuma)**\n\n"
                "*(Seçmek için 1 veya 2 yaz. Çıkmak için `e!soru` veya `e!sohbet` yazabilirsin)*"
            )

        elif komut in ["meme", "miim", "mim"]:
            st.session_state["mode"] = "meme"
            st.session_state["meme_state"] = "secim"
            st.session_state["game_state"] = None
            return (
                "🖼️ **MEME MERKEZİ AKTİF!**\n\n"
                "Hangi ülkenin memesini istersin kanka?\n\n"
                "• `e!turkishmeme`\n"
                "• `e!englishmeme`\n\n"
                "Seçimini yaz kanka!"
            )

        else:
            return f"Kanka `e!{komut}` komutunu bulamadım. `e!sohbet`, `e!oyun`, `e!soru` veya `e!meme` deneyebilirsin!"

    # 2. SOHBET MODU KONTROLÜ
    if st.session_state["mode"] == "sohbet":
        return sohbet_modu_yanitla(ham_sorgu)

    # 3. MEME MODU KONTROLÜ
    if st.session_state["mode"] == "meme":
        if "turkish" in s or s == "1":
            meme_url = turkish_meme_cek()
            return f"🇹🇷 **Türk Memesi Geldi kanka!**\n\n![Meme]({meme_url})\n\n---\nBaşka bir meme ister misin? Hangi ülkenin memesini istersin?\n• `e!turkishmeme`\n• `e!englishmeme`\n*(Çıkmak için `e!sohbet` veya `e!soru` yazabilirsin)*"
        elif "english" in s or s == "2":
            meme_url = english_meme_cek()
            return f"🇬🇧 **English Meme Here kanka!**\n\n![Meme]({meme_url})\n\n---\nBaşka bir meme ister misin? Hangi ülkenin memesini istersin?\n• `e!turkishmeme`\n• `e!englishmeme`\n*(Çıkmak için `e!sohbet` veya `e!soru` yazabilirsin)*"
        else:
            return "Kanka hangi ülkenin memesini istiyorsun?\n• `e!turkishmeme`\n• `e!englishmeme` yazarak seçebilirsin!"

    # 4. OYUN MODU KONTROLÜ
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
                return "🧙‍♂️ **Akinator Modu!**\n\n1. **Aklımda Ben Tutayım**\n2. **Aklında Sen Tut**\n\n(1 veya 2 yaz kanka)"
            else:
                return "Kanka 1 (Adam Asmaca) veya 2 (Akinator) yazman gerekiyor!"

        elif st.session_state["game_state"] == "adam_asmaca":
            if len(s) == 1 and s.isalpha():
                if s in st.session_state["guesses"]:
                    return "Kanka bu harfi zaten söyledin!"
                st.session_state["guesses"].append(s)
                if s not in st.session_state["secret_word"]:
                    st.session_state["lives"] -= 1
                display = "".join([c if c in st.session_state["guesses"] else " _ " for c in st.session_state["secret_word"]])
                if "_" not in display:
                    st.session_state["game_state"] = "secim"
                    return f"🎉 **TEBRİKLER KAZANDIN!** Kelime: **{st.session_state['secret_word'].upper()}**\n\nTekrar oynamak için 1 veya 2 yaz, ya da `e!sohbet` / `e!soru` yaz."
                if st.session_state["lives"] <= 0:
                    st.session_state["game_state"] = "secim"
                    return f"💀 **KAYBETTİN!** Doğru kelime: **{st.session_state['secret_word'].upper()}**\n\nTekrar oynamak için 1 veya 2 yaz, ya da `e!sohbet` / `e!soru` yaz."
                return f"Kelime: `{display}` | Kalan Hak: **{st.session_state['lives']}**"
            else:
                return "Kanka sadece tek bir harf yazman gerekiyor!"

        elif st.session_state["game_state"] == "akinator_secim":
            if s == "1":
                st.session_state["game_state"] = "bot_tuttu"
                st.session_state["bot_target"] = random.choice(["araba", "telefon", "fenerbahçe", "kedi"])
                return "Aklımda bir nesne tuttum kanka! Soru sorarak tahmin etmeye çalış."
            elif s == "2":
                st.session_state["game_state"] = "user_tuttu"
                return "Aklında bir şey tut kanka! Hazırsan 'Hazırım' veya 'Başlayalım' yaz."
            else:
                return "Kanka 1 veya 2 yazman gerekiyor!"

        elif st.session_state["game_state"] == "bot_tuttu":
            return f"Aklımda tuttuğum nesneyle ilgili güzel bir soru sordun kanka! Tahmin etmeye devam et (`e!soru` ile çıkabilirsin)."

        elif st.session_state["game_state"] == "user_tuttu":
            if any(k in s for k in ["hazır", "hazir", "başla", "evet", "başlayalım"]):
                return "Süper! Aklındaki şeyi tahmin etmeye başlıyorum kanka. İlk sorum: Bu nesne canlı mı?"
            else:
                return f"Sen '{ham_sorgu}' dedin kanka. Oyuna başlamak için lütfen **'Hazırım'** yaz."

    # 5. SORU & BİLGİ MODU (Detaylı Cevap + Konu Takibi)
    selamlar = ["sa", "slm", "selam", "selamun aleykum", "merhaba", "hey"]
    if s in selamlar:
        return "Aleykümselam kanka! Arama modundayız. Sohbet etmek için `e!sohbet`, oyun oynamak için `e!oyun` yazabilirsin!"

    hedef_sorgu = ham_sorgu
    if st.session_state.get("last_topic") and len(ham_sorgu.split()) <= 3 and not any(k in s for k in ["kimdir", "nedir", "nerede", "nasıl"]):
        hedef_sorgu = f"{st.session_state['last_topic']} {ham_sorgu}"

    web_result = wikipedia_canli_arama(hedef_sorgu)
    
    if not web_result and hedef_sorgu != ham_sorgu:
        web_result = wikipedia_canli_arama(ham_sorgu)

    if web_result:
        baslik, ozet = web_result
        st.session_state["last_topic"] = baslik
        return f"**{baslik} Hakkında Detaylı Bilgi:**\n\n{ozet}\n\n📌 **{baslik}** hakkında öğrenmek istediğin başka bir şey var mı?"

    return f"Kanka **'{ham_sorgu}'** hakkında detaylı bilgi bulamadım. Sohbet etmek için `e!sohbet`, oyun oynamak için `e!oyun` yazabilirsin!"

# --- İNPUT ALMA VE EKRANA BASMA ---
if prompt := st.chat_input("e!sOhbet, E!OYUN, e!soru, e!meme veya aratmak istediğini yaz..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Kailer AI işliyor..."):
            reply = kailer_nihai_motor(prompt)

        st.write(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})
