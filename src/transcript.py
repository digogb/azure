import requests
from dotenv import load_dotenv
import os

load_dotenv()

subs_key = os.getenv("SUBSCRIPTION_KEY")
region = os.getenv("REGION")


def transcript(audio_url):

    # Endpoint da Azure para transcrição em lote
    endpoint = f"https://{region}.api.cognitive.microsoft.com/speechtotext/v3.2/transcriptions"

    headers = {
        "Ocp-Apim-Subscription-Key": subs_key,
        "Content-Type": "application/json"
    }

    # Corpo da requisição com URL do áudio (pode adicionar mais de 1)
    payload = {
        "contentUrls": [audio_url],
        "locale": "pt-BR",  # Idioma do áudio
        "displayName": "Transcricao de Audio",
        "callbackUrl": "https://4a49-189-90-162-253.ngrok-free.app/azure-transcricao-webhook",
        "properties": {
            "diarizationEnabled": True,
            "wordLevelTimestampsEnabled": True,
            "punctuationMode": "DictatedAndAutomatic",
            "profanityFilterMode": "Masked",
            "displayFormWordLevelTimestampsEnabled": True,
            "diarization": {
                "speakers": {
                    "minCount": 1,
                    "maxCount": 25
                }
            }
        },
        
    }

    # Envia a requisição   
    response = requests.post(endpoint, headers=headers, json=payload)
    

    transcription_url = ""

    print(response.text)

    if response.status_code == 201:
        transcription_url = response.headers["Location"]
        print("Transcrição criada com sucesso!")
        print("Use esta URL para acompanhar o status da transcrição:")
        print(transcription_url)
    else:
        print("Erro ao criar transcrição:")
        print(response.status_code, response.text)
    
    return transcription_url
