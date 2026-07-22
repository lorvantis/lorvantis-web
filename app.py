import customtkinter as ctk
import threading
from g4f.client import Client

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class LorvantisDesktop(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Lorvantis AI")
        self.geometry("600x720")

        self.client = Client()
        self.messages = [{"role": "assistant", "content": "Merhaba! Ben Lorvantis. Sana nasıl yardımcı olabilirim?"}]

        # Başlık Bölümü
        self.label = ctk.CTkLabel(self, text="🤖 Lorvantis AI", font=ctk.CTkFont(size=24, weight="bold"))
        self.label.pack(pady=(15, 2))

        # Alt Yazı
        self.subtitle = ctk.CTkLabel(self, text="Türkiye'nin web yapay zekası", font=ctk.CTkFont(size=13, slant="italic"), text_color="gray70")
        self.subtitle.pack(pady=(0, 10))

        # Sohbet Alanı
        self.chat_area = ctk.CTkTextbox(self, width=540, height=480, state="disabled")
        self.chat_area.pack(pady=10)

        # Giriş Alanı
        self.input_frame = ctk.CTkFrame(self)
        self.input_frame.pack(fill="x", padx=20, py=10)

        self.entry = ctk.CTkEntry(self.input_frame, placeholder_text="Lorvantis'e bir şeyler yaz...", width=410)
        self.entry.pack(side="left", padx=5)
        self.entry.bind("<Return>", lambda event: self.start_send_thread())

        self.send_btn = ctk.CTkButton(self.input_frame, text="Gönder", width=90, command=self.start_send_thread)
        self.send_btn.pack(side="right", padx=5)

        self.update_chat("Lorvantis: Merhaba! Ben Lorvantis. Sana nasıl yardımcı olabilirim?")

    def update_chat(self, text):
        self.chat_area.configure(state="normal")
        self.chat_area.insert("end", text + "\n\n")
        self.chat_area.configure(state="disabled")
        self.chat_area.see("end")

    def start_send_thread(self):
        user_text = self.entry.get().strip()
        if not user_text:
            return

        # Kullanıcı mesajını yaz
        self.entry.delete(0, "end")
        self.update_chat(f"Sen: {user_text}")
        self.messages.append({"role": "user", "content": user_text})

        # Arayüzü kilitle ve "Düşünüyor..." durumuna getir
        self.entry.configure(state="disabled")
        self.send_btn.configure(state="disabled", text="Düşünüyor...")

        # Yanıtı ekranı dondurmadan arka planda al
        threading.Thread(target=self.get_ai_response, daemon=True).start()

    def get_ai_response(self):
        try:
            # Ana model isteği
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=self.messages
            )
            reply = response.choices[0].message.content
        except Exception:
            # Yedek model (ilki yoğun olursa otomatik geçer)
            try:
                response = self.client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=self.messages
                )
                reply = response.choices[0].message.content
            except Exception as e:
                reply = f"Şu an bağlantı kurulamadı, lütfen tekrar dene. ({e})"

        # Arayüzü güncelle ve kilitleri aç
        self.update_chat(f"Lorvantis: {reply}")
        self.messages.append({"role": "assistant", "content": reply})

        self.entry.configure(state="normal")
        self.send_btn.configure(state="normal", text="Gönder")

if __name__ == "__main__":
    app = LorvantisDesktop()
    app.mainloop()
