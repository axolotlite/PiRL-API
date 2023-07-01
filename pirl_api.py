from fastapi import FastAPI
from pydantic import BaseModel
import base64
from fastapi.responses import FileResponse
from fastapi.param_functions import Path
import os
import cv2
import numpy
from starlette.responses import StreamingResponse
import json
from dotenv import load_dotenv
import uvicorn
from utils import create_directories
from db_handler import DBHandler

class Attendance(BaseModel):
    user: str
    userId: int
    lessonId: int
    token: str
    # date: date
class APIWrapper():
    def __init__(self):
        host = os.getenv('HOST')
        port = os.getenv('PORT')
        self.app = FastAPI()
        config = uvicorn.Config(self.app, host=host, port=port, log_level="info")
        self.server = uvicorn.Server(config)
        available_directories = [
            "material", # lecture material
            "transcripts", # Ai based lecture transcript
            "summaries", # Ai summerization of transcripts
            "videos" # the recorded video
        ]
        create_directories(available_directories)
        self.db_handler = DBHandler()
        # self.instance = ThreadedUvicorn(config)
    def configure_routes(self):
    #     @self.app.get("/list-directory")
    #     async def list_directory():
    #         available_directories = {
    #             "material": [], # lecture material
    #             "transcripts": [], # Ai based lecture transcript
    #             "summaries": [], # Ai summerization of transcripts
    #             "videos": [] # the recorded video
    #         }
    #         files = []
    #         for directory in available_directories:
    #             try:
    #                 available_directories[directory] ={"content":os.listdir("data/" + directory)}
    #             except FileNotFoundError:
    #                 return {"message": "error: recreate directories"}
    #         return json.dumps(available_directories)


        @self.app.get("/list-directory/material")
        async def list_directory():
            files = []

            for file in os.listdir("data\material"):
                try:
                    files.append(file)
                    # available_directories[directory] ={"content":os.listdir("data/" + directory)}
                except FileNotFoundError:
                    return {"message": "error: recreate directories"}
            print(files)
            print(list(map(lambda file: file, files)))
            return list(map(lambda file: file, files))
        
        @self.app.get("/list-directory/summaries")
        async def list_directory():
            files = []

            for file in os.listdir("data\summaries"):
                try:
                    files.append(file)
                    # available_directories[directory] ={"content":os.listdir("data/" + directory)}
                except FileNotFoundError:
                    return {"message": "error: recreate directories"}
            print(files)
            print(list(map(lambda file: file, files)))
            return list(map(lambda file: file, files))
        
        @self.app.get("/list-directory/transcripts")
        async def list_directory():
            files = []

            for file in os.listdir("data/transcripts"):
                try:
                    files.append(file)
                    # available_directories[directory] ={"content":os.listdir("data/" + directory)}
                except FileNotFoundError:
                    return {"message": "error: recreate directories"}
            print(files)
            print(list(map(lambda file: file, files)))
            return list(map(lambda file: file, files))
        
        @self.app.get("/list-directory/videos")
        async def list_directory():
            files = []

            for file in os.listdir("data/videos"):
                try:
                    files.append(file)
                    # available_directories[directory] ={"content":os.listdir("data/" + directory)}
                except FileNotFoundError:
                    return {"message": "error: recreate directories"}
            print(files)
            print(list(map(lambda file: file, files)))
            return list(map(lambda file: file, files))


        @self.app.post("/attend/")
        async def attend(attendance: Attendance):
            #attendence in db
            exists = self.db_handler.add_student(attendance.userId,attendance.user)
            if(exists):
                print("userid already exists recording attendence")
            self.db_handler.add_attendance(attendance.userId,attendance.lessonId, True)
            print(attendance)
            return {"message": f"{attendance.user} attendance for {attendance.lessonId} recorded"}

        # @self.app.get("/download")
        # def download_file(directory: str, file_name: str):
        #     file_path = "./data/" + directory + '/' + file_name
        #     if not os.path.exists(file_path):
        #         print(file_path)
        #         raise HTTPException(status_code=404, detail="File not found")
        #     def file_generator():
        #         with open(file_path, "rb") as file:
        #             yield from file
        #     return StreamingResponse(content=file_generator(), media_type="application/pdf")

        @self.app.get('/material/{filename}')
        async def download_file(filename: str = Path(...)):
            directory = 'data/material'  # Set the directory where the files are stored
            print("hi i've been called material download")
            # Validate the requested file against a whitelist if needed
            # whitelist = ['file1.txt', 'file2.pdf']
            # if filename not in whitelist:
            #     raise HTTPException(status_code=404, detail='File not found')

            return FileResponse(f'{directory}/{filename}', filename=filename, media_type='application/octet-stream')
        
        @self.app.get('/summaries/{filename}')
        async def download_file(filename: str = Path(...)):
            directory = 'data/summaries'  # Set the directory where the files are stored
            print("hi i've been called summaries download")
            # Validate the requested file against a whitelist if needed
            # whitelist = ['file1.txt', 'file2.pdf']
            # if filename not in whitelist:
            #     raise HTTPException(status_code=404, detail='File not found')

            return FileResponse(f'{directory}/{filename}', filename=filename, media_type='application/octet-stream')
        
        @self.app.get('/transcripts/{filename}')
        async def download_file(filename: str = Path(...)):
            directory = 'data/transcripts'  # Set the directory where the files are stored
            print("hi i've been called transcripts download")
            # Validate the requested file against a whitelist if needed
            # whitelist = ['file1.txt', 'file2.pdf']
            # if filename not in whitelist:
            #     raise HTTPException(status_code=404, detail='File not found')

            return FileResponse(f'{directory}/{filename}', filename=filename, media_type='application/octet-stream')
        
        @self.app.get('/videos/{filename}')
        async def download_file(filename: str = Path(...)):
            directory = 'data/videos'  # Set the directory where the files are stored
            print("hi i've been called videos download")
            # Validate the requested file against a whitelist if needed
            # whitelist = ['file1.txt', 'file2.pdf']
            # if filename not in whitelist:
            #     raise HTTPException(status_code=404, detail='File not found')

            return FileResponse(f'{directory}/{filename}', filename=filename, media_type='application/octet-stream')

        @self.app.get("/OK")
        def health_check():
            return {"message": "alive and well","code":0}
        # for testing purposes testing
        @self.app.get("/stop")
        def stop():
            # self.instance.stop()
            self.server.should_exit = True
            print("exitting...")
    def stop(self):
            # self.instance.stop()
            self.server.should_exit = True
            print("exitting...")
    def start(self):
        self.configure_routes()
        self.server.run()
        

if __name__ == "__main__":
    load_dotenv()
    test = APIWrapper()
    test.start()
    # if(port == None):
    #     port = 8000
    # uvicorn.run(app, host="0.0.0.0", port=int(port))