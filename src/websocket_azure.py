import websocket
import threading
import uuid
import wave
import json
import time
from dotenv import load_dotenv
import os

load_dotenv()

SPEECH_KEY = os.getenv("SUBSCRIPTION_KEY")
SERVICE_REGION = os.getenv("REGION")
LANGUAGE = 'pt-BR'
AUDIO_FILE = './audios_to_send/abandono.wav'  # WAV PCM 16kHz Mono

CONNECTION_ID = str(uuid.uuid4())
URL = f"wss://{SERVICE_REGION}.stt.speech.microsoft.com/speech/recognition/conversation/cognitiveservices/v1?language={LANGUAGE}"

HEADERS = {
    'Ocp-Apim-Subscription-Key': SPEECH_KEY,
    'X-ConnectionId': CONNECTION_ID,
}

def on_open(ws):
    def run(*args):
        with open(AUDIO_FILE, 'rb') as f:
            f.read(44)  # pula o cabeçalho WAV
            chunk = 4096
            while True:
                data = f.read(chunk)
                if not data:
                    break
                ws.send(data, opcode=websocket.ABNF.OPCODE_BINARY)
                time.sleep(0.1)
        time.sleep(1)
        ws.close()
    threading.Thread(target=run).start()

def on_message(ws, message):
    try:
        msg = json.loads(message)
        if 'DisplayText' in msg:
            print("Transcrição:", msg['DisplayText'])
    except:
        pass

def on_error(ws, error):
    print("Erro:", error)

def on_close(ws, code, msg):
    print(f"[WebSocket encerrado] Código: {code} | Motivo: {msg}")

websocket.enableTrace(False)
ws = websocket.WebSocketApp(URL,
                            header=[f"Ocp-Apim-Subscription-Key: {SPEECH_KEY}",
                                    f"X-ConnectionId: {CONNECTION_ID}"],
                            on_open=on_open,
                            on_message=on_message,
                            on_error=on_error,
                            on_close=on_close)

ws.run_forever()
