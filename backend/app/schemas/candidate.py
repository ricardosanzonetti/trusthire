from pydantic import BaseModel, EmailStr


class CandidateCreate(BaseModel):
    full_name: str
    email: EmailStr
    linkedin_url: str | None = None


class CandidateResponse(BaseModel):
    id: int
    full_name: str
    email: str
    linkedin_url: str | None
    verification_status: str

    model_config = {
        "from_attributes": True
    }