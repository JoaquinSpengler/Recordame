import os
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from telegram import Bot
from app.channels.telegram import parse_telegram_message, validate_webhook_secret

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    bot_token = os.getenv("telegram_bot_token")
    if not bot_token:
        raise RuntimeError("Falta configurar telegram_bot_token en .env")

    webhook_secret = os.getenv("TELEGRAM_WEBHOOK_SECRET")
    if not webhook_secret:
        raise RuntimeError("Falta configurar TELEGRAM_WEBHOOK_SECRET en .env")

    async with Bot(token=bot_token) as bot:
        app.state.bot = bot
        app.state.webhook_secret = webhook_secret
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
    validate_webhook_secret(
        request.headers.get("X-Telegram-Bot-Api-Secret-Token"),
        request.app.state.webhook_secret,
    )
    # Implement webhook logic here
    message = await request.json()

    parsed_message = parse_telegram_message(message)

    if not parsed_message:
        return {"status": "No message received"}
    else:
        # Process the parsed message and respond accordingly
        if parsed_message.get("kind") == "text":
            chat_id = parsed_message.get("chat_id") 
            message_text = parsed_message.get("text") 
            if chat_id is not None and message_text:
                bot: Bot = request.app.state.bot
                await bot.send_message(chat_id=chat_id, text=f"Received your message: {message_text} ; chat_id: {chat_id}")
                return {"status": "Message received", "message": message_text, "chat_id": chat_id}
            else:
                return {"status": "Message missing chat_id or text"}
        elif parsed_message.get("kind") == "voice":
            chat_id = parsed_message.get("chat_id") 
            file_id = parsed_message.get("file_id")
            if chat_id is not None and file_id:
                bot: Bot = request.app.state.bot
                await bot.send_message(chat_id=chat_id, text=f"Received your voice message with file_id: {file_id} ; chat_id: {chat_id}")
                return {"status": "Voice message received", "file_id": file_id, "chat_id": chat_id}    
            else:
                return {"status": "Voice message missing chat_id or file_id"}       
        else:
            return {"status": "Update received but no message found"}


##test de api
@app.get("/")
async def root():
   return {"message": "Hello World1"}