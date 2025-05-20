import docx
from sentence_transformers import SentenceTransformer, util
import numpy as np
import os

def extrair_texto_docx(caminho):
    doc = docx.Document(caminho)
    return "\n".join(p.text for p in doc.paragraphs if p.text.strip())

def dividir_em_blocos(texto, tamanho_minimo=30):
    return [linha.strip() for linha in texto.split('\n') if len(linha.strip()) > tamanho_minimo]

def comparar_transcricoes(arquivo1, arquivo2):
    texto1 = extrair_texto_docx(arquivo1)
    texto2 = extrair_texto_docx(arquivo2)

    blocos1 = dividir_em_blocos(texto1)
    blocos2 = dividir_em_blocos(texto2)

    modelo = SentenceTransformer('all-MiniLM-L6-v2')
    emb1 = modelo.encode(blocos1, convert_to_tensor=True)
    emb2 = modelo.encode(blocos2, convert_to_tensor=True)

    similaridades = []
    for emb in emb1:
        score = util.cos_sim(emb, emb2).max().item()
        similaridades.append(score)

    media = np.mean(similaridades)
    print(f"\nSimilaridade média entre as transcrições: {media:.4f}")
    return media

# Use os nomes dos seus arquivos aqui:

if __name__ == "__main__":
    pasta = "./comparacoes"  # Caminho relativo da pasta onde estão os DOCX

    print("\n Arquivos encontrados na pasta:")
    for f in os.listdir(pasta):
        print("  -", f)

    # Altere os nomes conforme necessário
    arq1 = os.path.join(pasta, "reuniao_cgti_talia.docx")
    arq2 = os.path.join(pasta, "reuniao_cgti_azure.docx")

    comparar_transcricoes(arq1, arq2)