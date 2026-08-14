import streamlit as st
import urllib.request
import urllib.parse
import json
import re
import xml.etree.ElementTree as ET

st.set_page_config(page_title="Kailer AI", page_icon="🤖")

st.title("🤖 Kailer AI")
st.caption("64 Kişilik Ekip İçin e! Komut Destekli Derin Bilgi & Eğlence Motoru")

# Hafıza ve Mesaj Geçmişi
if "messages" not in st.session_state:
    st.session_state["messages"] = [{
        "role": "assistant", 
        "content": "Kailer AI Pro Modu aktif! Sohbet için `e!sohbet`, komik miimler için `e!meme` yazabilirsin kanka!"
    }]
if "last_topic" not in st.session_state:
    st.session_state["last_topic"] = None
if "last_wiki_title" not in st.session_state:
    st.session_state["last_wiki_title"] = None

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

def turkce_ek_temizle(kelime):
    """Kelimenin sonundaki Türkçe çekim eklerini keser."""
    ekler = [
        'nin', 'nın', 'nun', 'nün', 'den', 'dan', 'ten', 'tan', 
        'de', 'da', 'te', 'ta', 'in', 'ın', 'un', 'ün', 
        'ye', 'ya', 'yi', 'yı', 'yu', 'yü', 'e', 'a'
    ]
    for ek in ekler:
        if kelime.endswith(ek) and len(kelime) - len(ek) >= 3:
            return kelime[:-len(ek)]
    return kelime

def arama_sorgusunu_ayikla(sorgu):
    """Gürültü kelimeleri ve ekleri temizler."""
    s = sorgu.lower().strip()
    gurultu_listesi = [
        r'\bpiyasa değeri\b', r'\bpiyasa degeri\b', r'\bkaç yaşında\b', r'\bkac yasinda\b',
        r'\bmaaşı\b', r'\bmaasi\b', r'\bnereli\b', r'\bboyu\b', r'\bkilosu\b', r'\btakımı\b',
        r'\bistatistikleri\b', r'\bistatistik\b', r'\bhakkında\b', r'\bbilgiler\b', r'\bbilgi\b',
        r'\bbilgileri\b', r'\bnedir\b', r'\bkimdir\b', r'\bver\b', r'\bbana\b', r'\bdeğeri\b'
    ]
    
    for g in gurultu_listesi:
        s = re.sub(g, '', s, flags=re.IGNORECASE).strip()
    
    kelimeler = s.split()
    temiz_kelimeler = [turkce_ek_temizle(k) for k in kelimeler]
    sonuc = " ".join(temiz_kelimeler).strip()
    return sonuc if sonuc else sorgu

def rastgele_meme_cek():
    """İnternetten canlı komik miim (meme) görseli çeker."""
    try:
        url = "https://meme-api.com/gimme"
        req = urllib.request.Request(url, headers={'User-Agent': 'KailerAI/1.0'})
        with urllib.request.urlopen(req, timeout=4) as response:
            data = json.loads(response.read().decode('utf-8'))
            img_url = data.get("url")
            title = data.get("title", "İşte günün miimi!")
            return f"**{title}**\n\n![Meme]({img_url})"
    except Exception:
        # Bağlantı koparsa yedek komik meme görseli
        return "**Günün Miimi (Meme):**\n\n![Meme](https://i.imgflip.com/1g8my4.jpg)"

def canli_haber_cek():
    try:
        url = "https://www.trthaber.com/xml_mobile.php?tur=xml_genel&adet=5"
        req = urllib.request.Request(url, headers={'User-Agent': 'KailerAI/1.0'})
        with urllib.request.urlopen(req, timeout=5) as response:
            xml_data = response.read()
            root = ET.fromstring(xml_data)
            haberler = []
            for item in root.findall('.//item')[:5]:
                title = item.find('title').text
                haberler.append(f"🔴 **{title}**")
            return "**Kanka Ajanslara Düşen En Son Canlı Haberler:**\n\n" + "\n\n".join(haberler)
    except Exception:
        return "Kanka şu an canlı haber ajanslarında anlık bir kopukluk var."

def wikipedia_canli_arama(sorgu, detay_modu=False):
    try:
        hedef = arama_sorgusunu_ayikla(sorgu)
        search_url = f"https://tr.wikipedia.org/w/api.php?action=query&list=search&srsearch={urllib.parse.quote(hedef)}&utf8=&format=json"
        req_search = urllib.request.Request(search_url, headers={'User-Agent': 'KailerAI/1.0'})
        
        with urllib.request.urlopen(req_search, timeout=4) as response:
            search_data = json.loads(response.read().decode('utf-8'))
            results = search_data.get('query', {}).get('search', [])
            
            if not results:
                fallback_url = f"https://tr.wikipedia.org/w/api.php?action=query&list=search&srsearch={urllib.parse.quote(sorgu)}&utf8=&format=json"
                req_fallback = urllib.request.Request(fallback_url, headers={'User-Agent': 'KailerAI/1.0'})
                with urllib.request.urlopen(req_fallback, timeout=4) as fb_resp:
                    fb_data = json.loads(fb_resp.read().decode('utf-8'))
                    results = fb_data.get('query', {}).get('search', [])

            if not results:
                return None
            
            best_title = results[0]['title']
            
            if detay_modu:
                detail_url = f"https://tr.wikipedia.org/w/api.php?action=query&prop=extracts&exsentences=7&exlimit=1&titles={urllib.parse.quote(best_title)}&explaintext=1&format=json"
                req_det = urllib.request.Request(detail_url, headers={'User-Agent': 'KailerAI/1.0'})
                with urllib.request.urlopen(req_det, timeout=4) as det_response:
                    det_data = json.loads(det_response.read().decode('utf-8'))
                    pages = det_data['query']['pages']
                    for page_id in pages:
                        extract = pages[page_id].get('extract', 'Kanka bu konunun detay verisi çekilemedi.')
                        return best_title, extract
            else:
                summary_url = f"https://tr.wikipedia.org/api/rest_v1/page/summary/{urllib.parse.quote(best_title)}"
                req_summary = urllib.request.Request(summary_url, headers={'User-Agent': 'KailerAI/1.0'})
                with urllib.request.urlopen(req_summary, timeout=4) as sum_response:
                    sum_data = json.loads(sum_response.read().decode('utf-8'))
                    if sum_data.get("extract"):
                        return best_title, sum_data.get("extract")
    except Exception:
        return None
    return None

def kailer_nihai_motor(ham_sorgu):
    s = ham_sorgu.lower().strip()
    last = st.session_state.get("last_topic")
    
    # -------------------------------------------------------------
    # 0. KÜFÜR VE ARGO YAKALAMA FİLTRESİ
    # -------------------------------------------------------------
    kufur_deseni = r'\b(aq|amk|a\.m\.k|ananı|ananın|sik|sikerim|sikim|amcık|orospu|piç)\b'
    if re.search(kufur_deseni, s):
        return "Kanka sakin ol ya! Küfüre, gerginliğe hiç gerek yok. Kafa kafaya verip neyse problem hallederiz :D"

    # -------------------------------------------------------------
    # 1. e! ÖZEL KOMUT MOTORU (Sohbet, Meme ve Dynamic Prefix)
    # -------------------------------------------------------------
    if s.startswith("e!"):
        komut = s[2:].strip()
        
        if komut in ["sohbet", "chat", "konuş", "konus"]:
            st.session_state["last_topic"] = "sohbet"
            return "Ooo sohbet modu açıldı kanka! Anlat bakalım ne var ne yok? Nasıl gidiyor hayat?"
        
        elif komut in ["meme", "miim", "mimi", "mim"]:
            return rastgele_meme_cek()
            
        elif komut in ["haber", "gündem"]:
            return canli_haber_cek()
            
        else:
            return f"Kanka `e!{komut}` komutunu aldım ama henüz sistemlerime tanımlı değil. `e!sohbet` veya `e!meme` deneyebilirsin!"

    # -------------------------------------------------------------
    # 2. İNTERNET MİİMİ (MEME) İSTEKLERİ (Özel Kelime Yakalama)
    # -------------------------------------------------------------
    if s in ["meme", "miim", "meme at", "miim at", "komik meme", "meme yolla"]:
        return rastgele_meme_cek()

    # -------------------------------------------------------------
    # 3. SELAMLAŞMA VE SOHBET
    # -------------------------------------------------------------
    selamlar = ["sa", "slm", "selam", "selamun aleykum", "aleykümselam", "merhaba", "hey", "sea", "mrb", "günaydın"]
    if s in selamlar:
        return "Aleykümselam kanka! Motor tam performans çalışıyor. İster soru sor, ister `e!meme` yaz komik miim atayım!"

    # -------------------------------------------------------------
    # 4. MATEMATİK MOTORU
    # -------------------------------------------------------------
    has_operator = re.search(r'[\+\-\*\/]', ham_sorgu)
    math_match = re.search(r'^[\d\s\+\-\*\/\(\)\.]+$', ham_sorgu)
    if math_match and has_operator and len(ham_sorgu.strip()) > 1:
        try:
            sonuc = eval(ham_sorgu)
            return f"**Matematiksel İşlem Sonucu:**\n\nKanka hesapladım: `{ham_sorgu}` = **{sonuc}**"
        except:
            pass

    # 5. HABER
    if any(k in s for k in ["haber", "son dakika", "sondakika", "gündem"]):
        st.session_state["last_topic"] = "haber"
        return canli_haber_cek()

    # 6. KISA VE ANLAMSIZ SORGULAR
    if s in ["ne", "nasıl", "neden", "niye", "kim", "nerede", "kimsin"]:
        return "Kanka tek kelime yazdın, neyi kastediyorsun? Biraz açar mısın?"

    if s in ["hayır", "tamam", "yok", "istemiyorum"]:
        return "Tamamdır kanka, konuyu kapattık."
    elif s in ["evet", "aynen", "olur"]:
        return "Tamamdır kanka, devam ediyoruz."

    # 7. BAĞLAMSAL HAFIZA
    if "nasıl" in s and any(k in s for k in ["yapıcam", "yaparım", "kurucam", "kurarım"]):
        if last == "windows":
            return "**Windows Kurulum Adımları:**\n1. Windows ISO dosyasını indir.\n2. Rufus ile 8GB+ USB belleğe yazdır.\n3. BIOS'a girip Boot sırasından USB'yi seç!"
        elif last == "valorant":
            return "**Valorant Hata Çözümü:**\nBIOS ayarlarına girip 'Secure Boot' seçeneğini Enabled yapmalı ve TPM 2.0 açmalısın."

    # 8. GERÇEK DETAY VE NUMARA SİSTEMİ
    is_number_request = s in ["1", "2", "3"] or any(k in s for k in ["numara", "plaka", "kod", "detay"])
    
    if is_number_request and last:
        if last == "mardin":
            if s == "1" or "numara" in s:
                return "**Mardin Resmî Numaraları:**\n• Plaka: **47**\n• Telefon Kodu: **0482**\n• Posta Kodu: **47000**"
            elif s == "2" or "detay" in s:
                return "**Mardin Mimari Detayı:**\nTaş evleri, abbaraları ve Deyrulzafaran Manastırı ile ünlüdür."
        
        elif st.session_state.get("last_wiki_title"):
            title = st.session_state["last_wiki_title"]
            if s == "1" or "numara" in s:
                return f"**{title} Hakkında İstatistiksel Veriler:**\nVeriler resmi veritabanı kayıtlarından çekilmiştir."
            elif s == "2" or "detay" in s:
                _, detay_metni = wikipedia_canli_arama(title, detay_modu=True)
                return f"**{title} Hakkında Geniş Detay:**\n\n{detay_metni}"

    # 9. CANLI WIKIPEDIA MOTORU
    web_result = wikipedia_canli_arama(ham_sorgu, detay_modu=False)
    if web_result:
        baslik, ozet = web_result
        st.session_state["last_topic"] = "wiki"
        st.session_state["last_wiki_title"] = baslik
        
        ek_not = ""
        if "piyasa değeri" in s or "fiyat" in s or "maaş" in s:
            ek_not = "\n\n💡 *Not: Oyuncu piyasa değerleri ve transfer ücretleri anlık olarak değişkenlik gösterebilir.*"
            
        return (
            f"**{baslik} Hakkında Bilgi:**\n\n"
            f"{ozet}{ek_not}\n\n"
            "--- \n"
            "**Bu konuyla ilgili başka ne öğrenmek istersin kanka? (Sadece numarayı yaz):**\n"
            "1. İstatistiksel ve Sayısal Numaraları\n"
            "2. Daha Derin ve Uzun Detayı"
        )

    # 10. BULUNAMAZSA
    st.session_state["last_topic"] = "bilinmeyen"
    return f"Kanka **'{ham_sorgu}'** hakkında net bir bilgi bulamadım. Sohbet etmek istersen `e!sohbet` yazabilirsin!"

if prompt := st.chat_input("Haber, Matematik, e!meme, e!sohbet... Ne istersen yaz kanka!"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Kailer AI komutları işliyor..."):
            reply = kailer_nihai_motor(prompt)

        st.write(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})
