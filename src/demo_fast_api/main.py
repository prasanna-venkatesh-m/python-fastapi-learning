from fastapi import FastAPI
from demo_fast_api.controllers.user_controller import router as user_router

app = FastAPI()
app.include_router(user_router)

@app.get("/")
def read_root():
    return "API is running..."