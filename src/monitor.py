import requests
import json

from dotenv import load_dotenv

import os

load_dotenv()

subs_key = os.getenv("SUBSCRIPTION_KEY")

def status(status_url):

    headers = {
        "Ocp-Apim-Subscription-Key": subs_key
    }

    # Diagnóstico da resposta
    #print("Consultando status...")

    response = requests.get(status_url, headers=headers)

    #print(f"HTTP status code: {response.status_code}")

    try:
        data = response.json()
        
        
        return data
        #print("Conteúdo da resposta JSON:")
        #print(json.dumps(data, indent=2))
        

        #if "status" in data:
        #    print(f"Status atual da transcrição: {data['status']}")
        #else:
        #    print("A resposta não contém o campo 'status'. Verifique o conteúdo acima.")
    except Exception as e:
        print("Erro ao decodificar JSON:", e)
        print("Conteúdo da resposta bruta:")
        print(response.text)



#status("https://brazilsouth.api.cognitive.microsoft.com/speechtotext/v3.0/transcriptions/2253d715-704d-4b40-a089-d240e2148f28/files")


data = status("https://brazilsouth.api.cognitive.microsoft.com/speechtotext/v3.2/transcriptions/3fd7dd98-1022-4512-af90-feef0b124601")
print(data)