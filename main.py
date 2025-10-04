import customtkinter as ctk
from tkinter import filedialog
import threading
import whisper
import moviepy.editor as mp
import os

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Logos Scribe")
        self.geometry("500x250")
        self._set_appearance_mode("dark")

        self.file_path = ""
        self.model = None

        # UI Elements
        self.select_button = ctk.CTkButton(self, text="Selecionar Arquivo", command=self.select_file)
        self.select_button.pack(pady=20)

        self.file_label = ctk.CTkLabel(self, text="Nenhum arquivo selecionado")
        self.file_label.pack(pady=10)

        self.transcribe_button = ctk.CTkButton(self, text="Iniciar Transcrição", command=self.start_transcription_thread, state="disabled")
        self.transcribe_button.pack(pady=10)

        self.status_label = ctk.CTkLabel(self, text="")
        self.status_label.pack(pady=10)

    def select_file(self):
        """Opens a file dialog to select an audio or video file."""
        self.file_path = filedialog.askopenfilename(
            title="Selecione um arquivo de áudio ou vídeo",
            filetypes=(("Arquivos de Mídia", "*.mp4 *.mkv *.mov *.avi *.mp3 *.wav *.m4a"),
                       ("Todos os arquivos", "*.*"))
        )
        if self.file_path:
            self.file_label.configure(text=os.path.basename(self.file_path))
            self.transcribe_button.configure(state="normal")
            self.status_label.configure(text="")
        else:
            self.file_label.configure(text="Nenhum arquivo selecionado")
            self.transcribe_button.configure(state="disabled")

    def start_transcription_thread(self):
        """Starts the transcription process in a new thread."""
        self.transcribe_button.configure(state="disabled")
        self.select_button.configure(state="disabled")
        self.status_label.configure(text="Iniciando...")
        threading.Thread(target=self.transcribe_file, daemon=True).start()

    def transcribe_file(self):
        """Handles the audio extraction and transcription."""
        try:
            # Load Whisper model
            if not self.model:
                self.update_status("Carregando modelo Whisper (base)...")
                self.model = whisper.load_model("base")

            # --- Audio Extraction ---
            self.update_status("Extraindo áudio...")
            audio_path = self.file_path
            if self.file_path.lower().endswith(('.mp4', '.mkv', '.mov', '.avi')):
                video = mp.VideoFileClip(self.file_path)
                audio_path = "temp_audio.wav"
                video.audio.write_audiofile(audio_path)

            # --- Transcription ---
            self.update_status("Transcrevendo áudio...")
            result = self.model.transcribe(audio_path, verbose=False, language="pt")

            # --- SRT Generation ---
            self.update_status("Gerando arquivo SRT...")
            self.generate_srt(result['segments'])

            # --- Cleanup ---
            if audio_path == "temp_audio.wav":
                os.remove(audio_path)

            self.update_status("Concluído! Arquivo .srt salvo.")

        except Exception as e:
            self.update_status(f"Erro: {e}")
        finally:
            self.after(0, self.reset_ui)

    def generate_srt(self, segments):
        """Formats the transcription result into an SRT file."""
        srt_path = os.path.splitext(self.file_path)[0] + ".srt"
        with open(srt_path, "w", encoding="utf-8") as srt_file:
            for i, seg in enumerate(segments):
                start_time = self.format_timestamp(seg['start'])
                end_time = self.format_timestamp(seg['end'])
                text = seg['text'].strip()
                srt_file.write(f"{i + 1}\n")
                srt_file.write(f"{start_time} --> {end_time}\n")
                srt_file.write(f"{text}\n\n")

    def format_timestamp(self, seconds):
        """Converts seconds to SRT timestamp format HH:MM:SS,ms."""
        assert seconds >= 0, "non-negative timestamp expected"
        milliseconds = round(seconds * 1000.0)

        hours = milliseconds // 3_600_000
        milliseconds %= 3_600_000

        minutes = milliseconds // 60_000
        milliseconds %= 60_000

        seconds = milliseconds // 1_000
        milliseconds %= 1_000

        return f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"

    def update_status(self, message):
        """Updates the status label in a thread-safe way."""
        self.after(0, lambda: self.status_label.configure(text=message))

    def reset_ui(self):
        """Resets the UI to its initial state after transcription."""
        self.transcribe_button.configure(state="normal")
        self.select_button.configure(state="normal")


if __name__ == "__main__":
    app = App()
    app.mainloop()