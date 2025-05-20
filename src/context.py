class ContextProcess:
    def __init__(self):
        self.data = {}

    def init_file(self, file_name):
        if file_name not in self.data:
            self.data[file_name] = {
                "status_url": "",
                "status": "",
                "duration": "",
            }

    def update(self, file_name, field, value):
        if file_name in self.data:
            self.data[file_name][field] = value
        else:
            raise KeyError(f"Arquivo {file_name} não encontrado no contexto")    

    def get(self, file_name, field):
        return self.data.get(file_name, {}).get(field)
    
    def get_all(self):
        return self.data
    

