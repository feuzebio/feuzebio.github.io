import tkinter as tk
from tkinter import filedialog, messagebox
from gtts import gTTS
import threading

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Conversor TTS (Texto para Fala)")
        self.root.geometry("500x400")

        # --- Widgets ---
        self.label_instrucao = tk.Label(root, text="Digite ou cole o texto abaixo:", wraplength=480, justify="left")
        self.label_instrucao.pack(pady=(10, 5))

        self.text_area = tk.Text(root, wrap="word", height=15, width=60)
        self.text_area.pack(pady=5, padx=10, expand=True, fill="both")

        self.convert_button = tk.Button(root, text="Converter e Salvar", command=self.iniciar_conversao)
        self.convert_button.pack(pady=10)

        self.status_label = tk.Label(root, text="Aguardando texto...", fg="gray")
        self.status_label.pack(pady=5)

    def iniciar_conversao(self):
        texto = self.text_area.get("1.0", "end-1c").strip()

        if not texto:
            messagebox.showwarning("Aviso", "Por favor, insira um texto para converter.")
            return

        caminho_arquivo = filedialog.asksaveasfilename(
            defaultextension=".mp3",
            filetypes=[("Arquivos MP3", "*.mp3"), ("Todos os arquivos", "*.*")],
            title="Salvar arquivo de áudio"
        )

        if not caminho_arquivo:
            self.status_label.config(text="Operação cancelada pelo usuário.", fg="orange")
            return

        # Desabilitar o botão e atualizar o status
        self.convert_button.config(state="disabled")
        self.status_label.config(text="Convertendo... Por favor, aguarde.", fg="blue")

        # Executar a conversão em uma thread separada para não bloquear a GUI
        thread = threading.Thread(target=self.realizar_conversao, args=(texto, caminho_arquivo))
        thread.start()

    def realizar_conversao(self, texto, caminho_arquivo):
        try:
            tts = gTTS(text=texto, lang='pt-br', slow=False)
            tts.save(caminho_arquivo)
            # Atualizar a GUI na thread principal
            self.root.after(0, self.notificar_sucesso, caminho_arquivo)
        except Exception as e:
            # Atualizar a GUI na thread principal
            self.root.after(0, self.notificar_erro, e)

    def notificar_sucesso(self, caminho_arquivo):
        self.status_label.config(text=f"Áudio salvo com sucesso!", fg="green")
        messagebox.showinfo("Sucesso", f"O arquivo de áudio foi salvo em:\n{caminho_arquivo}")
        self.convert_button.config(state="normal")

    def notificar_erro(self, erro):
        self.status_label.config(text="Erro na conversão.", fg="red")
        messagebox.showerror("Erro", f"Ocorreu um erro durante a conversão:\n{erro}\n\nVerifique sua conexão com a internet.")
        self.convert_button.config(state="normal")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()