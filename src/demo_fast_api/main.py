from fastapi import FastAPI
from demo_fast_api.controllers.user_controller import router as user_router
from demo_fast_api.controllers.auth_controller import router as auth_router
from demo_fast_api.controllers.files_controller import router as file_router

app = FastAPI()
app.include_router(user_router)
app.include_router(auth_router)
app.include_router(file_router)

@app.get("/")
def read_root():
    return "API is running..."
    