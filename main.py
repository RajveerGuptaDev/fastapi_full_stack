from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from database import SessionLocal, engine
from models import Base, User, Employee
from schemas import UserSignup, UserLogin, UserResponse , UserUpdate
from Auth import hash_password
from Auth import verify_password, create_access_token
from Auth import get_current_user


app = FastAPI()
Base.metadata.create_all(bind=engine)



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def root(db: Session = Depends(get_db)):
    return {"status": "db connected"}

@app.post("/signup", response_model=UserResponse)
def signup(user: UserSignup, db: Session = Depends(get_db)):

    if db.query(User).filter(User.username == user.username).first():
        raise HTTPException(status_code=400, detail="Username already exists")

    
    employee = (
        db.query(Employee)
        .outerjoin(User)
        .filter(User.id == None)
        .first()
    )

    if not employee:
        raise HTTPException(status_code=400, detail="No employee available")

    new_user = User(
        username=user.username,
        password=hash_password(user.password),
        emp_id=employee.emp_id
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "username": new_user.username,
        "employee_name": f"{employee.f_name} {employee.l_name}"
    }

@app.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):

    # 1️⃣ User fetch karo
    db_user = db.query(User).filter(User.username == user.username).first()

    # 2️⃣ Username / password verify
    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    # 3️⃣ JWT token create
    access_token = create_access_token(
        data={
            "user_id": db_user.id,
            "username": db_user.username
        }
    )

    # 4️⃣ Response
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@app.post("/logout")
def logout(current_user: User = Depends(get_current_user)):
    return {
        "message": f"User {current_user.username} logged out successfully"
    }


@app.get("/users")
def get_all_users(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    users = db.query(User).all()
    result = []
    for user in users:
        result.append({
            "username": user.username,
            "employee": f"{user.employee.f_name} {user.employee.l_name}",
            "department": user.employee.dept,
            "Earning": user.employee.salary,
            "Hire Date": user.employee.hire_date
        })

    return {
        "logged_in_user": current_user.username,
        "data": result
    }



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
    return {"message": "User updated"}

@app.delete("/users/{user_id}")
def delete_user(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not allowed")

    db.delete(current_user)
    db.commit()
    return {"message": "User deleted"}


