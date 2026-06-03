# pyrefly: ignore [missing-import]
from fastapi import FastAPI,Request
from routes.user import router as user_router
from routes.auth import router as auth_router
from database import Base,engine
app= FastAPI()
app.include_router(user_router)
app.include_router(auth_router)

# 

# app = FastAPI()
Base.metadata.create_all(bind=engine)

# Allow React frontend

@app.middleware("http")
async def log_requests(request: Request, call_next):
    print(f"Request: {request.url}")

    response = await call_next(request)

    print("Response sent")

    return response

@app.get("/")
def hello():
    return{
        "msg":"Hello"
    }

# pyrefly: ignore [missing-import]
from fastapi import File, UploadFile
import shutil
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    with open(f"uploads/{file.filename}", "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"msg": "File saved"}
from fastapi.staticfiles import StaticFiles

app.mount("/files", StaticFiles(directory="uploads"), name="files")