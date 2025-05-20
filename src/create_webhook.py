import requests
import os
from dotenv import load_dotenv

load_dotenv()

subs_key = os.getenv("SUBSCRIPTION_KEY")
region = os.getenv("REGION")

# Endpoint da Azure para criacao do webhook
endpoint = f"https://{region}.api.cognitive.microsoft.com/speechtotext/v3.1/webhooks"

headers = {
    "Ocp-Apim-Subscription-Key": subs_key,
    "Content-Type": "application/json"
}

payload = {
    "displayName": "TranscriptionCompletionWebHook",
    "properties": {
        "secret": ""  # para validar a origem do POST recebido
    },
    "webUrl": "https://4985-2804-7f7-e03f-1be-2a4e-89c3-a8d1-11b3.ngrok-free.app/azure-transcricao-webhook",  # substitua pela URL real do seu webhook
    "events": {
        "transcriptionCompletion": True
    },
    "description": "Webhook para notificar transcrição finalizada"
}

response = requests.post(endpoint, headers=headers, json=payload)

print("Status:", response.status_code)
print("Resposta:", response.text)
