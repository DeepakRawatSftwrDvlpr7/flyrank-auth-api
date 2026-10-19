# Secure Auth API (FlyRank BE-03)

A secure API handling user authentication (Sign Up, Log In, and Log Out) and protecting routes using Supabase as the Identity Provider. Built with Python and FastAPI.

## Setup & Run Instructions
1. Create a Supabase project and get your Project URL and Anon Key.
2. Create a `.env` file with `SUPABASE_URL` and `SUPABASE_KEY`.
3. Install dependencies: `pip install -r requirements.txt`
4. Start the server: `uvicorn main:app --reload`
5. Test endpoints with the interactive Swagger UI at `http://localhost:8000/docs`.

## Endpoints
| Operation | Method | Endpoint | Auth Required? |
|---|---|---|---|
| Sign Up | POST | `/auth/signup` | No |
| Log In | POST | `/auth/login` | No |
| Log Out | POST | `/auth/logout` | Yes (Bearer Token) |
| Profile | GET | `/protected/profile` | Yes (Bearer Token) |
| Public Info | GET | `/public/info` | No |
