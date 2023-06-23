import qrcode
from PIL import Image
from io import BytesIO
import base64
from flask import Flask, send_file
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

app = Flask(__name__)

@app.route("/")
def serve_qrcode():
    text = "http://192.168.1.7/8000/list-directory?directory=material"  # Replace with your desired text
    img = generate_qrcode(text)
    bytes_io = BytesIO()
    img.save(bytes_io, format="PNG")
    bytes_io.seek(0)
    return '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>QR Code</title>
        </head>
        <body>
            <img src="data:image/png;base64,{}" alt="QR Code">
        </body>
        </html>
    '''.format(base64.b64encode(bytes_io.getvalue()).decode())


if __name__ == "__main__":
    app.run()
