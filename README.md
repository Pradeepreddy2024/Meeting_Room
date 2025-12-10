# Meeting Room Booking App (Microservices, FastAPI, PostgreSQL)

## Services

- `user_service` – user registration, login, JWT auth
- `room_service` – CRUD for meeting rooms
- `booking_service` – create bookings with priority rules

All services use:
- FastAPI
- PostgreSQL via SQLAlchemy
- JWT auth (`python-jose`)
- Password hashing (`passlib[bcrypt]`)

## Prerequisites

- Docker & Docker Compose installed

## How to run

1. Clone this project.
2. In the project root, check `.env` and adjust secrets if needed.
3. Run:

   ```bash
   docker-compose up --build
   ```

This will start:
- Postgres at `localhost:5432`
- `user_service` at `http://localhost:8001`
- `room_service` at `http://localhost:8002`
- `booking_service` at `http://localhost:8003`

## API Docs

Each service exposes Swagger UI at:

- `user_service`: `http://localhost:8001/docs`
- `room_service`: `http://localhost:8002/docs`
- `booking_service`: `http://localhost:8003/docs`

## Basic Flow

1. **Register user** (TEAM_LEAD, MANAGER, or CEO)

   `POST http://localhost:8001/users/register`

2. **Login** to get JWT

   `POST http://localhost:8001/users/login`

   Use form fields:
   - `username` = email
   - `password` = password

   Response contains `access_token`.

3. Use `Authorization: Bearer <token>` header when calling:

   - `GET/POST/PUT/DELETE http://localhost:8002/rooms`
   - `GET/POST/DELETE http://localhost:8003/bookings`

## Booking Priority Rules

- Roles:
  - TEAM_LEAD
  - MANAGER
  - CEO

- Meeting types:
  - TEAM
  - PROJECT
  - CLIENT

- Allowed combinations:
  - CEO: CLIENT, PROJECT
  - MANAGER: PROJECT, TEAM
  - TEAM_LEAD: TEAM

- Priority (highest → lowest):
  - CEO
  - MANAGER
  - TEAM_LEAD

When creating a booking:
- If there is a **higher priority** existing booking that overlaps in the same room, the new booking is **rejected**.
- If the new booking has **higher priority**, the existing conflicting lower-priority bookings are **auto-cancelled**.

## Next Steps

- Add an API gateway or HTTP reverse proxy (e.g., Nginx) to route a single base URL.
- Add role-based access control decorators/utilities.
- Build the React + Material UI front-end that talks to these services.
- Add tests (pytest) and CI/CD.
