#!/usr/bin/env python3

import boto3
import os
from dotenv import load_dotenv
from botocore.client import Config

load_dotenv()

# Replace with your actual R2 values
R2_ACCESS_KEY_ID = os.getenv("CLOUDFLARE_ACCESS_KEYID")
R2_SECRET_ACCESS_KEY = os.getenv("SECRET_ACCESS_KEY")
R2_BUCKET_NAME = os.getenv("R2_BUCKET_NAME")
R2_ENDPOINT_URL = os.getenv("R2_ENDPOINT")

# Create an S3-compatible client
s3 = boto3.client(
    's3',
    aws_access_key_id=R2_ACCESS_KEY_ID,
    aws_secret_access_key=R2_SECRET_ACCESS_KEY,
    endpoint_url=R2_ENDPOINT_URL,
    config=Config(signature_version='s3v4')
)

def upload_user_image(image_path, file_name):
    path_to_upload = f"user_data/uploads/{file_name}"
    
    with open(image_path, "rb") as f:
        response = s3.put_object(
            Bucket=R2_BUCKET_NAME,
            Key=path_to_upload,
            Body=f.read()
        )

if __name__ == "__main__":
    upload_user_image(image_path, file_name)
