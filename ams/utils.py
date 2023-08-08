import base64
import io
import uuid

import cv2
import numpy as np
import qrcode
from fileupload.uploader import ObjectUploaderFactory


def upload_image_to_minio(
    image_bytes: bytes, fileName: str, content_type: str = "application/octet-stream"
) -> str:

    uploader = ObjectUploaderFactory().generate()
    uploader.upload_object(image_bytes, fileName, content_type)


def image_to_bytes(image) -> bytes:
    """qrcode.image.pil.PilImage to byte"""

    byte_stream = io.BytesIO()

    image.save(byte_stream, format="PNG")

    byte_array = byte_stream.getvalue()

    return byte_array


def generate_qr_image(user_data, firstName):

    qr_image = qrcode.make(user_data)
    image_bytes = image_to_bytes(qr_image)
    random_4digit: str = str(uuid.uuid4().fields[-1])[:4]
    image_url = upload_image_to_minio(image_bytes, firstName + random_4digit + ".png")

    return image_url


def decode_base64_qrimage_data(base64_qrimage):

    detector = cv2.QRCodeDetector()

    bytes_data = base64.b64decode(base64_qrimage)

    np_image = cv2.imdecode(np.frombuffer(bytes_data, dtype=np.uint8), cv2.IMREAD_COLOR)

    data, vertices_arr, binary_decode = detector.detectAndDecode(np_image)

    return data
