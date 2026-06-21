from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User

from app.schemas.candidate import (
    CandidateCreate,
    CandidateResponse,
    VerificationResponse
)

from app.services.candidate_service import (
    create_candidate,
    get_candidates,
    get_candidate_by_id,
    delete_candidate,
    update_candidate,
    verify_linkedin
)

router = APIRouter(
    prefix="/candidates",
    tags=["Candidates"]
)


@router.post(
    "/",
    response_model=CandidateResponse
)
def create_candidate_endpoint(
    candidate: CandidateCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return create_candidate(
        db=db,
        candidate_data=candidate
    )


@router.get(
    "/",
    response_model=list[CandidateResponse]
)
def get_candidates_endpoint(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_candidates(db)


@router.get(
    "/{candidate_id}",
    response_model=CandidateResponse
)
def get_candidate_by_id_endpoint(
    candidate_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_candidate_by_id(
        db=db,
        candidate_id=candidate_id
    )


@router.put(
    "/{candidate_id}",
    response_model=CandidateResponse
)
def update_candidate_endpoint(
    candidate_id: int,
    candidate: CandidateCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return update_candidate(
        db=db,
        candidate_id=candidate_id,
        candidate_data=candidate
    )


@router.delete(
    "/{candidate_id}",
    response_model=CandidateResponse
)
def delete_candidate_endpoint(
    candidate_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return delete_candidate(
        db=db,
        candidate_id=candidate_id
    )


@router.post(
    "/{candidate_id}/verify-linkedin",
    response_model=VerificationResponse
)
def verify_linkedin_endpoint(
    candidate_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return verify_linkedin(
        db=db,
        candidate_id=candidate_id
    )