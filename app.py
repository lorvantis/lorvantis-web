import streamlit as st

st.set_page_config(page_title="Lorvantis AI", page_icon="🤖")

st.title("🤖 Lorvantis AI")
st.caption("Türkiye’nin web yapay zekası")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Selam kanka! O ezber cümleleri çöpe attık. Ne sorsan çat diye cevabını alırsın. Ne kaynatıyoruz?"}]

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
        with st.spinner("Lorvantis düşünüyor..."):
            try:
                lower_input = full_user_input.lower()
                
                # Windows 10 kurulumu sorulursa direkt net rehber
                if "windows 10" in lower_input or "kurcam" in lower_input or "kurulum" in lower_input or "format" in lower_input:
                    reply = (
                        "Kanka Windows 10 kurulumu şöyle:\n\n"
                        "1. **8GB'lık boş bir flash bellek** bul ve Microsoft'un sitesinden *Media Creation Tool* ile Windows 10'u flash'a yazdır.\n"
                        "2. Bilgisayarı yeniden başlatırken anakartına göre **Boot Menüsü** tuşuna (Genelde F12, F11 veya Del) sürekli basıp USB'yi seç.\n"
                        "3. Kurulum ekranı açılınca 'Şimdi Yükle', ardından **Özel (Gelişmiş)** seçeneğini seç.\n"
                        "4. Eski Windows'un olduğu sürücüyü biçimlendir, o boş alanı seçip ileri de. İşlem tamamdır! 😎"
                    )
                elif "fenerbahçe" in lower_input or "fener" in lower_input:
                    reply = "Fener'in büyüklüğü tartışılmaz kanka! 💛💙 Başka ne merak ediyorsun?"
                elif "nasılsın" in lower_input or "naber" in lower_input:
                    reply = "Eyvallah kanka, sen nasılsın? Kodlama nasıl gidiyor? 🚀"
                else:
                    # O ezber "masaya yatırdık" lafı silindi, artık direkt soruya göre şekilleniyor:
                    reply = f"Kanka '{prompt}' konusuna gelince; hemen detaylıca bakalım, ne öğrenmek istiyorsun tam olarak? 🔥"
                    
            except Exception as e:
                reply = f"Kanka hata yok dedik, ufak bir şey oldu: {e} 😎"

            st.write(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})
