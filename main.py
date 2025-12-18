from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from database import SessionLocal, engine
from models import Base, User, Employee
from schemas import UserSignup, UserLogin, UserResponse , UserUpdate



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

    # 1️⃣ duplicate username check
    if db.query(User).filter(User.username == user.username).first():
        raise HTTPException(status_code=400, detail="Username already exists")

    # 2️⃣ free employee assign
    employee = db.query(Employee).filter(Employee.user == None).first()
    if not employee:
        raise HTTPException(status_code=400, detail="No employee available")

    # 3️⃣ create user
    new_user = User(
        username=user.username,
        password=user.password,
        emp_id=employee.emp_id
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "username": new_user.username,
        "employee_name": f"{employee.f_name} {employee.l_name}"
    }

@app.get("/users")
def get_all_users(db: Session = Depends(get_db)):
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
    return result


@app.put("/users/{user_id}")
def update_user(user_id: int, data: UserUpdate, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.username = data.username
    db.commit()

    return {"message": "User updated successfully"}

@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()

    return {"message": "User deleted successfully"}

