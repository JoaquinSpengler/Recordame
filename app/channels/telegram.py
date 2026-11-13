import asyncio

from fastapi import HTTPException
from telegram import Bot


def validate_webhook_secret(
    webhook_secret_token: str | None,
    expected_secret: str,
) -> None:
    if webhook_secret_token != expected_secret:
        raise HTTPException(status_code=403, detail="Unauthorized webhook secret token")

def parse_telegram_message(update: dict) -> dict | None:
    if not update:
        return None

    parsed_data = {}
    
    if update.get("message"):

        message_text = update["message"].get("text")
        if message_text:
            parsed_data["kind"] = "text"
            parsed_data["chat_id"] = update["message"].get("chat", {}).get("id")
            parsed_data["text"] = update["message"].get("text")
            parsed_data["from_user"] = update["message"].get("from", {}).get("username")
        elif update["message"].get("voice"):
            parsed_data["kind"] = "voice"
            parsed_data["chat_id"] = update["message"].get("chat", {}).get("id")
            parsed_data["file_id"] = update["message"].get("voice", {}).get("file_id")
            parsed_data["from_user"] = update["message"].get("from", {}).get("username")
        else:
             return None

        return parsed_data

    return None

async def send_telegram_message(bot: Bot, chat_id: int, text: str) -> None:
    try:
        await bot.send_message(chat_id=chat_id, text=text)
    except Exception as e:
        print(f"Error sending message to chat {chat_id}: {e}")

async def download_telegram_file(bot: Bot, file_id: str) -> bytes:
    try:
        telegram_file = await bot.get_file(file_id)
        file_content = await telegram_file.download_as_bytearray()
        return file_content
    except Exception as e:
        print(f"Error downloading file with ID {file_id}: {e}")
        return b""

async def transcribe_audio(model, audio_bytes: bytes) -> str:
    from io import BytesIO
    from app.services.transcription import get_transcription

    audio_buffer = BytesIO(audio_bytes)
    audio_buffer.seek(0)
    transcription = await asyncio.to_thread(get_transcription, model, audio_buffer)
    return transcription