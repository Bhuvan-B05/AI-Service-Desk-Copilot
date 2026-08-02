from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from ai import analyze_ticket
from sqlalchemy import func
import models
import schemas

from database import get_db
from auth import (
    hash_password,
    verify_password,
    create_access_token,
    decode_access_token
)

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


@router.post("/register", response_model=schemas.UserResponse)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):

    existing = db.query(models.User).filter(
        models.User.email == user.email
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    new_user = models.User(
        name=user.name,
        email=user.email,
        hashed_password=hash_password(user.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.post("/login", response_model=schemas.Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    existing = db.query(models.User).filter(
        models.User.email == form_data.username
    ).first()

    if existing is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    if not verify_password(
        form_data.password,
        existing.hashed_password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    token = create_access_token(
        {
            "sub": str(existing.id)
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):

    payload = decode_access_token(token)

    if payload is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

    user = db.query(models.User).filter(
        models.User.id == int(payload["sub"])
    ).first()

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="User not found"
        )

    return user


@router.get("/me", response_model=schemas.UserResponse)
def me(current_user: models.User = Depends(get_current_user)):
    return current_user


@router.post("/tickets", response_model=schemas.TicketResponse)
def create_ticket(
    ticket: schemas.TicketCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    new_ticket = models.Ticket(
        title=ticket.title,
        description=ticket.description,
        owner=current_user
    )

    db.add(new_ticket)
    db.commit()
    db.refresh(new_ticket)

    return new_ticket

@router.get("/tickets", response_model=list[schemas.TicketResponse])
def get_tickets(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    return (
        db.query(models.Ticket)
        .filter(models.Ticket.user_id == current_user.id)
        .order_by(models.Ticket.created_at.desc())
        .all()
    )


@router.put("/tickets/{ticket_id}", response_model=schemas.TicketResponse)
def update_ticket(
    ticket_id: int,
    ticket: schemas.TicketUpdate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    existing = (
        db.query(models.Ticket)
        .filter(
            models.Ticket.id == ticket_id,
            models.Ticket.user_id == current_user.id
        )
        .first()
    )

    if existing is None:
        raise HTTPException(
            status_code=404,
            detail="Ticket not found"
        )

    existing.status = ticket.status

    db.commit()
    db.refresh(existing)

    return existing


@router.delete("/tickets/{ticket_id}")
def delete_ticket(
    ticket_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    existing = (
        db.query(models.Ticket)
        .filter(
            models.Ticket.id == ticket_id,
            models.Ticket.user_id == current_user.id
        )
        .first()
    )

    if existing is None:
        raise HTTPException(
            status_code=404,
            detail="Ticket not found"
        )

    db.delete(existing)
    db.commit()

    return {
        "message": "Ticket deleted successfully"
    }

@router.post("/tickets/{ticket_id}/analyze")
def analyze(
    ticket_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    ticket = (
        db.query(models.Ticket)
        .filter(
            models.Ticket.id == ticket_id,
            models.Ticket.user_id == current_user.id
        )
        .first()
    )

    if ticket is None:
        raise HTTPException(
            status_code=404,
            detail="Ticket not found"
        )

    result = analyze_ticket(
    ticket.title,
    ticket.description
)

    required_keys = [
        "category",
        "priority",
        "severity",
        "summary",
        "root_cause",
        "resolution",
        "assigned_team",
        "estimated_time"
    ]

    if not all(key in result for key in required_keys):
        raise HTTPException(
            status_code=500,
            detail="AI returned an invalid response."
        )

    ticket.category = result["category"]
    ticket.priority = result["priority"]
    ticket.severity = result["severity"]

    ticket.ai_summary = result["summary"]
    ticket.ai_root_cause = result["root_cause"]
    ticket.ai_resolution = result["resolution"]

    ticket.assigned_team = result["assigned_team"]
    ticket.estimated_time = result["estimated_time"]

    db.commit()
    db.refresh(ticket)

    return {
        "message": "Analysis completed",
        "analysis": result
    }
@router.get("/dashboard")
def dashboard(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    tickets = db.query(models.Ticket).filter(
        models.Ticket.user_id == current_user.id
    )

    total = tickets.count()

    open_tickets = tickets.filter(
        models.Ticket.status == "Open"
    ).count()

    resolved = tickets.filter(
        models.Ticket.status == "Resolved"
    ).count()

    high_priority = tickets.filter(
        models.Ticket.priority == "High"
    ).count()

    critical = tickets.filter(
        models.Ticket.severity == "Critical"
    ).count()

    return {
        "total_tickets": total,
        "open_tickets": open_tickets,
        "resolved_tickets": resolved,
        "high_priority": high_priority,
        "critical_tickets": critical
    }