from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.candidate import Candidate


class CandidateRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, candidate: Candidate) -> Candidate:
        try:
            self.db.add(candidate)
            self.db.commit()
            self.db.refresh(candidate)

            return candidate

        except IntegrityError:
            self.db.rollback()
            raise

    def get_all(self) -> list[Candidate]:
        return self.db.query(Candidate).all()

    def get_by_id(self, candidate_id: int) -> Candidate | None:
        return (
            self.db.query(Candidate)
            .filter(Candidate.id == candidate_id)
            .first()
        )

    def update(self, candidate: Candidate) -> Candidate:
        self.db.commit()
        self.db.refresh(candidate)

        return candidate

    def delete(self, candidate: Candidate) -> None:
        self.db.delete(candidate)
        self.db.commit()