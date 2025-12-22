from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from database import SessionLocal, engine
from models import Base, User, Employee
from schemas import UserSignup, UserLogin, UserUpdate
from auth import hash_password, verify_password, create_access_token, get_current_user
from fastapi.middleware.cors import CORSMiddleware

# ---------------- APP INIT ----------------
app = FastAPI()
Base.metadata.create_all(bind=engine)

# ---------------- DB DEP ----------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------------- ROOT ----------------
@app.get("/")
def root():
    return {"status": "db connected"}

# ---------------- SIGNUP ----------------
@app.post("/signup")
def signup(user: UserSignup, db: Session = Depends(get_db)):

    # username exists check
    if db.query(User).filter(User.username == user.username).first():
        raise HTTPException(status_code=400, detail="Username already exists")

    # get free GOT character
    employee = db.query(Employee).filter(Employee.user_id == None).first()
    if not employee:
        raise HTTPException(status_code=400, detail="No character available")

    # create user
    new_user = User(
        username=user.username,
        password=hash_password(user.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # assign character
    employee.user_id = new_user.id
    db.commit()

    # auto-login token
    access_token = create_access_token(
        data={"user_id": new_user.id}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "username": new_user.username,
        "employee_name": f"{employee.f_name} {employee.l_name}"
    }

# ---------------- LOGIN ----------------
@app.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):

    db_user = db.query(User).filter(User.username == user.username).first()

    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    access_token = create_access_token(
        data={"user_id": db_user.id}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

# ---------------- LOGOUT ----------------
@app.post("/logout")
def logout(current_user: User = Depends(get_current_user)):
    # JWT logout handled on frontend
    return {"message": f"User {current_user.username} logged out successfully"}

# ---------------- GET ALL USERS ----------------
@app.get("/users")
def get_all_users(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    users = db.query(User).all()
    result = []

    for user in users:
        emp = user.employee
        result.append({
            "username": user.username,
            "employee": f"{emp.f_name} {emp.l_name}" if emp else None,
            "department": emp.dept if emp else None,
            "earning": emp.salary if emp else None,
            "hire_date": emp.hire_date if emp else None
        })

    return {
        "logged_in_user": current_user.username,
        "data": result
    }

@app.get("/me")
def get_me(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == current_user.id).first()
    emp = user.employee

    return {
        "username": user.username,
        "character": f"{emp.f_name} {emp.l_name}" if emp else None,
        "department": emp.dept if emp else None,
        "salary": emp.salary if emp else None
    }


# ---------------- UPDATE USER ----------------
@app.put("/users/{user_id}")
def update_user(
    user_id: int,
    data: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not allowed")

    current_user.username = data.username
    db.commit()

    return {"message": "User updated successfully"}

# ---------------- DELETE USER ----------------
@app.delete("/users/{user_id}")
def delete_user(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not allowed")

    # free character
    if current_user.employee:
        current_user.employee.user_id = None

    db.delete(current_user)
    db.commit()

    return {"message": "User deleted successfully"}

# ---------------- CORS ----------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # 👈 sab origins allow
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)