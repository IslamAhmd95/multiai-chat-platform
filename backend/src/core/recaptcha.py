
import requests
from fastapi import HTTPException, status
from src.core.config import settings

RECAPTCHA_VERIFY_URL = "https://www.google.com/recaptcha/api/siteverify"


async def verify_recaptcha_token(recaptcha_token: str) -> bool:
    if not recaptcha_token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="reCAPTCHA token is required"
        )

    try:
        response = requests.post(
            RECAPTCHA_VERIFY_URL,
            data={
                "secret": settings.RECAPTCHA_SECRET_KEY,
                "response": recaptcha_token
            },
            timeout=10
        )
        response.raise_for_status()

        result = response.json()

        if not result.get("success"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="reCAPTCHA verification failed. Please try again."
            )

        return True

    except requests.RequestException as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error verifying reCAPTCHA: {str(e)}"
        )
