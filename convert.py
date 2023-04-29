import os
import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
from transformers import MBartForConditionalGeneration, MBart50TokenizerFast

try:
    model = MBartForConditionalGeneration.from_pretrained("facebook/mbart-large-50-many-to-many-mmt")
    tokenizer = MBart50TokenizerFast.from_pretrained("facebook/mbart-large-50-many-to-many-mmt")
except Exception as e:
    print("An error occurred:", str(e))


class SpeechRecognizer:
    def __init__(self):
        self.recognizer = sr.Recognizer()

    def record_audio(self, audio_file):
        with sr.AudioFile(audio_file) as source:
            audio = self.recognizer.record(source)
        return audio

    def recognize_google(self, audio, lang='en-US'):
        try:
            text = self.recognizer.recognize_google(audio, language=lang)
            print(text)
            return text
        except sr.UnknownValueError:
            print("Google could not understand audio")
        except sr.RequestError as e:
            print("Google error; {0}".format(e))

    def recognize_sphinx(self, audio, lang='en-US'):  # offline
        try:
            text = self.recognizer.recognize_sphinx(audio, language=lang)
            return text
        except sr.UnknownValueError:
            print("Sphinx could not understand audio")
        except sr.RequestError as e:
            print("Sphinx error; {0}".format(e))

    def recognize_wit(self, audio, lang='en-US'):
        try:
            text = self.recognizer.recognize_wit(audio, key="WIT_AI_KEY")
            print(text)
            return text
        except sr.UnknownValueError:
            print("Wit could not understand audio")
        except sr.RequestError as e:
            print("Wit error; {0}".format(e))


class Translate:
    def __init__(self):
        self.model = MBartForConditionalGeneration.from_pretrained("facebook/mbart-large-50-many-to-many-mmt")
        self.tokenizer = MBart50TokenizerFast.from_pretrained("facebook/mbart-large-50-many-to-many-mmt")

    def trans_mbart(self, lang, des):
        article = "{}".format(self)
        tokenizer.src_lang = "{}".format(lang)
        encoded_hi = tokenizer(article, return_tensors="pt")
        generated_tokens = model.generate(
            **encoded_hi,
            forced_bos_token_id=tokenizer.lang_code_to_id["{}".format(des)]
        )
        translations = tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)
        return translations

    def trans_google(self, lang, des):
        text = "{}".format(self)
        translator = Translator()
        translations = translator.translate(text, src="{}".format(lang), dest="{}".format(des))
        return translations.text


class TextToSpeech:
    def __init__(self):
        self.text = "{}".format(self)

    def tts_google(self, lang):
        tts = gTTS(text="{}".format(self), lang="{}".format(lang), slow=False)
        tts.save("{}.mp3".format(self))
        audio = os.system("{}.mp3".format(self))
        return audio

    def tts_mbart(self, lang, des):
        article = "{}".format(self)
        tokenizer.src_lang = "{}".format(lang)
        encoded = tokenizer(article, return_tensors="pt")
        generated_tokens = model.generate(
            **encoded,
            forced_bos_token_id=tokenizer.lang_code_to_id["{}".format(des)]
        )
        translations = tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)
        return translations
