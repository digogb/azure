import re
import json

# 1. Carrega words da Azure
with open("./done/File 1.json", "r", encoding="utf-8") as f:
    azure = json.load(f)

azure_words = []
for frase in azure["recognizedPhrases"]:
    azure_words.extend(frase["nBest"][0].get("words", []))

# 2. Carrega os segmentos do Whisper (já salvos em um .txt)
segmentos = []
with open("./done/diarizacao_whisper.txt", "r", encoding="utf-8") as f:
    for linha in f:
        match = re.match(r"\[(\d+\.\d+)s\s*-\s*(\d+\.\d+)s\]\s*(.*)", linha.strip())
        if match:
            start = float(match.group(1))
            end = float(match.group(2))
            text = match.group(3)
            segmentos.append({"start": start, "end": end, "texto_whisper": text})

# 3. Atribui palavras da Azure a cada segmento
saida = []
for seg in segmentos:
    palavras = [
        w["word"] for w in azure_words
        if seg["start"] * 1000 <= w["offsetMilliseconds"] < seg["end"] * 1000
    ]
    saida.append({
        "start": seg["start"],
        "end": seg["end"],
        "texto": " ".join(palavras)
    })

# 4. Salva resultado final
with open("./done/resultado_hibrido.txt", "w", encoding="utf-8") as f:
    for bloco in saida:
        f.write(f"[{bloco['start']:.2f}s - {bloco['end']:.2f}s] {bloco['texto']}\n")
