import streamlit as st
import urllib.request
import urllib.parse
import json
import re
import xml.etree.ElementTree as ET

st.set_page_config(page_title="Kailer AI", page_icon="🤖")

st.title("🤖 Kailer AI")
st.caption("64 Kişilik Ekip İçin Canlı Haber ve Evrensel Bilgi Motoru")

# Hafıza ve Mesaj Geçmişi
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Kailer AI tam kapasite aktif! Canlı haber, matematik, bilim, tarih... Neyi arıyoruz kanka?"}]
if "last_topic" not in st.session_state:
    st.session_state["last_topic"] = None
if "last_wiki_title" not in st.session_state:
    st.session_state["last_wiki_title"] = None

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

def metni_temizle_ve_anla(metin):
    """Klavye kaymalarını, kısaltmaları ve hızlı yazım hatalarını anında çözer."""
    m = metin.lower().strip()
    hizli_yazim_sozlugu = {
        r'\bhqyır\b': 'hayır', r'\bhsyır\b': 'hayır',
        r'\bevt\b': 'evet', r'\bevtt\b': 'evet',
        r'\btm\b': 'tamam', r'\btmm\b': 'tamam', r'\bok\b': 'tamam',
        r'\bnbr\b': 'naber', r'\bslm\b': 'selam', r'\bsa\b': 'selam',
        r'\bmrdin\b': 'mardin', r'\bmardn\b': 'mardin',
        r'\bvlorant\b': 'valorant', r'\bvalrant\b': 'valorant',
        r'\bwndows\b': 'windows', r'\bwindos\b': 'windows',
        r'\bucgen\b': 'üçgen', r'\butgen\b': 'üçgen'
    }
    for hata, dogru in hizli_yazim_sozlugu.items():
        m = re.sub(hata, dogru, m)
    return m

def canli_haber_cek():
    """Ajanslardan anlık (1 saniye önceki) son dakika haberlerini canlı çeker."""
    try:
        # TRT Haber canlı RSS akışı
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
        return "Kanka şu an canlı haber ajanslarında anlık bir kopukluk var, 1-2 dakika sonra tekrar yaz."

def wikipedia_canli_arama(sorgu):
    """Dünyadan güneşe, en alakasız bilimsel veya tarihi konuyu anında bulur."""
    try:
        search_url = f"https://tr.wikipedia.org/w/api.php?action=query&list=search&srsearch={urllib.parse.quote(sorgu)}&utf8=&format=json"
        req_search = urllib.request.Request(search_url, headers={'User-Agent': 'KailerAI/1.0'})
        with urllib.request.urlopen(req_search, timeout=4) as response:
            search_data = json.loads(response.read().decode('utf-8'))
            
            if not search_data['query']['search']:
                return None
            
            best_title = search_data['query']['search'][0]['title']
            
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
    s = metni_temizle_ve_anla(ham_sorgu)
    last = st.session_state.get("last_topic")
    
    # 1. MATEMATİK VE HESAPLAMA MOTORU (Saniyesinde çözer)
    math_match = re.search(r'^[\d\s\+\-\*\/\(\)\.]+$', ham_sorgu)
    if math_match and len(ham_sorgu.strip()) > 1:
        try:
            sonuc = eval(ham_sorgu)
            return f"**Matematiksel İşlem Sonucu:**\n\nKanka uğraşmana gerek yok, `{ham_sorgu}` işleminin net sonucu: **{sonuc}**"
        except:
            pass

    # 2. CANLI HABER MOTORU (1 Saniye Öncesi)
    if "haber" in s or "son dakika" in s or "sondakika" in s or "gündem" in s:
        st.session_state["last_topic"] = "haber"
        return canli_haber_cek()

    # 3. SOHBETLER VE KISA CEVAPLAR
    if s in ["selam", "selamun aleykum", "merhaba", "hey"]:
        return "Aleykümselam kanka! Sistemler online. Dünya'dan Güneş'e neyi araştıralım?"
    elif s in ["nasılsın", "naber", "ne var ne yok", "iyi misin"]:
        return "Harikayım kanka, fişek gibiyim! Sen nasılsın?"
    elif s in ["hayır", "tamam", "yok", "istemiyorum"]:
        return "Anlaşıldı kanka, konuyu kapattık. Başka ne arıyoruz?"
    elif s in ["evet", "aynen", "olur"]:
        return "Tamamdır kanka, nasıl istersen. Yeni sorunu bekliyorum."

    # 4. HAFIZA SİSTEMİ (Numara İstendiğinde)
    is_number_request = s in ["1", "2", "3"] or "numara" in s or "plaka" in s or "kod" in s or "detay" in s
    
    if is_number_request and last:
        if last == "mardin":
            if s == "1" or "numara" in s or "plaka" in s:
                return "**Mardin Resmî Numaraları:**\n• Plaka: **47**\n• Telefon: **0482**\n• Posta Kodu: **47000**"
            elif s == "2" or "detay" in s:
                return "**Mardin Mimari Detayı:**\nTaş evleri, abbaraları ve Deyrulzafaran Manastırı ile ünlüdür."
        
        elif st.session_state.get("last_wiki_title"):
            title = st.session_state["last_wiki_title"]
            if s == "1" or "numara" in s:
                return f"**{title} Hakkında Teknik/Sayısal Detaylar:**\n\nBu konuyla ilgili istatistiksel ve sayısal veriler, küresel ölçekteki kurumların anlık veritabanlarında kayıtlıdır."
            elif s == "2" or "detay" in s:
                return f"**{title} Hakkında Ekstra Detay:**\n\nKanka, {title} konusu genel hatlarıyla tarihsel arka planı, teknik yapısı ve evrensel kuralları çerçevesinde çok katmanlı bir şekilde değerlendirilir."

    # 5. KESİN VE ÖZEL EŞLEŞMELER
    if "mardin" in s:
        st.session_state["last_topic"] = "mardin"
        return (
            "**Mardin Hakkında Açık ve Detaylı Bilgiler:**\n\n"
            "• **Coğrafya:** Güneydoğu Anadolu'da, taş mimarisiyle bilinen tarihi şehirdir.\n"
            "• **Kültür:** Süryani, Kürt, Arap ve Türklerin bir arada yaşadığı hoşgörü merkezidir.\n\n"
            "--- \n"
            "**Detayına inelim mi kanka? (Numarasını yazman yeterli):**\n"
            "1. Plaka ve Telefon Numaraları\n"
            "2. Gezilecek Yerleri ve Mimarisi"
        )

    if re.search(r'\b(din|inanç|islam)\b', s):
        st.session_state["last_topic"] = "din"
        return (
            "**Din ve İnanç Sistemleri:**\n\n"
            "• **Tanım:** Din, insanları ahlaki kurallarla birleştiren inançlar bütünüdür.\n"
            "• **Türleri:** Semavi dinler ve felsefi inançlar olarak ayrılır."
        )

    if "windows" in s or "format" in s:
        st.session_state["last_topic"] = "windows"
        return "Kanka Windows formatı için en az 8 GB USB'ye ISO yazdırıp BIOS'tan boot etmen ve diskleri biçimlendirmen gerekir."

    if "valorant" in s or "riot" in s:
        st.session_state["last_topic"] = "valorant"
        return "Kanka Valorant için Windows 11'de TPM 2.0 ve Secure Boot açık olmalı; Vanguard arka planda çalışmalıdır."

    # 6. CANLI WEB VE EVRENSEL ARAMA MOTORU (Dünyadan Güneşe Her Şey)
    web_result = wikipedia_canli_arama(s)
    if web_result:
        baslik, ozet = web_result
        st.session_state["last_topic"] = "wiki"
        st.session_state["last_wiki_title"] = baslik
        return (
            f"**{baslik} Hakkında Detaylı Bilgi:**\n\n"
            f"{ozet}\n\n"
            "--- \n"
            "**Bu konuyla ilgili başka ne öğrenmek istersin kanka? (Sadece numarayı yaz):**\n"
            "1. İstatistiksel ve Sayısal Numaraları\n"
            "2. Daha Derin ve Tarihi Detayı"
        )

    # 7. EĞER HİÇBİR YERDE BULAMAZSA (Hata Payı Yok)
    st.session_state["last_topic"] = "bilinmeyen"
    return (
        f"Kanka **'{ham_sorgu}'** çok spesifik veya mantık dışı bir kavram olabilir.\n\n"
        "Eğer bu yeni çıkan bir terimse veya belirli bir oyun/yazılım detayıysa bana ufak bir ipucu ver (örn: 'şu oyunun hilesi' veya 'şu yazılımın kodu' gibi), saniyesinde parçalayalım!"
    )

if prompt := st.chat_input("Haber, Matematik, Bilim... Aratmak istediğini yaz kanka!"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Kailer AI canlı ağları tarıyor..."):
            reply = kailer_nihai_motor(prompt)

        st.write(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})
