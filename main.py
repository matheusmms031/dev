from flask import Flask, request, jsonify
from func import Aplication
from func import APIMETA
import requests


apimeta = APIMETA(baerer="EAASXZBNoNhB4BQDTqrZCpfaQvUMBRutURPnwRFuZAUqwsx3cuoYKX1XboyUnINtPq1ZB4aQoZAg8OlSVqs8nsJfVfvWtS6F10L2TdJ6oMWA0FXKRZAEUAvE3TtpQvxABeBH2OgCSBM8HvjZAr6BE8HTDy2fSydU10xpZAoerSJONDkxdNeBvvU2N79ft1FwXlAZB4wSWaHM0GwnxmoKJ6dpZCW9xp2gzmZBCypo2i2ImsIP5ZCrYw8SGfFQjBvPDOZAXus7OyfBOABguGYcrrqZBiI0110vZA3ecU6fBjal5QSPNAZDZD", version=24.0, phone_id=871508606049549)
app = Flask(__name__)

BAERER_TOKEN = "EAASXZBNoNhB4BQDTqrZCpfaQvUMBRutURPnwRFuZAUqwsx3cuoYKX1XboyUnINtPq1ZB4aQoZAg8OlSVqs8nsJfVfvWtS6F10L2TdJ6oMWA0FXKRZAEUAvE3TtpQvxABeBH2OgCSBM8HvjZAr6BE8HTDy2fSydU10xpZAoerSJONDkxdNeBvvU2N79ft1FwXlAZB4wSWaHM0GwnxmoKJ6dpZCW9xp2gzmZBCypo2i2ImsIP5ZCrYw8SGfFQjBvPDOZAXus7OyfBOABguGYcrrqZBiI0110vZA3ecU6fBjal5QSPNAZDZD"

# --- Configure estas variáveis ---
VERIFY_TOKEN = "tokenReste234512234" # Use o mesmo token que você configurar na Meta
# ---------------------------------

# Esta rota recebe todos os eventos do WhatsApp
@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    # 1. ETAPA DE VERIFICAÇÃO (GET)
    if request.method == "GET":
        # Recebe os parâmetros enviados pela Meta
        mode = request.args.get("hub.mode")
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")

        # Verifica se o modo é 'subscribe' e se o token é o correto
        if mode == "subscribe" and token == VERIFY_TOKEN:
            print(f"✅ Webhook Verificado! Token: {token}")
            # Retorna o 'challenge' para confirmar a verificação
            return challenge, 200
        else:
            # Token não corresponde ou modo incorreto
            print("❌ Falha na Verificação.")
            return jsonify({"status": "error"}), 403

    # 2. ETAPA DE NOTIFICAÇÃO (POST)
    elif request.method == "POST":
        data = request.json
        print("\n--- NOVO PAYLOAD RECEBIDO ---")
        print(data) # Imprime o JSON bruto para depuração

        try:
            # Percorre o objeto para chegar ao conteúdo da mensagem
            # O objeto JSON é complexo, com vários níveis (entry -> changes -> value -> messages)

            # Extração simplificada da mensagem de texto
            for entry in data.get("entry", []):
                for change in entry.get("changes", []):
                    value = change.get("value", {})
                    if value.get("messages"):
                        for message in value.get("messages", []):
                            # Filtra apenas por mensagens de texto (text)
                            if message.get("type") == "text":
                                phone_id = value.get("metadata", {}).get("phone_number_id")
                                from_number = message.get("from")
                                text_content = message.get("text", {}).get("body")
                                if text_content == "acessar painel":
                                    print(from_number)
                                    response = apimeta.send_message(destiny=int(from_number), content_type="text", content={"body": "Opa"})
                                    print(response.json())
                            # Se for outro tipo (imagem, vídeo, etc.), você pode expandir aqui
                            elif message.get("type") == "image":
                                print(f"🖼️ Recebida uma Imagem de: {message.get('from')}")
                                
        except Exception as e:
            print(f"Erro ao processar mensagem: {e}")
            
        return jsonify({"status": "ok"}), 200 # Resposta obrigatória

if __name__ == "__main__":
    # Rodar o servidor Flask
    app.run(port=5000, debug=True)