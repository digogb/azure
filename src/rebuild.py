import json

def reconstruir_falas(recognizedPhrases, pausa_max=1000):
    falas = []
    for frase in recognizedPhrases:
        speaker = frase.get("speaker", "desconhecido")
        words = frase["nBest"][0].get("words", [])
        if not words:
            continue

        bloco = []
        ultima_fim = None
        for word in words:
            inicio = word["offsetMilliseconds"]
            fim = inicio + word["durationMilliseconds"]

            if ultima_fim is not None and (inicio - ultima_fim) > pausa_max:
                # Quebra de fala
                falas.append({
                    "speaker": speaker,
                    "texto": " ".join([w["word"] for w in bloco]),
                    "inicio": bloco[0]["offsetMilliseconds"],
                    "fim": bloco[-1]["offsetMilliseconds"] + bloco[-1]["durationMilliseconds"]
                })
                bloco = []

            bloco.append(word)
            ultima_fim = fim

        if bloco:
            falas.append({
                "speaker": speaker,
                "texto": " ".join([w["word"] for w in bloco]),
                "inicio": bloco[0]["offsetMilliseconds"],
                "fim": bloco[-1]["offsetMilliseconds"] + bloco[-1]["durationMilliseconds"]
            })

    return falas
