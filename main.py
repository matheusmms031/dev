from flask import Flask, request, jsonify

app = Flask(__name__)

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

                                print(f"\n📞 Mensagem de: {from_number}")
                                print(f"📝 Conteúdo: {text_content}")
                                print("--- FIM DA MENSAGEM ---")
                            
                            # Se for outro tipo (imagem, vídeo, etc.), você pode expandir aqui
                            elif message.get("type") == "image":
                                print(f"🖼️ Recebida uma Imagem de: {message.get('from')}")
                                
        except Exception as e:
            print(f"Erro ao processar mensagem: {e}")
            
        return jsonify({"status": "ok"}), 200 # Resposta obrigatória

if __name__ == "__main__":
    # Rodar o servidor Flask
    app.run(port=5000, debug=True)