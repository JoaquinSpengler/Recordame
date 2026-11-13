import os
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from fastapi import FastAPI, Request, APIRouter
from telegram import Bot
from faster_whisper import WhisperModel
from app.routers.telegram import router as telegram_router

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    bot_token = os.getenv("telegram_bot_token")
    if not bot_token:
        raise RuntimeError("Falta configurar telegram_bot_token en .env")

    webhook_secret = os.getenv("TELEGRAM_WEBHOOK_SECRET")
    if not webhook_secret:
        raise RuntimeError("Falta configurar TELEGRAM_WEBHOOK_SECRET en .env")

    model = WhisperModel("small", device="cpu", compute_type="int8")

    async with Bot(token=bot_token) as bot:
        app.state.bot = bot
        app.state.webhook_secret = webhook_secret
        app.state.transcription_model = model
        yield

app = FastAPI(lifespan=lifespan)

app.include_router(telegram_router)

##Endpoint que consulta con un bot de telegram y devuelve la respuesta del bot
@app.get("/botGetME")
async def bot_get_me(request: Request):
    bot: Bot = request.app.state.bot
    user = await bot.get_me()
    return {"id": user.id, "username": user.username}


##test de api
@app.get("/")
async def root():
   return {"message": "Hello World"}