from extract_audio import extract_audio
from audio_preprocessor import AudioPreprocessor
from send_files import send_files
from transcript import transcript
from monitor import status
from download import download
from transform import transform_file
from datetime import datetime
from context import ContextProcess

import time

# criando contexto
context_process = ContextProcess()

# aplicando demucs para separar canal de voz
data_inicio = datetime.now()
print(f"iniciando o transcrição em: {datetime.now()}")
#pre = AudioPreprocessor()
#pre.process(context_process)

# entraindo o audio em MONO
extract_audio()  

#print(context_process.get_all())

urls = send_files()

status_controller = []

try:
    for url in urls:
        data_inicio_azure = datetime.now()
        print(f"iniciando a transcrição em: {datetime.now()}")
        status_url = transcript(url)
        status_controller.append(status_url)

    for iterator, status_url in enumerate(status_controller):

        status_item = 'Running'

        while status_item == 'Running':
            data_status = status(status_url)
            status_item = data_status ['status'] if 'status' in data_status else ''
            file = data_status['links']['files'] if 'links' in data_status else ''
            print(f" Process {iterator+1} is/was {status_item}...")
            time.sleep(10)

        if status_item == 'Succeeded':
            file_name = f"File {iterator+1}"
            download(file, file_name)
            transform_file(file_name)
        elif status_item == 'Failed':
            #print(json.dumps(data_status, indent=2))     
            print(f"Erro na transcricao do process {iterator+1} : {data_status['properties']['error']['code']} - {data_status['properties']['error']['message']}")

        data_fim = datetime.now()
        print(f"finalizando a transcrição em: {datetime.now()}")    

        print(f"Duração Total: {data_fim - data_inicio}")    
        print(f"Duração Azure: {data_fim - data_inicio_azure}")    

          
except Exception as e:
    print(e)






