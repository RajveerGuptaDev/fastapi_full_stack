from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class Employee(Base):
    __tablename__ = "employees"

    emp_id = Column(Integer, primary_key=True, index=True)
    f_name = Column(String(50))
    l_name = Column(String(50))
    email = Column(String(100), unique=True, nullable=False,index=True)
    dept = Column(String(50))
    salary = Column(Integer)
    hire_date = Column(Date)

    # one-to-one relation banaya 
    user = relationship("User", back_populates="employee", uselist=False)


# NEW users table
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

    emp_id = Column(Integer, ForeignKey("employees.emp_id"))
    employee = relationship("Employee", back_populates="user")
