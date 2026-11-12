from fastapi import HTTPException


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