from flask import Flask, request, send_file, render_template
from gtts import gTTS
import io

app = Flask(__name__, template_folder='templates')

@app.route('/')
def index():
    """Serves the main HTML page."""
    return render_template('index.html')

@app.route('/api/tts', methods=['POST'])
def tts():
    """
    Handles the text-to-speech conversion.
    Receives text in a JSON payload, converts it to speech using gTTS,
    and returns the audio as an MP3 file.
    """
    data = request.get_json()
    text_to_speak = data.get('text', '')

    if not text_to_speak:
        return "No text provided", 400

    try:
        # Generate the speech using gTTS
        tts = gTTS(text=text_to_speak, lang='pt', slow=False)

        # Save the speech to a temporary in-memory file
        mp3_fp = io.BytesIO()
        tts.write_to_fp(mp3_fp)
        mp3_fp.seek(0) # Rewind the file pointer to the beginning

        return send_file(
            mp3_fp,
            mimetype='audio/mpeg',
            as_attachment=False,
            download_name='speech.mp3'
        )
    except Exception as e:
        print(f"Error generating speech: {e}")
        return "Error generating speech", 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)