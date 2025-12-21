from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

    # one-to-one relation
    employee = relationship(
        "Employee",
        back_populates="user",
        uselist=False
    )


class Employee(Base):
    __tablename__ = "employees"

    emp_id = Column(Integer, primary_key=True, index=True)
    f_name = Column(String(50))
    l_name = Column(String(50))
    email = Column(String(100), unique=True, nullable=False, index=True)
    dept = Column(String(50))
    salary = Column(Integer)
    hire_date = Column(Date)

    # FK moved here (IMPORTANT)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    user = relationship("User", back_populates="employee")

