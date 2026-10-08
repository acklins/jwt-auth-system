# Auth System

**Module:** 5 — FastAPI Development
**Estimated time:** 55 minutes

## Objective

Build a JWT-based authentication system with user registration, login, and protected endpoints using password hashing, token creation, and FastAPI dependency injection.

## What You'll Do

1. In `app/models/user.py`, define the `User` ORM model with columns: id, username (unique), email (unique), hashed_password.
2. In `app/schemas/user.py`, define three schemas:
   - `UserCreate` — registration input (username, email, password).
   - `UserResponse` — returned to clients (id, username, email -- never the password).
   - `TokenResponse` — JWT response (access_token, token_type).
3. In `app/auth.py`, implement the authentication utilities:
   - Create a `CryptContext` for bcrypt password hashing.
   - `hash_password()` — hash a plain-text password.
   - `verify_password()` — verify a plain-text password against a hash.
   - `create_access_token()` — build a signed JWT with an expiration claim.
   - `get_current_user()` — a FastAPI dependency that decodes a JWT, looks up the user, and returns it (or raises 401).
4. In `app/routers/auth.py`, implement the endpoints:
   - `POST /register` — create a new user with a hashed password, reject duplicates with 409.
   - `POST /token` — authenticate credentials via `OAuth2PasswordRequestForm`, return a JWT.
   - `GET /me` — return the current user using `Depends(get_current_user)`.
   - Add at least one additional protected endpoint.
5. In `app/main.py`, include the auth router with `prefix="/auth"`.

## Starter Code

```
app/
  __init__.py
  main.py              — FastAPI app; needs router inclusion
  database.py          — Database setup (pre-configured)
  auth.py              — JWT and password utility stubs
  models/
    __init__.py
    user.py            — User ORM model stub
  schemas/
    __init__.py
    user.py            — User and Token schema stubs
  routers/
    __init__.py
    auth.py            — Auth endpoint stubs
```

## Running

```bash
uvicorn app.main:app --reload
```

## Deliverable

A working auth system where users can register, log in to receive a JWT, and access protected endpoints. The Swagger UI "Authorize" button should work for testing protected routes.
