from fastapi import HTTPException


def validate_webhook_secret(
    webhook_secret_token: str | None,
    expected_secret: str,
) -> None:
    if webhook_secret_token != expected_secret:
        raise HTTPException(status_code=403, detail="Unauthorized webhook secret token")
