import customtkinter as ctk
import requests
import json
import threading

# Tema Ayarları (Tamamen Kapkara)
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

class LorvantisApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Lorvantis")
        self.geometry("450x650")
        self.configure(fg_color="#000000")

        # --- ÜST BAR (Header) ---
        self.top_frame = ctk.CTkFrame(self, fg_color="#000000", height=50)
        self.top_frame.pack(fill="x", side="top", padx=10, pady=5)

        self.menu_btn = ctk.CTkButton(
            self.top_frame, text="=", width=40, height=40, 
            font=("Arial", 24, "bold"), fg_color="transparent", 
            hover_color="#1a1a1a", text_color="white", command=self.toggle_drawer
        )
        self.menu_btn.pack(side="left")

        self.title_label = ctk.CTkLabel(
            self.top_frame, text="LORVANTIS", 
            font=("Arial", 16, "bold"), text_color="white"
        )
        self.title_label.pack(side="left", expand=True)

        self.settings_btn = ctk.CTkButton(
            self.top_frame, text="...", width=40, height=40, 
            font=("Arial", 20, "bold"), fg_color="transparent", 
            hover_color="#1a1a1a", text_color="white", command=self.open_settings
        )
        self.settings_btn.pack(side="right")

        # --- SOHBET ALANI ---
        self.chat_area = ctk.CTkScrollableFrame(self, fg_color="#000000")
        self.chat_area.pack(fill="both", expand=True, padx=10, pady=5)

        # --- ALT MESAJ BARI ---
        self.bottom_frame = ctk.CTkFrame(self, fg_color="#000000")
        self.bottom_frame.pack(fill="x", side="bottom", padx=15, pady=15)

        self.entry = ctk.CTkEntry(
            self.bottom_frame, placeholder_text="Mesaj yazın...",
            height=50, corner_radius=25, fg_color="#121212", 
            border_color="#2a2a2a", text_color="white", 
            placeholder_text_color="#666666", font=("Arial", 14)
        )
        self.entry.pack(fill="x", side="left", expand=True, padx=(0, 10))
        self.entry.bind("<Return>", lambda event: self.send_message())

        self.send_btn = ctk.CTkButton(
            self.bottom_frame, text="➔", width=50, height=50, 
            corner_radius=25, fg_color="#222222", hover_color="#333333",
            text_color="white", font=("Arial", 16, "bold"), command=self.send_message
        )
        self.send_btn.pack(side="right")

    def toggle_drawer(self):
        drawer = ctk.CTkToplevel(self)
        drawer.title("Sohbet Geçmişi")
        drawer.geometry("250x400")
        drawer.configure(fg_color="#0a0a0a")
        
        lbl = ctk.CTkLabel(drawer, text="Sohbet Geçmişi", font=("Arial", 16, "bold"))
        lbl.pack(pady=15)

    def open_settings(self):
        settings = ctk.CTkToplevel(self)
        settings.title("Ayarlar")
        settings.geometry("300x250")
        settings.configure(fg_color="#0a0a0a")

        lbl = ctk.CTkLabel(settings, text="Hesap Ayarları", font=("Arial", 16, "bold"))
        lbl.pack(pady=10)

    def send_message(self):
        user_text = self.entry.get().strip()
        if not user_text:
            return

        self.add_message(user_text, is_user=True)
        self.entry.delete(0, "end")

        threading.Thread(target=self.get_ai_response, args=(user_text,)).start()

    def add_message(self, text, is_user=False):
        msg_frame = ctk.CTkFrame(
            self.chat_area, 
            fg_color="#1f1f1f" if is_user else "#101010",
            corner_radius=15
        )
        msg_frame.pack(
            anchor="e" if is_user else "w", 
            pady=5, padx=5, fill="x"
        )

        sender = "Sen: " if is_user else "Lorvantis: "
        msg_label = ctk.CTkLabel(
            msg_frame, text=sender + text, text_color="white", 
            wraplength=350, justify="left", font=("Arial", 13)
        )
        msg_label.pack(padx=12, pady=8, anchor="w")

    def get_ai_response(self, prompt):
        try:
            # Akıllı uzunluk ayarı için güncellenmiş yönlendirme
            full_prompt = (
                "Senin adın Lorvantis. Samimi, kanka tarzında ve akıllı bir Türkçe yapay zekasın. "
                "Cevap uzunluğunu kullanıcının sorusuna göre ayarla: Basit selamlaşma veya tek kelimelik sorularda "
                "kısa ve öz cevap ver. Teknik anlatım, rehber veya detay gerektiren sorularda ise uydurmadan "
                "güncel bilgilerle detaylı ve uzun açıkla.\n\n"
                f"Kullanıcı: {prompt}\n"
                "Lorvantis:"
            )

            payload = {
                "model": "llama3.2",
                "prompt": full_prompt,
                "stream": False,
                "options": {
                    "temperature": 0.3, # Mantıklı yanıtlar vermesi için
                    "num_predict": 500  # Gerektiğinde uzun yazabilmesi için alan bırakıyoruz
                }
            }
            
            response = requests.post("http://localhost:11434/api/generate", json=payload)
            
            if response.status_code == 200:
                answer = response.json().get("response", "Cevap yok kanka.").strip()
            else:
                answer = "Ollama kapalı veya sorun var kanka."
        except Exception as e:
            answer = "Ollama kapalı, çalışmıyor kanka."

        self.add_message(answer, is_user=False)

if __name__ == "__main__":
    app = LorvantisApp()
    app.mainloop()
