import streamlit as st
import random

st.set_page_config(page_title="Lorvantis AI", page_icon="🤖")

st.title("🤖 Lorvantis AI")
st.caption("Türkiye'nin web yapay zekası")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Merhaba! Ben Lorvantis. Sana nasıl yardımcı olabilirim?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input("Lorvantis'e bir şeyler yaz..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Lorvantis düşünüyor..."):
            p = prompt.lower().strip()
            
            # 1. Selamlaşma ve Hal Hatır
            if any(k in p for k in ["sa", "selam", "merhaba", "hey", "selamün aleyküm"]):
                reply = "Aleykümselam kanka! Ne var ne yok, bugün hangi projeyle uğraşıyoruz?"
            elif any(k in p for k in ["nasılsın", "ne var ne yok", "iyi misin", "naber"]):
                reply = "İyilik kanka, kodlar arasında koşturmaca devam ediyor. Sen nasılsın?"
            elif any(k in p for k in ["adın ne", "kimsin", "sen kim"]):
                reply = "Ben Lorvantis! Senin tasarladıp geliştirdiğin yerli ve milli web yapay zeka asistanınım."

            # 2. Teknik / Kurulum Konuları (Mala anlatır gibi uzun ve detaylı)
            elif any(k in p for k in ["windows", "format", "kur", "yükle", "iso", "usb"]):
                if "mala anlat" in p or "detay" in p or "uzun" in p:
                    reply = """Mala anlatır gibi adım adım Windows 10 kurulumu kanka, ezberle:
1. **USB Hazırlığı:** İçinde önemli bir şey olmayan en az 8 GB'lık bir flash bellek bul.
2. **Rufus ve ISO:** Microsoft'un sitesinden resmi Windows 10 ISO dosyasını indir. Rufus programını açıp ISO'yu flash belleğe yazdır (Bu işlem flash'ı sıfırlar, dikkat!).
3. **BIOS Ayarı:** Bilgisayarı kapatıp açarken sürekli F12, F8 veya Del tuşuna basarak BIOS'a gir. Boot menüsünden hazırladığın USB belleği ilk sıraya al ve kaydedip çık.
4. **Kurulum Ekranı:** Bilgisayar USB'den açılınca dil seç, "İleri" de ve "Şimdi Yükle"ye bas.
5. **Disk Seçimi:** C diski dahil her şeyi biçimlendir (temiz kurulum için), Windows'u kuracağın ana diski seçip ileri de. 
6. **Bitiş:** Bilgisayar birkaç kez yeniden başlayacak. Sonra masaüstü gelir, ilk iş olarak ekran kartı driver'ını kurmayı unutma!"""
                else:
                    reply = "Windows 10 kurmak için flash belleğe ISO yazdırıp BIOS'tan boot etmen yeterli kanka. Detaylı anlatmamı ister misin?"

            # 3. Yazılım / Kodlama
            elif any(k in p for k in ["python", "kod", "script", "hata", "error", "streamlit"]):
                reply = f"Kod işi bende kanka! '{prompt}' konusunda takıldığın yer neresi? İstediğin fonksiyonu veya mantığı hemen yazabilirim."

            # 4. Spor / Futbol
            elif any(k in p for k in ["fenerbahçe", "fb", "maç", "lig", "futbol"]):
                reply = "Renkler belli kanka! Sarı-Lacivert rüzgarı esiyor, her kulvarda sonuna kadar destekliyoruz."

            # 5. Esnek Genel Yaklaşım (Her kelimeyi harmanlayan akıllı yedek)
            else:
                # Cümledeki anahtar kelimeleri yakalayıp ona göre akıllıca türetelim
                if "nasıl" in p:
                    reply = f"'{prompt}' konusunu çözmek için mantık basit kanka: Adım adım ilerleyeceğiz, önce temeli atıp sonra üstüne çıkacağız. Tam olarak takıldığın yer neresi?"
                elif "nedir" in p or "ne demek" in p:
                    reply = f"Kanka '{prompt}' dediğin olay kısaca şu: Temel mantığını kavradıktan sonra her şey çorap söküğü gibi gelir. Merak ettiğin alt detay var mı?"
                elif "neden" in p or "niye" in p:
                    reply = f"'{prompt}' olmasının sebebi tamamen sistemin işleyiş mantığıyla alakalı kanka. İstiyorsan bunu daha derinlemesine açabilirim."
                else:
                    # Asla tıkanmaz, her cümleye mantıklı bir sohbet tonu üretir
                    cevaplar = [
                        f"Anladım kanka, '{prompt}' dedin. Bu konunun altından rahatlıkla kalkarız, detay ister misin?",
                        f"'{prompt}' konusunu aklıma yazdım dostum. Buna benzer projelerde hep bu mantık dönüyor, nasıl devam edelim?",
                        f"Güzel konu kanka: '{prompt}'. Bununla ilgili ne yapmak istiyorsun, tam olarak hedefimiz ne?"
                    ]
                    reply = random.choice(cevaplar)

            st.write(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})
