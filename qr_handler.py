import qrcode
from PIL import Image
from io import BytesIO
import os
import json
import numpy
import cv2
from dotenv import load_dotenv
from utils import get_ip
class QrHandler():
    def __init__(self):
        self.port = os.getenv('PORT')
    def generate_qrcode(self,text):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=1,
        )
        qr.add_data(text)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        return img

    def save_qrcode_to_bytes(self,text):
        img = self.generate_qrcode(text)
        bytes_io = BytesIO()
        img.save(bytes_io, format="PNG")
        bytes_io.seek(0)
        return bytes_io

    def generate_qr_endpoint(self,token="token"):
        address = f"{get_ip()[-1][0]}:{self.port}/"
        json_data = {"address": address, "token": token}
        json_data = json.dumps(json_data)
        img = numpy.array(self.generate_qrcode(json_data).convert("RGB"))
        return img

    def test_gen(self):
        image = self.generate_qr_endpoint()
        cv2.imshow("test",image)
        cv2.waitKey(0)
        # closing all open windows
        cv2.destroyAllWindows()

if __name__ == "__main__":
    load_dotenv()
    test = QrHandler()
    test.test_gen()