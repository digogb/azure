from rebuild import reconstruir_falas
import json

with open("./done/File 1.json", "r", encoding="utf-8") as f:
    dados = json.load(f)

falas = reconstruir_falas(dados["recognizedPhrases"])

# Caminho do arquivo de saída
saida_txt = "./done/falas_reconstruidas.txt"

# Grava no .txt
with open(saida_txt, "w", encoding="utf-8") as f:
    for fala in falas:
        linha = f"[{fala['inicio']/1000:.2f}s - {fala['fim']/1000:.2f}s] Speaker {fala['speaker']}: {fala['texto']}\n"
        f.write(linha)

print(f"Arquivo salvo em: {saida_txt}")
