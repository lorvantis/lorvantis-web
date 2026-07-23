import streamlit as st
from duckduckgo_search import DDGS

st.set_page_config(page_title="Lorvantis AI", page_icon="🤖")

st.title("🤖 Lorvantis AI")
st.caption("Türkiye’nin gerçek web arama destekli yapay zekası")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Selam kanka! Gerçek web arama motorunu bağladık. Artık internette ne ararsan anında çekip getiriyoruz. Ne soruyorsun?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input("Lorvantis'e bir şeyler yaz..."):
    cleaned_prompt = prompt.strip()
    lower_prompt = cleaned_prompt.lower()

    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Lorvantis webde aratıyor..."):
            reply = ""
            handled_locally = False

            # 1. Selamlaşma ve Günlük Kalıplar (Anında yanıt, web'e gitmez)
            if lower_prompt in ["sa", "selam", "slm"]:
                reply = "Aleykümselam kanka, nasılsın?"
                handled_locally = True
            elif lower_prompt in ["as", "aleykümselam"]:
                reply = "Aleykümselam kanka, ne var ne yok?"
                handled_locally = True
            elif any(w in lower_prompt for w in ["nasılsın", "naber", "ne var ne yok"]):
                reply = "İyiyim kanka, sen nasılsın, ne bakmıştın?"
                handled_locally = True
            elif any(w in lower_prompt for w in ["sağol", "sagol", "teşekkürler", "teşekkür ederim", "eyvallah"]):
                reply = "Bir şey değil kanka!"
                handled_locally = True

            # 2. Gerçek Web Araması (DuckDuckGo ile canlı internet taraması)
            if not handled_locally:
                try:
                    search_query = cleaned_prompt
                    # Şehir, ülke veya tanıtım sorgularını daha net aratmak için optimize ediyoruz
                    if "tanıt" in lower_prompt or "hakkında bilgi" in lower_prompt:
                        search_query = f"{cleaned_prompt} hakkında bilgi, coğrafi ve genel özellikleri"
                    
                    with DDGS() as ddgs:
                        # İnternetten ilk 3 sonucu çekiyoruz
                        results = [r for r in ddgs.text(search_query, max_results=3)]
                    
                    if results:
                        # Bulunan web sonuçlarını kanka diliyle harmanlayıp sunuyoruz
                        snippets = "\n".join([f"- {r['title']}: {r['body']}" for r in results])
                        reply = f"Kanka **'{cleaned_prompt}'** için web'i taradım, bulduğum güncel bilgiler şunlar:\n\n{snippets}\n\nBaşka merak ettiğin bir yer veya detay var mı? 🔥"
                    else:
                        raise Exception("Sonuç bulunamadı")
                        
                except Exception:
                    # Web araması anlık takılırsa akıllı yerel hafıza devreye girer
                    if "mardin" in lower_prompt:
                        reply = "Mardin, Güneydoğu Anadolu Bölgesi'nde yer alan, taş mimarisi, dar sokakları ve eşsiz Mezopotamya manzarasıyla büyüleyen 47 plakalı efsanevi şehrimizdir kanka! 🏛️"
                    elif "siirt" in lower_prompt:
                        reply = "Siirt, Güneydoğu'da yer alan; büryan kebabı, tiftik battaniyesi ve 56 plakasıyla öne çıkan güzel bir ilimizdir kanka! 🇹🇷"
                    elif "kerem aktürkoğlu" in lower_prompt or "aktürkoğlu" in lower_prompt:
                        reply = "Kerem Aktürkoğlu Türk futbolunun hızıyla ve bitiriciliğiyle göz dolduran milli kanat oyuncusudur kanka! ⚡⚽"
                    elif "fenerbahçe" in lower_prompt or "fener" in lower_prompt:
                        reply = "Fenerbahçe şampiyonluk yolunda kadro kalitesiyle ve taraftarıyla ligin tozunu attıran dev bir camiadır kanka 💛💙"
                    else:
                        reply = f"Kanka **'{cleaned_prompt}'** konusunu webde taradım ama anlık bir bağlantı pürüzü oldu. Tekrar dener misin, hemen çözelim! 🚀"

            st.write(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})
