import os
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request
from telegram import Bot

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    bot_token = os.getenv("telegram_bot_token")
    if not bot_token:
        raise RuntimeError("Falta configurar telegram_bot_token en .env")

    async with Bot(token=bot_token) as bot:
        app.state.bot = bot
        yield

app = FastAPI(lifespan=lifespan)

##Endpoint que consulta con un bot de telegram y devuelve la respuesta del bot
@app.get("/botGetME")
async def bot_get_me(request: Request):
    bot: Bot = request.app.state.bot
    user = await bot.get_me()
    return {"id": user.id, "username": user.username}

@app.post("/webhook")
async def webhook(request: Request):
    webhook_secret = os.getenv("TELEGRAM_WEBHOOK_SECRET")
    # Check if the secret token is present and matches the expected value
    if not webhook_secret:
        raise RuntimeError("Falta configurar TELEGRAM_WEBHOOK_SECRET en .env")
    if request.headers.get("X-Telegram-Bot-Api-Secret-Token") != webhook_secret:
       raise HTTPException(status_code=403, detail="Unauthorized")
    # Implement webhook logic here
    message = await request.json()
    # Process the incoming message and respond accordingly 
    if not message:
        return {"status": "No message received"}
    else:
        if message.get("message"):
            message_text = message["message"].get("text")
            #return {"status": "Message received", "message": message_text}
            if message_text:
                chat_id = message["message"]["chat"]["id"]
                if chat_id:
                    bot: Bot = request.app.state.bot
                    await bot.send_message(chat_id=chat_id, text=f"Received your message: {message_text} ; chat_id: {chat_id}")
                    #return {"status": "Message received", "message": message_text, "chat_id": chat_id}
                    ##return {"status": "Message received", "message": message_text}
            else:
                return {"status": "Message received but no text found"}
        else:
            return {"status": "Update received but no message found"}



##test de api
@app.get("/")
async def root():
   return {"message": "Hello World1"}