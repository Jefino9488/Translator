from flask import Flask, request, render_template, send_file
import convert
import websocket

app = Flask(__name__, template_folder="templates")


# def main():
#     recognizer = convert.SpeechRecognizer()
#     audio = input("Enter audio file: ")
#     audio = "{}".format(audio)
#     try:
#         text = recognizer.recognize_sphinx(recognizer.record_audio(audio))
#         print(text)
#         audio = input("Enter audio file: ")
#         audio = "{}".format(audio)
#         text = recognizer.recognize_sphinx(recognizer.record_audio(audio))
#         return text
#     except Exception as e:
#         print("An error occurred:", str(e))
#         audio = input("Enter audio file: ")
#         audio = "{}".format(audio)
#         text = recognizer.recognize_sphinx(recognizer.record_audio(audio))
#         return text

@app.route('/', methods=['GET', 'POST'])
def main():
    recognizer = convert.SpeechRecognizer()
    if request.method == 'POST':
        from_lang = request.form['language']
        to_lang = request.form['translate_to']
        audio = request.files['audio']
        audio.save('audio.mp3')
        audio = "audio.mp3"
        try:
            text = recognizer.recognize_google(recognizer.record_audio(audio), from_lang)
            tran = convert.Translate()
            print(text)
            tran_text = tran.trans_google(text, to_lang)
            return render_template('index_beta.html', text=text, tran_text=tran_text)
        except Exception as e:
            print("An error occurred:", str(e))
            return render_template('index_beta.html', error=str(e))
    else:
        return render_template('index_beta.html')


if __name__ == '__main__':
    app.run(debug=True)
