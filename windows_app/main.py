import tkinter as tk
from tkinter import scrolledtext, messagebox
from gtts import gTTS
from playsound import playsound
import tempfile
import os
import threading

class TTSApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Conversor de Texto para Áudio")
        self.root.geometry("500x350")

        # Instrução
        self.instruction_label = tk.Label(
            root,
            text="Insira o texto que deseja converter para áudio na caixa abaixo.",
            wraplength=480,
            justify="center"
        )
        self.instruction_label.pack(pady=10)

        # Área de texto
        self.text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=60, height=10)
        self.text_area.pack(pady=10, padx=10)

        # Botão para gerar áudio
        self.generate_button = tk.Button(root, text="Gerar e Ouvir", command=self.start_tts_thread)
        self.generate_button.pack(pady=5)

        # Rótulo de status
        self.status_label = tk.Label(root, text="", fg="green")
        self.status_label.pack(pady=5)

    def start_tts_thread(self):
        # Inicia a operação em uma nova thread para não bloquear a GUI
        thread = threading.Thread(target=self.generate_and_play)
        thread.daemon = True
        thread.start()

    def generate_and_play(self):
        input_text = self.text_area.get("1.0", tk.END).strip()

        if not input_text:
            messagebox.showerror("Erro", "Nenhum texto inserido. Por favor, digite ou cole um texto.")
            return

        try:
            # Desabilitar o botão e mostrar status
            self.generate_button.config(state=tk.DISABLED)
            self.status_label.config(text="Gerando áudio...", fg="blue")

            tts = gTTS(text=input_text, lang='pt', slow=False)

            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
                temp_path = temp_audio.name
                tts.save(temp_path)

            self.status_label.config(text="Reproduzindo...", fg="blue")
            playsound(temp_path)

            # Limpeza
            os.remove(temp_path)

            self.status_label.config(text="Áudio reproduzido com sucesso!", fg="green")

        except Exception as e:
            error_message = f"Ocorreu um erro: {e}"
            if "Failed to establish a new connection" in str(e):
                error_message = "Erro de conexão. Verifique sua internet."

            messagebox.showerror("Erro", error_message)
            self.status_label.config(text="Falha na conversão.", fg="red")
        finally:
            # Reabilitar o botão
            self.generate_button.config(state=tk.NORMAL)


if __name__ == "__main__":
    app_root = tk.Tk()
    app = TTSApp(app_root)
    app_root.mainloop()