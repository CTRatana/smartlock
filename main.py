from typing import Union
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.database import Base, engine

from modules.user.controller import router as user_router
from modules.card.controller import router as card_router
from modules.history.controller import router as history_router
from modules.attendance.controller import router as attendace_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router)
app.include_router(card_router)
app.include_router(history_router)
app.include_router(attendace_router)

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)


@app.on_event("shutdown")
def shutdown():
    engine.dispose()


@app.get('/')
def welcome():
    return f'Welcome to API'