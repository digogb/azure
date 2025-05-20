import json

PATH = "./done"

def transform_file(file_name):

    # Abre o JSON gerado pela Azure com diarização
    with open(f"{PATH}/{file_name}.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    # Lista para armazenar frases formatadas
    frases = []

    if "recognizedPhrases" in data:
        for frase in data["recognizedPhrases"]:
            speaker = frase.get("speaker", "Desconhecido")
            texto = frase.get("nBest", [{}])[0].get("display", "").strip()

            if texto:
                frases.append(f"[Locutor {speaker}] {texto}")

    # Salva as frases em um arquivo .txt
    with open(f"{PATH}/{file_name}.txt", "w", encoding="utf-8") as out:
        out.write("\n\n".join(frases))

    print(f"Transcrição com locutores salva como '{file_name}.txt'")
