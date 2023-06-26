from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel
import base64
import os
import cv2
import numpy
from starlette.responses import StreamingResponse
import json
from dotenv import load_dotenv

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "fakehashedsecret",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret2",
        "disabled": True,
    },
}
class Attendance(BaseModel):
    user: str
    userId: str
    token: str
    # date: date
class APIWrapper():
    def __init__(self):
        self.host = os.getenv('HOST')
        self.port = os.getenv('PORT')
        self.app = FastAPI()

    def configure_routes(self):
        @self.app.get("/list-directory")
        async def list_directory():
            available_directories = {
                "material": [], # lecture material
                "transcripts": [], # Ai based lecture transcript
                "summaries": [], # Ai summerization of transcripts
                "videos": [] # the recorded video
            }
            files = []
            for directory in available_directories:
                try:
                    available_directories[directory] ={"content":os.listdir("data/" + directory)}
                except FileNotFoundError:
                    return {"message": "error: recreate directories"}
            return json.dumps(available_directories)
        @self.app.post("/attend/")
        async def attend(attendance: Attendance):
            #attendence in db
            print(attendance)
            return {"message": f"attendance recorded"}

        @self.app.get("/download")
        def download_file(directory: str, file_name: str):
            file_path = "./data/" + directory + '/' + file_name
            if not os.path.exists(file_path):
                print(file_path)
                raise HTTPException(status_code=404, detail="File not found")
            def file_generator():
                with open(file_path, "rb") as file:
                    yield from file
            return StreamingResponse(content=file_generator(), media_type="application/pdf")

        @self.app.get("/OK")
        def health_check():
            return {"message": "alive and well","code":0}

    def run(self):
        self.configure_routes()
        uvicorn.run(self.app, host=self.host,port=self.port)

if __name__ == "__main__":
    load_dotenv()
    test = APIWrapper()
    test.run()
    # if(port == None):
    #     port = 8000
    # uvicorn.run(app, host="0.0.0.0", port=int(port))