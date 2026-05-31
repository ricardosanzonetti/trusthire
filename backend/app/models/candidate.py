from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.base import Base


class Candidate(Base):
    __tablename__ = "candidates"

    id: Mapped[int] = mapped_column(primary_key=True)

    full_name: Mapped[str] = mapped_column(String(255))
    email: Mapped[str] = mapped_column(String(255), unique=True)

    linkedin_url: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True
    )

    verification_status: Mapped[str] = mapped_column(
        String(50),
        default="pending"
    )