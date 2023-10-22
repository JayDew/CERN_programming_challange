from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from .routers.orders import router as orders_router
from .routers.plates import router as plates_router
from .routers.users import router as users_router
from .routers.reviews import router as reviews_router
from . import models
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)


app = FastAPI(root_path='/api/', version="0.3.0")


# Add CORS middleware for frontend
origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://127.0.0.1",
    "http://127.0.0.1:8000"
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(orders_router, prefix="/orders", tags=["orders"])
app.include_router(plates_router, prefix="/plates", tags=["plates"])
app.include_router(users_router, prefix="/users", tags=["users"])
app.include_router(reviews_router, prefix="/review", tags=["review"])


@app.on_event("startup")
async def startup():
    pass


@app.on_event("shutdown")
async def shutdown():
    pass
