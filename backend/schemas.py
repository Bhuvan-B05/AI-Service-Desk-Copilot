from datetime import datetime
from pydantic import BaseModel, EmailStr


# ---------- User ----------

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    created_at: datetime

    model_config = {
        "from_attributes": True
    }


# ---------- Token ----------

class Token(BaseModel):
    access_token: str
    token_type: str


# ---------- Ticket ----------

class TicketCreate(BaseModel):
    title: str
    description: str


class TicketUpdate(BaseModel):
    status: str


class TicketResponse(BaseModel):
    id: int
    title: str
    description: str

    category: str
    priority: str
    severity: str

    status: str

    ai_summary: str | None = None
    ai_root_cause: str | None = None
    ai_resolution: str | None = None

    created_at: datetime

    assigned_team: str | None = None
    estimated_time: str | None = None

    model_config = {
        "from_attributes": True
    }