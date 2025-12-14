from datetime import timedelta

from fastapi import status, HTTPException
from sqlmodel import select, Session

from src.core.token import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from src.core.recaptcha import verify_recaptcha_token
from src.models.user import User
from src.core.hashing import hash_password, verify_password
from src.schemas.auth_schema import SignUpSchema, LoginSchema
from src.core.helpers import check_email_exists, check_username_exists


async def signup(data: SignUpSchema, db: Session):
    # Verify reCAPTCHA token BEFORE processing signup
    await verify_recaptcha_token(data.recaptcha_token)

    if check_email_exists(data.email, db):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    if check_username_exists(data.username, db):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )

    user_data = data.model_dump(
        exclude={'recaptcha_token'})  # Don't store the token
    user_data['password'] = hash_password(user_data['password'])

    user = User(**user_data)
    try:
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}"
        )


async def login(data: LoginSchema, db: Session):
    # Verify reCAPTCHA token BEFORE processing login
    await verify_recaptcha_token(data.recaptcha_token)

    user = db.scalar(select(User).where(
        (User.email == data.login) | (User.username == data.login)))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    if not verify_password(data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Incorrect password"
        )

    # generate a jwt and return it
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return user, access_token
