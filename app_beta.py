from flask import Flask, request, render_template, send_file
import os

from playsound import playsound

import convert
import speech_recognition as rec
from gtts import gTTS

rec = rec.Recognizer()

app = Flask(__name__, template_folder="templates")


@app.route('/', methods=['GET', 'POST'])
def main():
    speech = convert.SpeechRecognizer()
    tran = convert
    if request.method == 'POST':
        user_audio = request.form['audio']
        user_text = request.form['text']
        input_lang = request.form['translate_from']
        output_lang = request.form['translate_to']
        select_model = request.form['select_model']
        tts_model = request.form['tts_model']
        user_input = user_audio or user_text
        while user_input != "bye":
            try:
                if user_audio:
                    text = speech.recognize_sphinx(speech.record_audio(user_audio)) or speech.recognize_google(
                        speech.record_audio(user_audio))
                else:
                    text = user_text
                if select_model == "1":
                    result = tran.trans_google(text, input_lang, output_lang)
                    if tts_model == "1":
                        tran.say(result, output_lang)
                else:
                    result = tran.trans_mbart(text, input_lang, output_lang)
                print(result)

                user_audio = request.form['audio']
                user_text = request.form['text']
                user_input = user_audio or user_text
                input_lang = request.form['translate_from']
                output_lang = request.form['translate_to']
                select_model = request.form['select_model']
            except Exception as e:
                print("An error occurred:", str(e))
                user_audio = request.form['audio']
                user_text = request.form['text']
                user_input = user_audio or user_text
                input_lang = request.form['translate_from']
                output_lang = request.form['translate_to']
                select_model = request.form['select_model']

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)


def say(text):
    text = gTTS(text)
    text.save("output.mp3")
    playsound("output.mp3")
    os.remove("output.mp3")


def main():
    input_lang = "en"
    output_lang = "vi"

    global rec
    rec = rec.Recognizer()
    mic = rec.Microphone()
    a = input_lang
    with mic as source:
        print("Speak in {}:".format(a))
        rec.adjust_for_ambient_noise(source)
        audio = rec.listen(source)
    try:
        text = rec.recognize_google(audio, language=a)
        print(f"You said: {text}")


    except rec.UnknownValueError:
        print("Google Speech Recognition could not understand audio")

    else:
        try:
            con = convert.SpeechRecognizer()
            tran = convert.Translate()
            text = con.recognize_sphinx(con.record_audio(audio)) or con.recognize_google(con.record_audio(audio))
            print("You said :", text)
            text = tran.translate(text, 'en')
            print(text)
        except:
            print("i didn't get that")
