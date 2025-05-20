import azure.cognitiveservices.speech as speechsdk
from dotenv import load_dotenv
import os

load_dotenv()

class AzureSpeechTranslator:
    def __init__(self, chave, regiao, idioma_origem='pt-BR', idioma_destino='en-US'):
        self.chave = chave
        self.regiao = regiao
        self.idioma_origem = idioma_origem
        self.idioma_destino = idioma_destino
        self.translator = self._configurar_translator()

    def _configurar_translator(self):
        translation_config = speechsdk.translation.SpeechTranslationConfig(
            subscription=self.chave,
            region=self.regiao
        )
        translation_config.speech_recognition_language = self.idioma_origem
        translation_config.add_target_language(self.idioma_destino)

        audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)

        return speechsdk.translation.TranslationRecognizer(
            translation_config=translation_config,
            audio_config=audio_config
        )

    def escutar_e_traduzir(self):
        print(f" Fale algo em '{self.idioma_origem}'... será traduzido para '{self.idioma_destino}'")
        resultado = self.translator.recognize_once()

        if resultado.reason == speechsdk.ResultReason.TranslatedSpeech:
            print(" Original:", resultado.text)
            print(" Tradução:", resultado.translations[self.idioma_destino])
        elif resultado.reason == speechsdk.ResultReason.RecognizedSpeech:
            print(" Fala reconhecida, mas não traduzida:", resultado.text)
        elif resultado.reason == speechsdk.ResultReason.NoMatch:
            print(" Nenhuma fala reconhecida.")
        elif resultado.reason == speechsdk.ResultReason.Canceled:
            cancel_details = resultado.cancellation_details
            print(" Cancelado:", cancel_details.reason)
            if cancel_details.reason == speechsdk.CancellationReason.Error:
                print("Erro:", cancel_details.error_details)

# --- USO ---
if __name__ == "__main__":
    CHAVE = os.getenv("SUBSCRIPTION_KEY")
    REGIAO = os.getenv("REGION")  # ex: brazilsouth

    tradutor = AzureSpeechTranslator(chave=CHAVE, regiao=REGIAO, idioma_origem='ko-KR', idioma_destino='pt-BR')
    tradutor.escutar_e_traduzir()
