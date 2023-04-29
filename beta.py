from flask import Flask, request, render_template, send_file
from googletrans import Translator
import gtts
import os
import speech_recognition as rec
import subprocess

app = Flask(__name__, template_folder="templates")

r = rec.Recognizer()
mic = rec.Microphone()
a = ""
translator = Translator(service_urls=['translate.google.com'], user_agent='Mozilla/5.0')


def record():
    audio = request.files['audio']
    audio.save('audio.mp3')
    subprocess.call(['ffmpeg', '-i', 'audio.mp3',
                     'audio.wav'])
    os.remove("audio.mp3")
    audio = "audio.wav"
    print(audio)
    return audio


def translate(self, lang):
    translator = Translator()
    result = translator.translate(text, dest=lang)
    return result.text


def recognize(audio):
    try:
        with rec.AudioFile(audio) as source:
            audio_data = r.record(source)
            text = r.recognize_google(audio_data, language=a)
            print(f"You said: {text}")
            return text

    except rec.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
        return "Error: Could not understand audio. Please try again."

    except rec.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
        return f"Error: Could not request results from Google Speech Recognition service; {e}"


@app.route('/', methods=['GET', 'POST'])
def main():
    global a
    if request.method == 'POST':
        a = request.form['language']
        text = recognize(record())
        out_lang = request.form['translate_to']

        if text.startswith("Error"):
            return render_template('index.html', error=text)

        translated = translate(text, out_lang)
        print(f"Translated self: {translated}")
        os.remove("audio.wav")
        return render_template('index.html', translated_text=translated, text=text)
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
