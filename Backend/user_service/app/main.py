
from fastapi import FastAPI
from fastapi import Request
from .database import get_db
from .database import Base, engine
from .routers import user, auth



Base.metadata.create_all(bind=engine)

app = FastAPI(title="User Service")

app.include_router(user.router, prefix="/api/users")
app.include_router(auth.router, prefix="/api/users")
