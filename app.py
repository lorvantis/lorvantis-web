import streamlit as st

st.set_page_config(page_title="Lorvantis AI", page_icon="🤖")

st.title("🤖 Lorvantis AI")
st.caption("Türkiye'nin akıllı web yapay zekası")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Merhaba! Ben Lorvantis. Sana nasıl yardımcı olabilirim?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

def akilli_cevap_bul(prompt):
    p = prompt.lower().strip()
    
    # 1. Net Selamlaşmalar (Sadece cümle başı veya tam kelimeyse selam al, "detay" içinde "sa" geçince selam çakmasın!)
    if p in ["sa", "selam", "merhaba", "hey", "selamün aleyküm"] or p.startswith("selam "):
        return "Aleykümselam kanka! Hoş geldin, bugün hangi projeyle veya soruyla uğraşıyoruz?"
        
    elif any(k in p for k in ["nasılsın", "ne var ne yok", "naber", "iyi misin"]):
        return "Bombaneyim kanka, kodlar ve veri tabanıyla haşır neşir ilerliyoruz. Sen nasılsın?"
        
    elif any(k in p for k in ["adın ne", "kimsin", "sen kim"]):
        return "Ben Lorvantis! Senin tasarlayıp hayata geçirdiğin, Türkçe'nin altını üstüne getiren yapay zeka asistanınım."
        
    elif "muvafakatname" in p:
        return "Muvafakatname kanka, resmi ve hukuki olarak **'onay verme, rıza gösterme'** belgesidir. Bir kişinin başka birine işlem yapabilmesi için yazılı izin vermesidir."

    elif "windows 10" in p or "format" in p or "kurulum" in p:
        return """Windows 10 yüklemek için şu adımları takip edebilirsin kanka:
1. En az 8 GB boş bir USB bul.
2. Microsoft'un resmi sitesinden Windows 10 indirme aracını indirip USB'ye yazdır.
3. Bilgisayarı yeniden başlatıp BIOS tuşuna basarak USB'yi ilk sıraya al.
4. İleri diyerek kurulumu tamamla ve ekran kartı driver'ını güncellemeyi unutma!"""

    elif "python" in p or "kod" in p or "script" in p:
        return f"Python işleri bende kanka! '{prompt}' konusunda ne scripti yazmamı istiyorsan hemen kodlayalım."

    elif "fenerbahçe" in p or "fb" in p:
        return "Renkler belli kanka! Sarı-Lacivert rüzgarı esiyor, her kulvarda sonuna kadar destekliyoruz."

    # 2. Detaylı / Mala Anlat / Açıkla istekleri
    elif any(k in p for k in ["detay", "anlat", "açıkla", "mala anlat", "uzun"]):
        return f"Eyvallah kanka, '{prompt}' dedin. İstediğin konuyu en ince detayına kadar parçalarına ayıralım: Temel mantığı kavradıktan sonra bu işin üstesinden rahatlıkla gelirsin. Tam olarak hangi noktayı açmamı istiyorsun?"

    # 3. Esnek Genel Yaklaşım (Yazım hatalarını ve devrik cümleleri tolere eder)
    else:
        if "nasıl" in p:
            return f"'{prompt}' işini çözmek için mantık basit kanka: Adım adım ilerleyeceğiz, önce temeli atıp sonra üstüne çıkacağız. Süreci başlatmak için ilk adımı nereye atalım?"
        elif "nedir" in p or "ne demek" in p:
            return f"Kanka '{prompt}' dediğin olay, teknik veya günlük dilde kendine has bir yere sahip olan kavramdır. Detaylıca açmamı ister misin?"
        else:
            return f"Kanka '{prompt}' konusunu aldım. Yazım hatası veya devrik cümle fark etmez, bunu analiz ettim. Tam olarak ne öğrenmek istiyorsun, hemen detaylandırıp cevap vereyim!"

if prompt := st.chat_input("Lorvantis'e bir şeyler yaz..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Lorvantis düşünüyor..."):
            reply = akilli_cevap_bul(prompt)
            st.write(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})
