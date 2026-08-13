import streamlit as st

st.set_page_config(page_title="Kailer AI", page_icon="🤖")

st.title("🤖 Kailer AI")
st.caption("Türkiye'nin akıllı web yapay zekası (Kesintisiz Mod)")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Merhaba! Ben Kailer AI. Hangi konuyu merak ediyorsun, sor patlatalım kanka?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

def akilli_cevap_uret(prompt):
    p = prompt.lower().strip()
    
    # Selamlaşmalar
    if p in ["sa", "selam", "selamun aleykum", "selamın aleyküm", "merhaba", "hey"]:
        return "Aleykümselam kanka! Hoş geldin, ne arıyoruz bugün?"
    elif p in ["nasılsın", "naber", "ne var ne yok", "nasılsın?", "iyi misin"]:
        return "Bombaneyim kanka, fişek gibiyim! Sen nasılsın?"
    elif p in ["adın ne", "kimsin", "sen kimsin"]:
        return "Ben Kailer AI kanka! Senin yarattığın, Türkiye'nin en sağlam yapay zekasıyım."

    # Soru kategorilerine göre dinamik ve detaylı üretim
    if "?" in p or "nasıl" in p or "nedir" in p or "niye" in p or "kim" in p or "nerede" in p or "kaç" in p:
        return f"Kanka '{prompt}' konusunu derinlemesine analiz ettim. Bu tarz konularda en önemli detay, arka plandaki mantığı ve güncel verileri doğru oturtmaktır. Sorduğun soru gayet net; teknik veya genel kültür açısından bakarsak bu işin kökeni oldukça detaylı bir altyapıya dayanıyor. Başka bir detay veya merak ettiğin başka bir yer var mı?"
    
    # Genel kelimeler için
    return f"Kanka '{prompt}' ile ilgili bilgileri taradım. Bu konuda bilmen gereken en net şey, sistemin her türlü senaryoya ayak uydurabilecek kapasitede olmasıdır. Konuyu biraz daha açmak ister misin, hemen detaylandıralım!"

if prompt := st.chat_input("Kailer AI'a dilediğin soruyu sor..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Kailer AI tarıyor..."):
            reply = akilli_cevap_uret(prompt)

        st.write(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})
