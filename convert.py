import os
import speech_recognition as sr
import whisper
from googletrans import Translator
from gtts import gTTS
from transformers import MBartForConditionalGeneration, MBart50TokenizerFast, AutoTokenizer, \
    AutoModelForSeq2SeqLM

model = MBartForConditionalGeneration.from_pretrained("facebook/mbart-large-50-many-to-many-mmt")
tokenizer = MBart50TokenizerFast.from_pretrained("facebook/mbart-large-50-many-to-many-mmt")


class SpeechRecognizer:
    def __init__(self):
        self.recognizer = sr.Recognizer()

    def record_audio(self):
        with sr.AudioFile(self) as source:
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

    def recognize_sphinx(self, audio, lang='en-US'):
        try:
            text = self.recognizer.recognize_sphinx(audio, language=lang)
            print(text)
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

    @staticmethod
    def recognize_whisper(self, audio, lang='en-US'):
        try:
            model = whisper.load_model("base")
            result = model.transcribe("audio.mp3", lang=lang)
            print(result["text"])
            return result["text"]
        except sr.UnknownValueError:
            print("Whisper could not understand audio")
        except sr.RequestError as e:
            print("Whisper error; {0}".format(e))


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
        os.system("{}.mp3".format(self))

    def tts_mbart(self, lang):
        model_name = "t5-base"
        token = AutoTokenizer.from_pretrained(model_name)
        mode = AutoModelForSeq2SeqLM.from_pretrained(model_name)
        text = "{}".format(self)
        input_ids = token.encode(text, return_tensors="pt")
        outputs = mode.generate(input_ids=input_ids, num_beams=5, early_stopping=True, max_new_tokens=100)
        return outputs
