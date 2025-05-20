from fastapi import FastAPI, Request, Response

app = FastAPI()

@app.post("/azure-transcricao-webhook")
async def receber_webhook(request: Request):
    # Verifica se é uma requisição de verificação
    if "validationToken" in request.query_params:
        token = request.query_params["validationToken"]
        return Response(content=token, media_type="text/plain") 

    # Caso seja uma notificação real
    payload = await request.json()
    print("📨 Notificação recebida da Azure:", payload)
    return {"status": "ok"}

