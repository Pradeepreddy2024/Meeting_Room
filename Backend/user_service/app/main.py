
from fastapi import FastAPI
from fastapi import Request
from .database import get_db
from .database import Base, engine
from .routers import user, auth



Base.metadata.create_all(bind=engine)

app = FastAPI(title="User Service")

from fastapi.middleware.cors import CORSMiddleware

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(user.router, prefix="/api/users")
app.include_router(auth.router, prefix="/api/users")
