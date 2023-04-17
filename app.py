from flask import Flask, request, render_template
from googletrans import Translator
import gtts
from playsound import playsound
import os
import speech_recognition as rec

app = Flask(__name__, template_folder="templates")

r = rec.Recognizer()
mic = rec.Microphone()
a = ""


def say(text):
    text = gtts.gTTS(text)
    text.save("output.mp3")
    playsound("output.mp3")
    os.remove("output.mp3")


def translate(text, lang):
    translator = Translator()
    result = translator.translate(text, dest=lang)
    return result.text


def listen():
    with mic as source:
        print("Speak in {}:".format(a))
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
    return audio


def recognize(audio):
    try:
        text = r.recognize_google(audio, language=a)
        print(f"You said: {text}")
        return text

    except rec.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
        say("Sorry, I could not understand what you said. Please try again.")
        return "Error: Could not understand audio. Please try again."

    except rec.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
        say("Sorry, an error occurred. Please try again.")
        return f"Error: Could not request results from Google Speech Recognition service; {e}"


@app.route('/', methods=['GET', 'POST'])
def main():
    global a
    if request.method == 'POST':
        a = request.form['language']
        text = str(recognize(listen()))
        out_lang = request.form['translate_to']

        if text.startswith("Error"):
            return render_template('index.html', error=text)

        translated = translate(text, out_lang)
        print(f"Translated text: {translated}")
        say(translated)
        return render_template('index.html', translated_text=translated, text=text)
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
