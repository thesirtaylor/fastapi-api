import logging

from fastapi import FastAPI

from app.api.user_api import router as user_router

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

app = FastAPI()

@app.get("/api/health-check")
def root():
    return {"message": "Welcome to FastAPI with SQLAlchemy"}

app.include_router(user_router, prefix="/api/v1")

@app.on_event("startup")
async def startup():
    #perform any async startup here, if needed
    logging.info("server is starting up")
    # pass

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)