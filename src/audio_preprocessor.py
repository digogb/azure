import os
import shutil
import subprocess
from pathlib import Path
from context import ContextProcess

diretorio_local = "./videos"  # pasta onde estão os arquivos a extrair

class AudioPreprocessor:
    def __init__(self, demucs_model="htdemucs", output_dir="vocals_only"):
        self.demucs_model = demucs_model
        self.output_dir = Path(output_dir)

    def process(self, context: ContextProcess) -> str:
        input_path = Path(diretorio_local)

        if not input_path.exists():
            raise FileNotFoundError(f"Pasta não encontrada: {input_path}")

        for nome_arquivo in os.listdir(input_path):

            context.init_file(nome_arquivo)

            filepath = os.path.join(diretorio_local, nome_arquivo)

            # Executa demucs com dois stems: vocals e accompaniment
            comando = [
                "demucs",
                "--two-stems", "vocals",  # 👈 separa apenas vocals/accompaniment
                "-n", self.demucs_model,
                str(filepath)
            ]

            print(f"Rodando Demucs em: {filepath}")
            resultado = subprocess.run(comando, capture_output=True, text=True)

            if resultado.returncode != 0:
                print(" Erro ao rodar Demucs:")
                print(resultado.stderr)
                raise RuntimeError("Falha ao executar Demucs.")

            # Caminho para o vocals.wav gerado
            nome_sem_extensao, _ = nome_arquivo.split(".")

            vocals_path = (
                Path("separated") /
                self.demucs_model /
                nome_sem_extensao /
                "vocals.wav"
            )

            if not vocals_path.exists():
                raise FileNotFoundError("Arquivo vocals.wav não encontrado após separação.")

            # Move o vocals.wav para a pasta de saída simplificada
            final_path =  f"./extracao/{input_path.stem}_vocals.wav"
            shutil.move(str(vocals_path), final_path)

            print(f" Voz separada: {final_path}")
            return str(final_path)


