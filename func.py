import requests
import json

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
    def __init__(self, baerer: str,version: float, phone_id: int): # Phone_id: 871508606049549 
        self.baerer = baerer
        self.version = f"v{version:.1f}"
        self.phone_id = phone_id
        self.url_base = f"https://graph.facebook.com/{self.version}/{self.phone_id}"
        
    def send_message(self,destiny: int, content_type: str, content: dict):
        print(self.url_base)
        json_data = json.dumps({"messaging_product": "whatsapp",    
                            "recipient_type": "individual",
                            "to": f"{destiny}",
                            "type": "text",
                            "text": {
                                "preview_url": False,
                                "body": content['body']
                             }
                        })
        response = requests.post(self.url_base+"/messages", headers={"Authorization": f"Bearer {self.baerer}", "Content-Type": "application/json", "Accept-Encoding": "gzip", "User-Agent": "Meta for Developers"}, 
                      data=json_data)
        return response