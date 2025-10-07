# Movie Ticket Booking System (Django + DRF)
It implements JWT authentication, movie/show management, seat booking, and Swagger API docs.

## Features
- Signup / Login (JWT)
- Movie, Show, Booking models
- Booking endpoints with business rules: prevent double booking and overbooking
- Swagger documentation at `/swagger/`
- Simple unit tests (example)

## Quick Start (if you want to run locally)
1. Create a virtualenv and install:
   ```bash
   python -m venv venv
   source venv/bin/activate      # or venv\Scripts\activate on Windows
   pip install -r requirements.txt
   ```

2. Create a PostgreSQL database (or use SQLite by adjusting settings).

3. Copy `.env.example` to `.env` and update DB and SECRET settings.

4. Run migrations and start server:
   ```bash
   python manage.py migrate
   python manage.py runserver
   ```

5. Open Swagger docs:
   ```
   http://localhost:8000/swagger/
   ```

## API Endpoints (high level)
- `POST /api/signup/` -> Register
- `POST /api/token/` -> Obtain JWT (login)
- `GET /api/movies/` -> List movies
- `GET /api/movies/{id}/shows/` -> Shows for a movie
- `POST /api/shows/{id}/book/` -> Book seat (body: {"seat_number": 5})
- `POST /api/bookings/{id}/cancel/` -> Cancel booking
- `GET /api/my-bookings/` -> Bookings for logged-in user

