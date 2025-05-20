import azure.cognitiveservices.speech as speechsdk
from dotenv import load_dotenv
import os


load_dotenv()

# Substitua pelas suas credenciais
SPEECH_KEY = os.getenv("SUBSCRIPTION_KEY")
SERVICE_REGION = os.getenv("REGION")

speech_config = speechsdk.SpeechConfig(subscription=SPEECH_KEY, region=SERVICE_REGION)
speech_config.speech_recognition_language = "pt-BR"

audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

def recognizing(evt):
    print(f"(Parcial): {evt.result.text}", end="\r")

def recognized(evt):
    print(f"\n✔️ Final: {evt.result.text}")

def canceled(evt):
    print(f"\n[ERRO]: {evt.reason}")
    if evt.reason == speechsdk.CancellationReason.Error:
        print(f"Detalhes: {evt.error_details}")

# Conecta os eventos
speech_recognizer.recognizing.connect(recognizing)
speech_recognizer.recognized.connect(recognized)
speech_recognizer.canceled.connect(canceled)

# Inicia a transcrição contínua
print("🎙️ Fale algo (Ctrl+C para parar):")
speech_recognizer.start_continuous_recognition()

try:
    while True:
        pass
except KeyboardInterrupt:
    print("\nEncerrando...")
    speech_recognizer.stop_continuous_recognition()
