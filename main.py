from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel
import qrcode
from PIL import Image
from io import BytesIO
import base64
import os
import cv2
import numpy
from starlette.responses import StreamingResponse
import netifaces
import json
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
def generate_qrcode(text):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(text)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    return img

def save_qrcode_to_bytes(text):
    img = generate_qrcode(text)
    bytes_io = BytesIO()
    img.save(bytes_io, format="PNG")
    bytes_io.seek(0)
    return bytes_io

app = FastAPI()

@app.get("/list-directory")
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
class Attendance(BaseModel):
    user: str
    userId: str
    token: str
    # date: date
@app.post("/attend/")
async def attend(attendance: Attendance):
    #attendence in db
    print(attendance)
    return {"message": f"attendance recorded"}

#this is to test generation of qrcode and conversion to cv2 format, this is not final
#This will be moved into another file, later.
def get_ip():
    addresses = []
    for ifaceName in netifaces.interfaces():
        addresses.append([i['addr'] for i in netifaces.ifaddresses(ifaceName).setdefault(netifaces.AF_INET, [{'addr':'No IP addr'}])])
    return addresses
@app.get("/test")
async def test():
    address = f"{get_ip()[-1][0]}:{port}"
    json_data = {"address": address, "token": "hosted token"}
    json_data = json.dumps(json_data)
    img = numpy.array(generate_qrcode(json_data).convert("RGB"))
    # return img
    cv2.imshow("test",img)
    cv2.waitKey(0)
    # closing all open windows
    cv2.destroyAllWindows()

@app.get("/download")
def download_file(directory: str, file_name: str):
    file_path = "./data/" + directory + '/' + file_name
    if not os.path.exists(file_path):
        print(file_path)
        raise HTTPException(status_code=404, detail="File not found")
    def file_generator():
        with open(file_path, "rb") as file:
            yield from file
    return StreamingResponse(content=file_generator(), media_type="application/pdf")

@app.get("/OK")
def health_check():
    return {"message": "alive and well","code":0}

if __name__ == "__main__":
    port = os.getenv('APP_PORT')
    if(port == None):
        port = 8000
    uvicorn.run(app, host="0.0.0.0", port=int(port))