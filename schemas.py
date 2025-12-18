from pydantic import BaseModel

# -------- SIGNUP --------
class UserSignup(BaseModel):
    username: str
    password: str


# -------- LOGIN --------
class UserLogin(BaseModel):
    username: str
    password: str


# -------- RESPONSE --------
class UserResponse(BaseModel):
    username: str
    employee_name: str
