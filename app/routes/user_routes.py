from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas, auth
from ..database import SessionLocal
from ..dependencies import role_required
user_router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@user_router.post("/signup")
def signup(user:schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    hashed = auth.hash_password(user.password)
    new_user = models.User(username=user.username, password=hashed, role=user.role)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message":"User created","username":new_user.username, "role":new_user.role}


@user_router.post("/login")
def login(user:schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if not db_user or not auth.verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = auth.create_access_token({"sub": db_user.username, "role":db_user.role})
    return {"access_token": token, "token_type":"bearer"}


@user_router.get("/admin-only")
def admin_dashboard(role: str = Depends(role_required("admin"))):
    return {"message": f"Hello Admin! Your role is: {role}"}

@user_router.get("/user-only")
def user_dashboard(role: str = Depends(role_required("user"))):
    return {"message": f"Hello User! Your role is: {role}"}

