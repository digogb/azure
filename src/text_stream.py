import os
import azure.cognitiveservices.speech as speechsdk
from dotenv import load_dotenv


load_dotenv()

# setup speech synthesizer
# IMPORTANTE: usar o endpoint websocket v2
speech_config = speechsdk.SpeechConfig(
    endpoint=f"wss://{os.getenv('REGION')}.tts.speech.microsoft.com/cognitiveservices/websocket/v2",
    subscription=os.getenv("SUBSCRIPTION_KEY")
)

# define uma voz
speech_config.speech_synthesis_voice_name = "pt-BR-FranciscaNeural"

# inicializa o sintetizador de fala
audio_config = speechsdk.audio.AudioOutputConfig(filename="output.wav")
speech_synthesizer = speechsdk.SpeechSynthesizer(
    speech_config=speech_config,
    audio_config=audio_config
)

# conecta o evento de sintetização para mostrar progresso
speech_synthesizer.synthesizing.connect(lambda evt: print("[audio]", end=""))

# configura timeouts para evitar cancelamento
speech_config.set_property(speechsdk.PropertyId.SpeechSynthesis_FrameTimeoutInterval, "100000000")
speech_config.set_property(speechsdk.PropertyId.SpeechSynthesis_RtfTimeoutThreshold, "10")

# cria a requisição com input do tipo TextStream
tts_request = speechsdk.SpeechSynthesisRequest(
    input_type=speechsdk.SpeechSynthesisRequestInputType.TextStream
)

# inicia a tarefa de síntese
tts_task = speech_synthesizer.speak_async(tts_request)

# TEXTO FIXO a ser falado
fixed_text = "Hello, welcome to the Azure Speech Service demonstration. This is a fixed message."

# escreve o texto fixo no input stream
tts_request.input_stream.write(fixed_text)

print("[TTS Input Complete]", end="")

# fecha o input stream
tts_request.input_stream.close()

# aguarda a síntese terminar
result = tts_task.get()
print("[TTS END]", end="")
