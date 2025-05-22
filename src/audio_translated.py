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
        print(f"Fale algo em '{self.idioma_origem}'... será traduzido para '{self.idioma_destino}'")
        resultado = self.translator.recognize_once()

        if resultado.reason == speechsdk.ResultReason.TranslatedSpeech:
            texto_original = resultado.text
            traducao = resultado.translations[self.idioma_destino]
            print("Original:", texto_original)
            print("Tradução:", traducao)
            return traducao
        elif resultado.reason == speechsdk.ResultReason.RecognizedSpeech:
            print("Fala reconhecida, mas não traduzida:", resultado.text)
            return resultado.text
        elif resultado.reason == speechsdk.ResultReason.NoMatch:
            print("Nenhuma fala reconhecida.")
        elif resultado.reason == speechsdk.ResultReason.Canceled:
            cancel_details = resultado.cancellation_details
            print("Cancelado:", cancel_details.reason)
            if cancel_details.reason == speechsdk.CancellationReason.Error:
                print("Erro:", cancel_details.error_details)
        return None

class AzureTextToSpeech:
    def __init__(self, chave, regiao, voz='en-US-BrianMultilingualNeural'):
        self.chave = chave
        self.regiao = regiao
        self.voz = voz
        self.speech_config = self._configurar_speech()

    def _configurar_speech(self):
        speech_config = speechsdk.SpeechConfig(
            subscription=self.chave,
            region=self.regiao
        )
        speech_config.speech_synthesis_voice_name = self.voz
        return speech_config

    def sintetizar_para_arquivo(self, texto, arquivo_saida='output.wav'):
        audio_config = speechsdk.audio.AudioOutputConfig(filename=arquivo_saida)
        synthesizer = speechsdk.SpeechSynthesizer(
            speech_config=self.speech_config,
            audio_config=audio_config
        )
        resultado = synthesizer.speak_text_async(texto).get()

        if resultado.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            print(f"Áudio salvo com sucesso em '{arquivo_saida}'")
        elif resultado.reason == speechsdk.ResultReason.Canceled:
            cancel_details = resultado.cancellation_details
            print("Cancelado:", cancel_details.reason)
            if cancel_details.reason == speechsdk.CancellationReason.Error:
                print("Erro:", cancel_details.error_details)

class MainApp:
    def __init__(self):
        self.chave = os.getenv("SUBSCRIPTION_KEY")
        self.regiao = os.getenv("REGION")

        if not self.chave or not self.regiao:
            raise ValueError("SUBSCRIPTION_KEY e REGION devem ser configuradas no .env")

        self.translator = AzureSpeechTranslator(
            chave=self.chave,
            regiao=self.regiao,
            idioma_origem='pt-BR',
            idioma_destino='en-US'
        )
        self.tts = AzureTextToSpeech(
            chave=self.chave,
            regiao=self.regiao,
            voz='en-US-BrianMultilingualNeural'
        )

    def executar(self):
        texto_traduzido = self.translator.escutar_e_traduzir()
        if texto_traduzido:
            self.tts.sintetizar_para_arquivo(texto_traduzido)
        else:
            print("Nenhum texto para sintetizar.")

# --- USO ---
if __name__ == "__main__":
    app = MainApp()
    app.executar()
