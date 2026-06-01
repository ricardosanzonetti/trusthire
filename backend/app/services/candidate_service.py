from fastapi import HTTPException
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


def get_candidate_by_id(
    db: Session,
    candidate_id: int
):
    candidate = (
        db.query(Candidate)
        .filter(Candidate.id == candidate_id)
        .first()
    )

    if not candidate:
        raise HTTPException(
            status_code=404,
            detail="Candidate not found"
        )

    return candidate


def delete_candidate(
    db: Session,
    candidate_id: int
):
    candidate = (
        db.query(Candidate)
        .filter(Candidate.id == candidate_id)
        .first()
    )

    if not candidate:
        raise HTTPException(
            status_code=404,
            detail="Candidate not found"
        )

    db.delete(candidate)
    db.commit()

    return candidate


def update_candidate(
    db: Session,
    candidate_id: int,
    candidate_data: CandidateCreate
):
    candidate = (
        db.query(Candidate)
        .filter(Candidate.id == candidate_id)
        .first()
    )

    if not candidate:
        raise HTTPException(
            status_code=404,
            detail="Candidate not found"
        )

    candidate.full_name = candidate_data.full_name
    candidate.email = candidate_data.email
    candidate.linkedin_url = candidate_data.linkedin_url

    db.commit()
    db.refresh(candidate)

    return candidate