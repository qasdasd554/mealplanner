"""Endpointy uwierzytelniania — rejestracja i logowanie."""

from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
import json

from app.core.security import create_access_token, get_password_hash, verify_password
from app.db.session import get_db
from app.models import User
from app.schemas.user import Token, UserCreate, UserResponse

router = APIRouter()


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Rejestracja nowego użytkownika",
)
async def register(
    request: Request,
    db: AsyncSession = Depends(get_db),
) -> User:
    """Tworzy nowe konto użytkownika.

    Sprawdza unikalność adresu e-mail przed utworzeniem.
    """
    try:
        body_bytes = await request.body()
        if not body_bytes:
            raise ValueError("Empty body")
        
        parsed_body = await request.json()
        
        # Obejście problemu podwójnego kodowania JSON przez frontend
        if isinstance(parsed_body, str):
            parsed_body = json.loads(parsed_body)
            
        user_in = UserCreate(**parsed_body)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Nieprawidłowe dane rejestracji: {str(e)}"
        )

    result = await db.execute(select(User).where(User.email == user_in.email))
    existing = result.scalar_one_or_none()
    if existing is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Użytkownik z tym adresem e-mail już istnieje",
        )

    user = User(
        email=user_in.email,
        password_hash=get_password_hash(user_in.password),
        display_name=user_in.display_name,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


@router.post(
    "/login",
    response_model=Token,
    summary="Logowanie — OAuth2 password flow",
)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
) -> dict[str, str]:
    """Uwierzytelnia użytkownika i zwraca token JWT.

    Używa standardowego OAuth2 password flow (username = e-mail).
    """
    result = await db.execute(select(User).where(User.email == form_data.username))
    user = result.scalar_one_or_none()

    if user is None or not verify_password(form_data.password, user.hashed_password if hasattr(user, 'hashed_password') else user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Nieprawidłowy e-mail lub hasło",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}
