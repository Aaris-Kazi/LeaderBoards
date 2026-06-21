from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from appConstant import CORS_ORIGIN
from routing import health_router, v1_router
from controller import HealthController, InterServiceController
from databaseConnections.MySQLConnections import Base, MySQLConnections

app = FastAPI()

status = {"status": "success"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGIN,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=MySQLConnections().engine)

app.include_router(health_router)
app.include_router(v1_router)
