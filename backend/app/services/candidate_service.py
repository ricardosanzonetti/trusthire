from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.candidate import Candidate
from app.repositories.candidate_repository import CandidateRepository
from app.schemas.candidate import CandidateCreate


def create_candidate(
    db: Session,
    candidate_data: CandidateCreate
) -> Candidate:

    repository = CandidateRepository(db)

    candidate = Candidate(
        full_name=candidate_data.full_name,
        email=candidate_data.email,
        linkedin_url=candidate_data.linkedin_url
    )

    return repository.create(candidate)


def get_candidates(db: Session):
    repository = CandidateRepository(db)

    return repository.get_all()


def get_candidate_by_id(
    db: Session,
    candidate_id: int
):
    repository = CandidateRepository(db)

    candidate = repository.get_by_id(candidate_id)

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
    repository = CandidateRepository(db)

    candidate = repository.get_by_id(candidate_id)

    if not candidate:
        raise HTTPException(
            status_code=404,
            detail="Candidate not found"
        )

    repository.delete(candidate)

    return candidate


def update_candidate(
    db: Session,
    candidate_id: int,
    candidate_data: CandidateCreate
):
    repository = CandidateRepository(db)

    candidate = repository.get_by_id(candidate_id)

    if not candidate:
        raise HTTPException(
            status_code=404,
            detail="Candidate not found"
        )

    candidate.full_name = candidate_data.full_name
    candidate.email = candidate_data.email
    candidate.linkedin_url = candidate_data.linkedin_url

    return repository.update(candidate)


def verify_linkedin(
    db: Session,
    candidate_id: int
):
    repository = CandidateRepository(db)

    candidate = repository.get_by_id(candidate_id)

    if not candidate:
        raise HTTPException(
            status_code=404,
            detail="Candidate not found"
        )

    if candidate.linkedin_url:
        candidate.verification_status = "verified"
    else:
        candidate.verification_status = "failed"

    repository.update(candidate)

    return {
        "message": "Verification completed",
        "verification_status": candidate.verification_status
    }