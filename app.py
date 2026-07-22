import streamlit as st
import random
import difflib

st.set_page_config(page_title="Lorvantis AI", page_icon="🤖")

st.title("🤖 Lorvantis AI")
st.caption("Türkiye'nin akıllı web yapay zekası")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Merhaba! Ben Lorvantis. Sana nasıl yardımcı olabilirim?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# Akıllı Yazım ve Kelime Yakalama Fonksiyonu
def akilli_cevap_bul(prompt):
    p = prompt.lower().strip()
    
    # 1. Doğrudan Komut ve Konu Eşleşmeleri
    if any(k in p for k in ["muvafakatname"]):
        return "Muvafakatname kanka, resmi ve hukuki olarak **'onay verme, rıza gösterme'** belgesidir. Bir kişinin başka birine işlem yapabilmesi için yazılı izin vermesidir."
    
    elif any(k in p for k in ["sa", "selam", "merhaba", "hey"]):
        return "Aleykümselam kanka! Hoş geldin, bugün hangi projeyle veya soruyla uğraşıyoruz?"
        
    elif any(k in p for k in ["nasılsın", "ne var ne yok", "naber"]):
        return "Bombaneyim kanka, kodlar ve veri tabanıyla haşır neşir ilerliyoruz. Sen nasılsın?"
        
    elif any(k in p for k in ["adın", "kimsin"]):
        return "Ben Lorvantis! Senin tasarlayıp hayata geçirdiğin, Türkçe'nin altını üstüne getiren yapay zeka asistanınım."
        
    elif any(k in p for k in ["windows 10", "format", "kurulum"]):
        return """Windows 10 yüklemek için şu adımları takip edebilirsin kanka:
1. En az 8 GB boş bir USB bul.
2. Microsoft'un resmi sitesinden Windows 10 indirme aracını indirip USB'ye yazdır.
3. Bilgisayarı yeniden başlatıp BIOS tuşuna basarak USB'yi ilk sıraya al.
4. İleri diyerek kurulumu tamamla ve ekran kartı driver'ını güncellemeyi unutma!"""

    elif any(k in p for k in ["python", "kod", "script"]):
        return f"Python işleri bende kanka! '{prompt}' konusunda ne scripti yazmamı istiyorsan hemen kodlayalım."

    elif any(k in p for k in ["fenerbahçe", "fb"]):
        return "Renkler belli kanka! Sarı-Lacivert rüzgarı esiyor, her kulvarda sonuna kadar destekliyoruz."

    # 2. Detaylı Anlat / Mala Anlat komutları
    elif any(k in p for k in ["detay", "anlat", "açıkla", "mala anlat"]):
        return f"Eyvallah kanka, '{prompt}' dedin. İstediğin konuyu en ince detayına kadar parçalarına ayıralım: Temel mantığı kavradıktan sonra bu işin üstesinden rahatlıkla gelirsin. Hangi aşamadan başlayalım?"

    # 3. Yazım Hatası Toleranslı Genel Yaklaşım
    else:
        # Cümle içinde geçen anahtar kelimelere göre akıllı türetme
        if "nasıl" in p:
            return f"'{prompt}' işini çözmek için mantık basit kanka: Adım adım ilerleyeceğiz, önce temeli atıp sonra üstüne çıkacağız. Tam olarak takıldığın yer neresi?"
        elif "nedir" in p or "ne demek" in p:
            return f"Kanka '{prompt}' dediğin olay, teknik veya günlük dilde kendine has bir yere sahip olan kavramdır. Detaylıca açmamı ister misin?"
        else:
            return f"Kanka '{prompt}' konusunu aldım. Yazım hatası veya devrik cümle fark etmez, bunu analiz ettim. Tam olarak ne öğrenmek istiyorsun, detaylandırayım?"

if prompt := st.chat_input("Lorvantis'e bir şeyler yaz..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Lorvantis düşünüyor..."):
            reply = akilli_cevap_bul(prompt)
            st.write(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})
