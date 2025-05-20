import webrtcvad
from pydub import AudioSegment
import os

def aplicar_vad(entrada_wav, saida_wav, agressividade=2, janela_ms=30):
    # Carrega o áudio
    audio = AudioSegment.from_wav(entrada_wav).set_channels(1).set_frame_rate(16000)
    amostras = audio.raw_data
    taxa = audio.frame_rate
    bytes_por_frame = int(taxa * (janela_ms / 1000.0) * 2)  # 2 bytes por amostra

    # Inicializa o VAD
    vad = webrtcvad.Vad(agressividade)

    trechos_fala = AudioSegment.empty()
    for i in range(0, len(amostras), int(bytes_por_frame)):
        bloco = amostras[i:i + int(bytes_por_frame)]
        if len(bloco) < int(bytes_por_frame):
            continue
        if vad.is_speech(bloco, sample_rate=16000):
            inicio_ms = int(i / 2 / (taxa / 1000))
            fim_ms = inicio_ms + janela_ms
            trecho = audio[inicio_ms:fim_ms]
            trechos_fala += trecho

    # Salva o novo áudio sem silêncios
    trechos_fala.export(saida_wav, format="wav")
    print(f" Novo arquivo com fala exportado para: {saida_wav}")
