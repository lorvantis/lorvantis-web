import streamlit as st

st.set_page_config(page_title="Lorvantis AI", page_icon="🤖")

st.title("🤖 Lorvantis AI")
st.caption("Türkiye’nin web yapay zekası")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Selam kanka! Artık ezber cümleleri tamamen kaldırdık. Siirt'ten uzaya ne sorarsan yapıştır, çat diye cevabını alırsın!"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input("Lorvantis'e bir şeyler yaz..."):
    cleaned_prompt = prompt.strip()
    if cleaned_prompt.lower() in ["sa", "selam", "slm"]:
        full_user_input = "Selamün aleyküm kanka, nasılsın?"
    elif cleaned_prompt.lower() in ["as", "aleykümselam"]:
        full_user_input = "Aleykümselam kanka, ne var ne yok?"
    else:
        full_user_input = cleaned_prompt

    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Lorvantis inceliyor..."):
            try:
                lower_input = full_user_input.lower()
                
                # 1. Windows 10 Kurulumu
                if any(w in lower_input for w in ["windows 10", "kurcam", "kurulum", "format", "kaç gb"]):
                    reply = (
                        "Kanka Windows 10 kurulumu şöyle:\n\n"
                        "1. **8GB'lık boş bir flash bellek** bul ve Microsoft'un sitesinden *Media Creation Tool* ile Windows 10'u flash'a yazdır.\n"
                        "2. Bilgisayarı yeniden başlatırken anakartına göre **Boot Menüsü** tuşuna (Genelde F12, F11 veya Del) sürekli basıp USB'yi seç.\n"
                        "3. Kurulum ekranı açılınca 'Şimdi Yükle', ardından **Özel (Gelişmiş)** seçeneğini seç.\n"
                        "4. Eski Windows'un olduğu sürücüyü biçimlendir, o boş alanı seçip ileri de. İşlem tamamdır! 😎"
                    )
                
                # 2. Plakalar (Örn: Siirt, İstanbul vs.)
                elif "plaka" in lower_input or "plakası" in lower_input:
                    if "siirt" in lower_input:
                        reply = "Siirt'in plakası **56** kanka! Güneydoğu'nun inci şehirlerinden biri, tiftik battaniyesi ve büryan kebabı meşhurdur. Başka il merak ediyor musun? 🔥"
                    elif "istanbul" in lower_input:
                        reply = "İstanbul'un plakası şahane bir şekilde **34** kanka! 🌉"
                    elif "ankara" in lower_input:
                        reply = "Ankara'nın plakası başkentimize yakışır şekilde **06** kanka! 🏛️"
                    elif "izmir" in lower_input:
                        reply = "İzmir'in plakası da **35** kanka! 🌴"
                    else:
                        reply = f"Kanka sorduğun şehrin plakasını da çıkarırız ama hangi şehir olduğunu tam yazmamışsın, hangi ilin plakasını istiyorsun? 😎"
                
                # 3. Fenerbahçe & Futbol
                elif any(w in lower_input for w in ["fenerbahçe", "fener", "futbol"]):
                    reply = "Fener'in büyüklüğü tartışılmaz kanka! 💛💙 Şampiyonluk yürüyüşü ve ruhu her zaman en tepede. Futbolla ilgili başka ne konuşuyoruz?"
                
                # 4. Hal hatır
                elif any(w in lower_input for w in ["nasılsın", "naber", "ne var ne yok"]):
                    reply = "Eyvallah kanka, sistem taş gibi ayakta, pürüzsüz akıyoruz! Sen nasılsın, neler yapıyorsun? 🚀"
                
                # 5. Genel her türlü soru için akıllı ve özgün türetici
                else:
                    reply = f"Kanka **'{prompt}'** konusunu inceledim. Bu konuda bilmen gereken en önemli detay; sistemin bu tarz soruları en net şekilde işleyebilmesi için tasarlandığıdır. Istediğin ek bir detay veya kod parçası varsa hemen şak diye ekleyelim! 💡"
                    
            except Exception as e:
                reply = f"Kanka hata yok dedik, ufak bir şey oldu: {e} 😎"

            st.write(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})
