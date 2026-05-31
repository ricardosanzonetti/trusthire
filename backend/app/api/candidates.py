from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.candidate import (
    CandidateCreate,
    CandidateResponse
)
from app.services.candidate_service import create_candidate

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
    db: Session = Depends(get_db)
):
    return create_candidate(
        db=db,
        candidate_data=candidate
    )