🐉 GOT Assigning System

A full-stack web application inspired by Game of Thrones, where users can sign up, log in, and view their assigned GOT character on a profile page, using secure authentication and cloud-based infrastructure.

📌 Project Overview

The GOT Assigning System demonstrates:

Full-stack web development

JWT-based authentication

Backend API development with FastAPI

Cloud database integration using Supabase

Real-world deployment using Vercel & Render

🚀 Features

User Signup

User Login

JWT Token-based Authentication

GOT Character Assignment

Secure Profile Page

Logout Functionality

🛠️ Tech Stack
Frontend

HTML

CSS

JavaScript

Deployed on Vercel

Backend

FastAPI (Python)

SQLAlchemy (ORM)

Deployed on Render

Database

PostgreSQL

Hosted on Supabase (Cloud Database)

Authentication

JWT (JSON Web Tokens)

Tools

VS Code

GitHub

Postman

🌐 Deployment Architecture

Deployment Flow

User
 ↓
Frontend (Vercel)
 ↓
Backend API (Render - FastAPI)
 ↓
Cloud Database (Supabase - PostgreSQL)

📂 Project Structure
got-assigning-system/
│
├── backend/
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   ├── database.py
│   ├── auth.py
│
├── frontend/
│   ├── index.html
│   ├── login.html
│   ├── signup.html
│   ├── profile.html
│   ├── style.css
│   ├── script.js
│
├── requirements.txt
└── README.md

🔐 API Endpoints
POST /signup

Registers a new user.

Request Body

{
  "username": "jon_snow",
  "password": "winter123"
}


Response

{
  "access_token": "jwt_token_here",
  "username": "jon_snow"
}

POST /login

Authenticates the user and returns a JWT token.

GET /profile

Fetches logged-in user details and assigned GOT character using JWT token.

🗄️ Database Design
Tables Used

users

employees

Relationship

One-to-One relationship between User and Employee

▶️ How to Run Locally (Optional)
Backend
pip install -r requirements.txt
uvicorn main:app --reload

Frontend
Open frontend/index.html in browser

☁️ Deployment Details
Frontend Deployment (Vercel)

Static frontend deployed on Vercel

Connected to backend via public Render API URL

Environment variables used for API base URL

Backend Deployment (Render)

FastAPI backend hosted on Render

Public API URL used by frontend

CORS enabled for Vercel domain

Database (Supabase)

PostgreSQL cloud database hosted on Supabase

Secure connection using database URL

Managed backups and scalability

 Pages

Signup Page

Login Page

Profile Page

⚠️ Challenges Faced

CORS issues between Vercel and Render

Supabase and render ipv4 and ipv6 connection issues

Supabase ipv4 session pooling issues

Environment variable configuration

JWT token handling in deployed environment

Cloud database connectivity

🚀 Future Enhancements

each character journey and story 

character dragon assigning

Password Reset

Valyerion commands for dragon riding

👨‍💻 Author

Rajveer Gupta
Full Stack Developer | FastAPI | PostgreSQL | Cloud Deployment

📄 License

This project is created for learning and demonstration purposes.