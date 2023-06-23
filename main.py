from fastapi import FastAPI
import qrcode
from PIL import Image
from io import BytesIO
import base64
import os
import cv2
import numpy
from starlette.responses import StreamingResponse

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
async def list_directory(directory: str):
    available_directories = [
        "material", # lecture material
        "transcripts", # Ai based lecture transcript
        "summaries", # Ai summerization of transcripts
        "videos" # the recorded video
    ]
    if(directory in available_directories):
        try:
            files = os.listdir("data/" + directory)
            return {"files": files}
        except FileNotFoundError:
            return {"message": "error: recreate directories"}
    else:
        return {"message": "error: wrong directory name"}

@app.get("/attend/")
async def attend(user: str, token: str):
    #attendence in db
    return {"message": f"attendance recorded"}

#this is to test generation of qrcode and conversion to cv2 format, this is not final
@app.get("/test/")
async def test(fun: str):
    img = numpy.array(generate_qrcode(fun).convert("RGB"))
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
    