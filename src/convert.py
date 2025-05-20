import json
from pathlib import Path

class convert_transcription:
    def __init__(self, caminho_json):
        self.caminho_json = Path(caminho_json)

    def carregar_dados(self):
        if not self.caminho_json.exists():
            raise FileNotFoundError(f"Arquivo não encontrado: {self.caminho_json.resolve()}")
        with open(self.caminho_json, 'r', encoding='utf-8') as f:
            return json.load(f)

    def gerar_segmentos(self):
        dados = self.carregar_dados()
        frases = dados.get("recognizedPhrases", [])
        segmentos = []

        for entrada in frases:
            if "nBest" not in entrada or not entrada["nBest"]:
                continue

            melhor = entrada["nBest"][0]
            texto = melhor.get("lexical", "").strip()
            speaker = f"SPEAKER_{str(entrada.get('speaker', 0)).zfill(2)}"
            start_time = int(entrada.get("offsetMilliseconds", 0))
            end_time = start_time + int(entrada.get("durationMilliseconds", 0))

            segmentos.append({
                "speaker": speaker,
                "start_time": start_time,
                "end_time": end_time,
                "text": texto
            })

        return segmentos

    def salvar_json(self, caminho_saida):
        segmentos = self.gerar_segmentos()
        with open(caminho_saida, 'w', encoding='utf-8') as f:
            json.dump(segmentos, f, ensure_ascii=False, indent=3)



caminho_entrada = "resultados/podcast1.json"
caminho_saida = "converted/segmentos_formatados.json"

extrator = SegmentadorDiarizado(caminho_entrada)
extrator.salvar_json(caminho_saida)