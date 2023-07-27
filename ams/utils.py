import base64
import io
import json
import os

import cv2
import numpy as np
import qrcode
from minio import Minio
from PIL import Image

# from minio.error import ResponseError

client = Minio(
    "minio:9001",
    access_key=os.environ.get("MINIO_ACCESS_KEY"),
    secret_key=os.environ.get("MINIO_SECRET_KEY"),
    secure=False,
)

bucket_name: str = os.environ.get("MINIO_BUCKET_NAME")
policy: dict = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {"AWS": ["*"]},
            "Action": ["s3:GetObject"],
            "Resource": [f"arn:aws:s3:::{bucket_name}/*"],
        },
        {
            "Effect": "Allow",
            "Principal": {"AWS": ["*"]},
            "Action": ["s3:DeleteObject", "s3:PutObject"],
            "Resource": [f"arn:aws:s3:::{bucket_name}/*"],
            "Condition": {"StringEquals": {"aws:username": ["access-key-value"]}},
        },
    ],
}


def upload_image_to_minio(image_bytes: bytes, fileName: str, content_type: str = "application/octet-stream") -> str:

    object_name: str = fileName

    print(object_name)

    # Create bucket if it doesn't exist
    if not client.bucket_exists(bucket_name):
        client.make_bucket(bucket_name)

        # Set the policy
        client.set_bucket_policy(bucket_name, json.dumps(policy))

    # Upload the image
    client.put_object(
        bucket_name, object_name, io.BytesIO(image_bytes), len(image_bytes), content_type= content_type
    )

    return f"http://127.0.0.1:9001/{bucket_name}/{object_name}"


def image_to_bytes(image) -> bytes:
    """qrcode.image.pil.PilImage to byte"""

    byte_stream = io.BytesIO()

    image.save(byte_stream, format="PNG")

    byte_array = byte_stream.getvalue()

    return byte_array


def generate_qr_image(user_data, firstName):

    qr_image = qrcode.make(user_data)
    image_bytes = image_to_bytes(qr_image)
    image_url = upload_image_to_minio(image_bytes, firstName + ".png")

    return image_url


def decode_base64_qrimage_data(base64_qrimage):

    detector = cv2.QRCodeDetector()

    bytes_data = base64.b64decode(base64_qrimage)
    # image = cv2.imread("qr_code.png")

    np_image = cv2.imdecode(np.frombuffer(bytes_data, dtype=np.uint8), cv2.IMREAD_COLOR)

    data, vertices_arr, binary_decode = detector.detectAndDecode(np_image)

    return data
