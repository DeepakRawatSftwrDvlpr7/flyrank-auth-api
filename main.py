import os
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

# Stage 0: Setup Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    print("WARNING: Missing SUPABASE_URL or SUPABASE_KEY in .env file")
    SUPABASE_URL = "http://localhost"
    SUPABASE_KEY = "dummy"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Stage 5: Swagger UI Security (HTTPBearer adds the padlock icon)
app = FastAPI(title="Auth API", version="1.0")
security = HTTPBearer()

class UserCredentials(BaseModel):
    email: str
    password: str

# Stage 3 & 4: Middleware/Dependency for token verification
def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        user_resp = supabase.auth.get_user(token)
        if not user_resp or not user_resp.user:
            raise HTTPException(status_code=401, detail="Invalid or expired token")
        return {"user": user_resp.user, "token": token}
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

# Stage 1: Signup
@app.post("/auth/signup", status_code=201)
def signup(creds: UserCredentials):
    if not creds.email or not creds.password:
        raise HTTPException(status_code=400, detail="Email and password are required")
    try:
        res = supabase.auth.sign_up({"email": creds.email, "password": creds.password})
        return {"user": res.user}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Stage 1: Login
@app.post("/auth/login", status_code=200)
def login(creds: UserCredentials):
    if not creds.email or not creds.password:
        raise HTTPException(status_code=400, detail="Email and password are required")
    try:
        res = supabase.auth.sign_in_with_password({"email": creds.email, "password": creds.password})
        return {"access_token": res.session.access_token, "refresh_token": res.session.refresh_token}
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid login credentials")

# Stage 4: Logout
@app.post("/auth/logout", status_code=204)
def logout(auth_data: dict = Depends(verify_token)):
    try:
        supabase.auth.sign_out()
        return None
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Stage 2: Protected Route
@app.get("/protected/profile", status_code=200)
def get_profile(auth_data: dict = Depends(verify_token)):
    return {"user": auth_data["user"]}

# Stage 2: Public Route
@app.get("/public/info", status_code=200)
def public_info():
    return {"message": "Welcome stranger! This info is public."}
