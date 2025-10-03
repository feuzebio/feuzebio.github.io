"""
Um aplicativo que converte texto para áudio em Português.
"""

import toga
from toga.style import Pack
from toga.style.pack import COLUMN, PADDING
from gtts import gTTS, gTTSError
import tempfile
import os
import threading
from rubicon.java import JavaClass, JavaInterface, platform


# Android-specific imports
if platform.is_android:
    MediaPlayer = JavaClass("android.media.MediaPlayer")
    CompletionListener = JavaInterface("android.media.MediaPlayer$OnCompletionListener")

class AudioPlayer(CompletionListener):
    def __init__(self, app, audio_file_path):
        super().__init__()
        self.app = app
        self.audio_file_path = audio_file_path
        self.media_player = MediaPlayer()
        self.media_player.setOnCompletionListener(self)

    def play(self):
        try:
            self.media_player.setDataSource(self.audio_file_path)
            self.media_player.prepare()
            self.media_player.start()
        except Exception as e:
            self.app.main_window.error_dialog("Erro de Reprodução", f"Não foi possível reproduzir o áudio: {e}")
            self.cleanup()

    def onCompletion(self, player):
        self.cleanup()

    def cleanup(self):
        self.media_player.release()
        if os.path.exists(self.audio_file_path):
            os.remove(self.audio_file_path)
        self.app.convert_button.enabled = True


class ConversordeTextoparaÁudio(toga.App):
    def startup(self):
        """Construct and show the Toga application."""
        main_box = toga.Box(style=Pack(direction=COLUMN, padding=10))

        instruction_label = toga.Label(
            "Insira o texto que deseja converter para áudio na caixa abaixo.",
            style=Pack(padding=(0, 0, 5, 0))
        )
        main_box.add(instruction_label)

        self.text_input = toga.MultilineTextInput(
            style=Pack(flex=1),
            placeholder="Digite seu texto aqui..."
        )
        main_box.add(self.text_input)

        self.convert_button = toga.Button(
            "Converter e Ouvir",
            on_press=self.on_convert_button_press,
            style=Pack(padding=10)
        )
        main_box.add(self.convert_button)

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()

    def on_convert_button_press(self, widget):
        """Handle button press: disable button and start conversion in a new thread."""
        self.convert_button.enabled = False
        thread = threading.Thread(target=self.generate_and_play_audio)
        thread.start()

    def generate_and_play_audio(self):
        """Generate the audio file from text and then play it."""
        text = self.text_input.value
        if not text.strip():
            self.main_window.info_dialog("Texto Vazio", "Por favor, insira um texto para converter.")
            self.convert_button.enabled = True
            return

        audio_file_path = None
        try:
            # Generate TTS
            tts = gTTS(text=text, lang='pt', tld='com.br')
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
                audio_file_path = temp_file.name
                tts.save(audio_file_path)

            # Use the native player
            if platform.is_android:
                player = AudioPlayer(self, audio_file_path)
                player.play()
            else:
                # Fallback for non-Android platforms (e.g., desktop testing)
                self.main_window.info_dialog("Plataforma não suportada", "A reprodução de áudio só funciona no Android.")
                self.convert_button.enabled = True


        except gTTSError as e:
            self.main_window.error_dialog(
                "Erro de Conversão",
                f"Não foi possível converter o texto. Verifique sua conexão com a internet. Erro: {e}"
            )
            if audio_file_path and os.path.exists(audio_file_path):
                os.remove(audio_file_path)
            self.convert_button.enabled = True
        except Exception as e:
            self.main_window.error_dialog("Erro Inesperado", f"Ocorreu um erro: {e}")
            if audio_file_path and os.path.exists(audio_file_path):
                os.remove(audio_file_path)
            self.convert_button.enabled = True


def main():
    return ConversordeTextoparaÁudio("Conversor de Texto para Áudio", "br.com.example.conversoraudio")
