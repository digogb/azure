import os
import subprocess

diretorio_local = "./videos"  # pasta onde estão os arquivos a extrair
diretorio_final = "./audios_to_send"

def extrair_com_processo(arquivo, saida):

    comando = [
    "ffmpeg",
    "-i", arquivo,                      # arquivo de entrada
    "-ac", "1",                         # mono
    "-ar", "16000",                     # 16kHz
    "-y",                               # sobrescreve se já existir
    "-af", "silenceremove=1:0:-45dB",   # VAD (remoção de silêncios)
    saida                               # arquivo de saída
]

    return subprocess.run(comando, capture_output=True, text=True)

def extract_audio():

    for nome_arquivo in os.listdir(diretorio_local):
        
        nome_arquivo_sem_extensao, _ = nome_arquivo.split(".",1)

        caminho_arquivo = os.path.join(diretorio_local, nome_arquivo)
        arquivo_saida = f"{diretorio_final}/{nome_arquivo_sem_extensao}.wav"

        os.makedirs(diretorio_final,exist_ok=True)

        if os.path.isfile(caminho_arquivo):
            result = extrair_com_processo(caminho_arquivo, arquivo_saida)

            if result.returncode == 0:
                print("Extração feita com sucesso!")
            else:
                print(" Erro ao extrair áudio.")
                print("Stderr:", result.stderr)
        

#extract_audio()