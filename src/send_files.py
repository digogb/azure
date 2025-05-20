from azure.storage.blob import BlobServiceClient, generate_blob_sas, BlobSasPermissions
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

# ===== CONFIGURAÇÕES =====
load_dotenv()

container_name = "audiotranscribe"
diretorio_local = "./videos"  # pasta onde estão os arquivos a enviar
conta_armazenamento = os.getenv("BLOB_ACCOUNT_NAME")  # mesmo valor do AccountName acima
chave_conta = os.getenv("BLOB_KEY")  # mesmo valor do AccountKey acima
connection_string = f"DefaultEndpointsProtocol=https;AccountName={conta_armazenamento};AccountKey={chave_conta};EndpointSuffix=core.windows.net"

# ===== CONECTA AO STORAGE =====
blob_service_client = BlobServiceClient.from_connection_string(connection_string)
container_client = blob_service_client.get_container_client(container_name)


def send_files():

    urls = []

    print("Enviando arquivo(s)...")

    # ===== ENVIA E GERA URL COM SAS =====
    for nome_arquivo in os.listdir(diretorio_local):
        caminho_arquivo = os.path.join(diretorio_local, nome_arquivo)

        if os.path.isfile(caminho_arquivo):
            print(f"Enviando: {nome_arquivo}...")
            blob_client = container_client.get_blob_client(blob=nome_arquivo)
            
            # Upload com sobrescrita
            with open(caminho_arquivo, "rb") as dados:
                blob_client.upload_blob(dados, overwrite=True)

            # Gera SAS válido por 1 hora
            sas_token = generate_blob_sas(
                account_name=conta_armazenamento,
                container_name=container_name,
                blob_name=nome_arquivo,
                account_key=chave_conta,
                permission=BlobSasPermissions(read=True),
                expiry=datetime.utcnow() + timedelta(hours=1)
            )

            url_com_sas = f"https://{conta_armazenamento}.blob.core.windows.net/{container_name}/{nome_arquivo}?{sas_token}"
            #print(f"Arquivo enviado com sucesso. URL com SAS (válida por 1h):\n{url_com_sas}\n")
            urls.append(url_com_sas)

        print(f"{nome_arquivo} enviado com sucesso.")    

    return urls
