import streamlit as st
import urllib.request
import urllib.parse
import json
import re
import xml.etree.ElementTree as ET

st.set_page_config(page_title="Kailer AI", page_icon="🤖")

st.title("🤖 Kailer AI")
st.caption("64 Kişilik Ekip İçin Gerçek Zamanlı ve Derin Bilgi Motoru")

# Hafıza ve Mesaj Geçmişi
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Kailer AI tam kapasite aktif! Artık hem gerçek detayları çekiyorum hem de ne dediğini harfi harfine anlıyorum."}]
if "last_topic" not in st.session_state:
    st.session_state["last_topic"] = None
if "last_wiki_title" not in st.session_state:
    st.session_state["last_wiki_title"] = None

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

def metni_temizle_ve_anla(metin):
    """Klavye kaymalarını düzeltir."""
    m = metin.lower().strip()
    hizli_yazim_sozlugu = {
        r'\bhqyır\b': 'hayır', r'\bhsyır\b': 'hayır',
        r'\bevt\b': 'evet', r'\bevtt\b': 'evet',
        r'\btm\b': 'tamam', r'\btmm\b': 'tamam',
        r'\bnbr\b': 'naber', r'\bslm\b': 'selam',
        r'\bmrdin\b': 'mardin', r'\bmardn\b': 'mardin',
        r'\bwndows\b': 'windows', r'\bwindos\b': 'windows',
        r'\bbilgilwr\b': 'bilgiler', r'\bbilgo\b': 'bilgi'
    }
    for hata, dogru in hizli_yazim_sozlugu.items():
        m = re.sub(hata, dogru, m)
    return m

def arama_sorgusunu_ayikla(sorgu):
    """'Singapur hakkında bilgiler' gibi cümlelerden asıl kelimeyi cımbızlar."""
    gereksizler = [r'\bhakkında\b', r'\bbilgiler\b', r'\bbilgi\b', r'\bnedir\b', r'\bkimdir\b', r'\bver\b', r'\bbana\b']
    temiz = sorgu
    for g in gereksizler:
        temiz = re.sub(g, '', temiz, flags=re.IGNORECASE).strip()
    return temiz if temiz else sorgu

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
    """Wikipedia'dan asıl kelimeyi bulur ve GERÇEK detay çeker."""
    try:
        hedef = arama_sorgusunu_ayikla(sorgu)
        search_url = f"https://tr.wikipedia.org/w/api.php?action=query&list=search&srsearch={urllib.parse.quote(hedef)}&utf8=&format=json"
        req_search = urllib.request.Request(search_url, headers={'User-Agent': 'KailerAI/1.0'})
        
        with urllib.request.urlopen(req_search, timeout=4) as response:
            search_data = json.loads(response.read().decode('utf-8'))
            if not search_data['query']['search']:
                return None
            
            best_title = search_data['query']['search'][0]['title']
            
            if detay_modu:
                # SAHTE METİN YERİNE GERÇEK DERİN DETAY ÇEKİCİ (7 CÜMLE)
                detail_url = f"https://tr.wikipedia.org/w/api.php?action=query&prop=extracts&exsentences=7&exlimit=1&titles={urllib.parse.quote(best_title)}&explaintext=1&format=json"
                req_det = urllib.request.Request(detail_url, headers={'User-Agent': 'KailerAI/1.0'})
                with urllib.request.urlopen(req_det, timeout=4) as det_response:
                    det_data = json.loads(det_response.read().decode('utf-8'))
                    pages = det_data['query']['pages']
                    for page_id in pages:
                        extract = pages[page_id].get('extract', 'Kanka bu konunun ekstra detayı sistemde yokmuş.')
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
    s = metni_temizle_ve_anla(ham_sorgu)
    last = st.session_state.get("last_topic")
    
    # 1. MATEMATİK
    has_operator = re.search(r'[\+\-\*\/]', ham_sorgu)
    math_match = re.search(r'^[\d\s\+\-\*\/\(\)\.]+$', ham_sorgu)
    if math_match and has_operator and len(ham_sorgu.strip()) > 1:
        try:
            sonuc = eval(ham_sorgu)
            return f"**Matematiksel İşlem Sonucu:**\n\nKanka uğraşmana gerek yok, `{ham_sorgu}` işleminin net sonucu: **{sonuc}**"
        except:
            pass

    # 2. HABER
    if "haber" in s or "son dakika" in s or "sondakika" in s or "gündem" in s:
        st.session_state["last_topic"] = "haber"
        return canli_haber_cek()

    # 3. KISA MUHABBET VE ANLAMSIZ ARAMALAR (Örn: "ne", "nasıl")
    if s in ["ne", "nasıl", "neden", "niye", "kim", "nerede", "kimsin"]:
        return "Kanka tek kelime yazdın, bağlamı kopardım. Neyi sorduğunu biraz daha açar mısın?"

    if s in ["selam", "selamun aleykum", "merhaba", "hey"]:
        return "Aleykümselam kanka! Sistemler online."
    elif s in ["hayır", "tamam", "yok", "istemiyorum"]:
        return "Anlaşıldı kanka, konuyu kapattık. Başka ne arıyoruz?"
    elif s in ["evet", "aynen", "olur"]:
        return "Tamamdır kanka, devam edelim."

    # 4. BAĞLAMSAL HAFIZA (Örn: "onları nasıl yapıcam")
    if ("nasıl" in s and ("yapıcam" in s or "yaparım" in s or "kurucam" in s or "kurarım" in s)):
        if last == "windows":
            return "**Windows Kurulum Adımları:**\n1. İnternetten 'Windows 10 ISO' indir.\n2. Rufus programı ile en az 8GB bir USB'ye yazdır.\n3. Bilgisayarı yeniden başlatıp BIOS'a gir (genelde F2 veya Delete).\n4. Boot menüsünden USB'yi 1. sıraya al.\n5. Kaydet ve çık, kurulum ekranı karşına gelecek!"
        elif last == "valorant":
            return "**Valorant Ayarları:**\nBIOS'a girip 'Security' sekmesinden 'Secure Boot'u Enable yapmalısın. AMD fTPM veya Intel PTT (TPM 2.0) ayarını da açıp kaydet."

    # 5. GERÇEK DETAY SİSTEMİ
    is_number_request = s in ["1", "2", "3"] or "numara" in s or "plaka" in s or "kod" in s or "detay" in s
    
    if is_number_request and last:
        if last == "mardin":
            if s == "1" or "numara" in s:
                return "**Mardin Resmî Numaraları:**\n• Plaka: **47**\n• Telefon: **0482**\n• Posta Kodu: **47000**"
            elif s == "2" or "detay" in s:
                return "**Mardin Mimari Detayı:**\nTaş evleri, abbaraları ve Deyrulzafaran Manastırı ile ünlüdür."
        
        elif st.session_state.get("last_wiki_title"):
            title = st.session_state["last_wiki_title"]
            if s == "1" or "numara" in s:
                return f"**{title} Hakkında Sayısal Veriler:**\nBu veriler kurumların resmi veritabanlarındadır."
            elif s == "2" or "detay" in s:
                # İŞTE BURADA SAHTE METİN YERİNE GERÇEK WIKIPEDIA DETAYI ÇEKİLİYOR
                _, detay_metni = wikipedia_canli_arama(title, detay_modu=True)
                return f"**{title} Hakkında Geniş Detay:**\n\n{detay_metni}"

    # 6. KESİN EŞLEŞMELER
    if "windows" in s or "format" in s:
        st.session_state["last_topic"] = "windows"
        return "Kanka Windows formatı için en az 8 GB USB'ye ISO yazdırıp BIOS'tan boot etmen ve diskleri biçimlendirmen gerekir."

    if "valorant" in s or "riot" in s:
        st.session_state["last_topic"] = "valorant"
        return "Kanka Valorant için Windows 11'de TPM 2.0 ve Secure Boot açık olmalı; Vanguard arka planda çalışmalıdır."

    # 7. CANLI WEB MOTORU (Ayıklanmış sorguyla hatasız arama)
    web_result = wikipedia_canli_arama(s, detay_modu=False)
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
            "2. Daha Derin ve Uzun Detayı"
        )

    # 8. BULUNAMAZSA (HATA EKRANI)
    st.session_state["last_topic"] = "bilinmeyen"
    return (
        f"Kanka **'{ham_sorgu}'** çok spesifik veya mantık dışı bir kavram olabilir.\n\n"
        "Eğer bu yeni çıkan bir terimse bana ufak bir ipucu ver!"
    )

if prompt := st.chat_input("Haber, Matematik, Bilim... Aratmak istediğini yaz kanka!"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Kailer AI canlı ağları tarıyor..."):
            reply = kailer_nihai_motor(prompt)

        st.write(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})
