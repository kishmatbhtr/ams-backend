import io
import json
import os
import uuid

import qrcode
from minio import Minio

# from minio.error import ResponseError

client = Minio(
    "minio:9000",
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


def upload_image_to_minio(image_bytes: bytes, fileName: str) -> str:

    random_4digit: str = str(uuid.uuid4().fields[-1])[:4]
    object_name: str = fileName + "-" + random_4digit + ".png"

    print(object_name)

    # Create bucket if it doesn't exist
    if not client.bucket_exists(bucket_name):
        client.make_bucket(bucket_name)

        # Set the policy
        client.set_bucket_policy(bucket_name, json.dumps(policy))

    # Upload the image
    client.put_object(
        bucket_name, object_name, io.BytesIO(image_bytes), len(image_bytes)
    )

    return f"http://127.0.0.1:9000/{bucket_name}/{object_name}"


def image_to_bytes(image) -> bytes:
    """qrcode.image.pil.PilImage to byte"""

    byte_stream = io.BytesIO()

    image.save(byte_stream, format="PNG")

    byte_array = byte_stream.getvalue()

    return byte_array


def generate_qr_image(user_data, firstName):

    qr_image = qrcode.make(user_data)
    image_bytes = image_to_bytes(qr_image)
    image_url = upload_image_to_minio(image_bytes, firstName)

    return image_url
