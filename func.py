class Aplication():
    def __init__(self,name: str,email: str,console: str, phone_id: int) -> object:
        self.psalternatives = ["ps4","ps5","PS4","PS5"]
        self.name = name
        self.email = email
        self.phone_id = phone_id
        if console in self.psalternatives:
            self.console = console
            return [200]
        else:
            return [500,"Erro ao cadastrar seu console, por favor tente novamente com os seguintes nomes: 'ps4', 'ps5', 'PS4' ou 'PS5'"]
        

class APIMETA():
    def __init__(self, baerer: str,version: float):
        self.baerer = baerer
        self.version = f"v{version:.1f}"
        
   