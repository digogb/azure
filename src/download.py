import requests
from dotenv import load_dotenv

import os

load_dotenv()

subs_key = os.getenv("SUBSCRIPTION_KEY")

headers = {
    "Ocp-Apim-Subscription-Key": subs_key
}
def download(file_url, name):

    # Obtém a lista de arquivos de resultado
    r = requests.get(file_url, headers=headers)
    files_data = r.json()

    # Procura pelo tipo Transcription

    os.makedirs("./done",exist_ok=True)
    for f in files_data["values"]:
        if f["kind"] == "Transcription":
            download_url = f["links"]["contentUrl"]
            response = requests.get(download_url)
            with open(f"./done/{name}.json", "w", encoding="utf-8") as out_file:
                out_file.write(response.text)
            print(f"Transcrição salva como {name}.json")
            break
    else:
        print(" Arquivo de transcrição não encontrado.")


download("https://brazilsouth.api.cognitive.microsoft.com/speechtotext/v3.2/transcriptions/3fd7dd98-1022-4512-af90-feef0b124601/files","teste")