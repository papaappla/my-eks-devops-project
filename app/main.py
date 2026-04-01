from fastapi import FastAPI
import os

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "EKS API Server is Running"}

@app.get("/healthz")
def health_check():
    return {"status": "ok"}
