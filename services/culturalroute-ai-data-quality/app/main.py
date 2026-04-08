from fastapi import FastAPI
from app.routers.import_router import router

app = FastAPI(title="Data Quality Service")

app.include_router(router)
