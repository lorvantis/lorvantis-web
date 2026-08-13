import streamlit as st
import requests
import time

st.set_page_config(page_title="Kailer AI", page_icon="🤖")

st.title("🤖 Kailer AI")
st.caption("Türkiye'nin akıllı web yapay zekası (Ultra Stabil Mod)")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Merhaba! Ben Kailer AI. Neyi aramamı istersin kanka?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# 429 YEMEMEK İÇİN AKILLI YEREL ARAMA VE BİLGİ BANKASI MOTORU
def yerel_ve_hizli_cevap(prompt):
    p = prompt.lower().strip()
    
    # Selamlaşmalar
    if p in ["sa", "selam", "selamun aleykum", "selamın aleyküm", "merhaba", "hey"]:
        return "Aleykümselam kanka! Hoş geldin, ne arıyoruz bugün?"
    elif p in ["nasılsın", "naber", "ne var ne yok", "nasılsın?", "iyi misin"]:
        return "Bombaneyim kanka, arama motoru gibi fişek gibiyim! Sen nasılsın?"
    elif p in ["adın ne", "kimsin", "sen kimsin"]:
        return "Ben Kailer AI kanka! Senin yarattığın, Türkiye'nin en sağlam yapay zekasıyım."
    
    # Sık sorulan bazı genel bilgileri harici sunucuya gitmeden (429'a takılmadan) anında veren yerel veritabanı
    if "türkiye'nin başkenti" in p or "ankara nerede" in p:
        return "Türkiye'nin başkenti Ankara'dır kanka. İç Anadolu Bölgesi'nde yer alır."
    elif "fenerbahçe" in p:
        return "Fenerbahçe Spor Kulübü, 1907 yılında İstanbul'da kurulan Türkiye'nin en büyük ve köklü spor kulüplerinden biridir kanka!"
    elif "lorvantis" in p:
        return "Lorvantis AI, senin ellerinle Python ve Streamlit kullanarak geliştirdiğin efsanevi yapay zeka projesindir kanka!"
        
    return None

if prompt := st.chat_input("Kailer AI'a bir şeyler yaz veya arat..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Kailer AI tarıyor..."):
            
            # Önce yerel motora bakıyoruz (Sıfır 429, anında cevap)
            reply = yerel_ve_hizli_cevap(prompt)
            
            if not reply:
                api_url = "https://text.pollinations.ai/"
                system_prompt = "Senin adın Kailer AI. Kullanıcıyla 'kanka' diyerek samimi bir dille konuş. İnternetteki en doğru bilgiyi net, detaylı ve efsanevi bir kalitede sun. Arama yaptığını belli etme."
                
                messages_payload = [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ]
                
                payload = {
                    "messages": messages_payload,
                    "model": "openai"
                }
                
                basarili = False
                son_hata = ""
                
                # Tek ve net deneme (Sunucuyu darlamamak için üst üste istek atmıyoruz)
                try:
                    res = requests.post(
                        api_url,
                        json=payload,
                        headers={'Content-Type': 'application/json'},
                        timeout=10
                    )
                    
                    if res.status_code == 200:
                        cevap_metni = res.text.strip()
                        if cevap_metni:
                            reply = cevap_metni
                            basarili = True
                    elif res.status_code == 429:
                        son_hata = "429 (Aşırı İstek)"
                    else:
                        son_hata = f"HTTP {res.status_code}"
                except Exception as e:
                    son_hata = "Bağlantı Kesintisi"
                
                # Eğer dış sunucu 429 verirse sistemi kilitlemek yerine kullanıcıyı patlatmayacak akıllı yedek cevap
                if not basarili:
                    if "429" in son_hata:
                        reply = "Kanka dışarıdaki arama sunucusu şu an anlık çok kalabalık, 429 uyarısı çaktı. 3-5 saniye bekleyip tekrar yazarsan anında fırlatacağım!"
                    else:
                        reply = f"Kanka anlık bir ağ takılması oldu (Hata: {son_hata}). Aynen devam edelim, soruyu bir daha yazar mısın?"

            st.write(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})
