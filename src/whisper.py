from faster_whisper import WhisperModel

model = WhisperModel("base", device="cpu")

print("Iniciando transcrição do whisper...")
segments, info = model.transcribe("./extracao/videos_vocals.wav")

# Caminho do arquivo de saída
saida_txt = "diarizacao_whisper.txt"

# Grava no .txt
with open(saida_txt, "w", encoding="utf-8") as f:
    for seg in segments:
        linha = f"[{seg.start:.2f}s - {seg.end:.2f}s] {seg.text}\n"
        f.write(linha)

print(f"Arquivo salvo em: {saida_txt}")
