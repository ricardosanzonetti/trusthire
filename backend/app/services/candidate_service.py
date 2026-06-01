from sqlalchemy.orm import Session

from app.models.candidate import Candidate
from app.schemas.candidate import CandidateCreate


def create_candidate(
    db: Session,
    candidate_data: CandidateCreate
) -> Candidate:

    candidate = Candidate(
        full_name=candidate_data.full_name,
        email=candidate_data.email,
        linkedin_url=candidate_data.linkedin_url
    )

    db.add(candidate)
    db.commit()
    db.refresh(candidate)

    return candidate


def get_candidates(db: Session):
    return db.query(Candidate).all()