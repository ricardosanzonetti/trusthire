from datetime import datetime, timedelta, UTC

from jose import jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories.user_repository import UserRepository


SECRET_KEY = "super-secret-key-change-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str
) -> bool:
    return pwd_context.verify(
        plain_password,
        hashed_password
    )


def create_access_token(
    data: dict
) -> str:
    to_encode = data.copy()

    expire = (
        datetime.now(UTC)
        + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
    )

    to_encode.update(
        {"exp": expire}
    )

    return jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


def register_user(
    db: Session,
    email: str,
    password: str
) -> User:
    repository = UserRepository(db)

    existing_user = (
        repository.get_by_email(email)
    )

    if existing_user:
        raise ValueError(
            "Email already registered"
        )

    user = User(
        email=email,
        hashed_password=hash_password(password)
    )

    return repository.create(user)


def login_user(
    db: Session,
    email: str,
    password: str
) -> str:
    repository = UserRepository(db)

    user = repository.get_by_email(email)

    if not user:
        raise ValueError(
            "Invalid credentials"
        )

    if not verify_password(
        password,
        user.hashed_password
    ):
        raise ValueError(
            "Invalid credentials"
        )

    return create_access_token(
        {"sub": user.email}
    )