from fastapi import APIRouter, Request
from app.channels.telegram import parse_telegram_message, validate_webhook_secret,send_telegram_message, download_telegram_file, transcribe_audio

# Puedes añadir un prefijo común y etiquetas para la documentación Swagger
router = APIRouter(
    prefix="/webhook/telegram",
    tags=["Telegram"]
)

@router.post("/")
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
                await send_telegram_message(request.app.state.bot, chat_id, f"Received your message: {message_text} ; chat_id: {chat_id}")
                return {"status": "Message received", "message": message_text, "chat_id": chat_id}
            else:
                return {"status": "Message missing chat_id or text"}
        elif parsed_message.get("kind") == "voice":
            chat_id = parsed_message.get("chat_id") 
            file_id = parsed_message.get("file_id")
            if chat_id is not None and file_id:
                audio_bytes = await download_telegram_file(request.app.state.bot, file_id)
                transcription = await transcribe_audio(request.app.state.transcription_model, audio_bytes)
                await send_telegram_message(request.app.state.bot, chat_id, f"Transcription: {transcription}")
                return {"status": "Voice message transcribed", "transcription": transcription, "chat_id": chat_id}
            else:
                return {"status": "Voice message missing chat_id or file_id"}       
        else:
            return {"status": "Update received but no message found"}