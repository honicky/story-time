import boto3
import mimetypes
import os
import requests
from typing import Optional


class Boto3Client:
    def __init__(self):
        self.boto3_client = boto3.session.Session(
            aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"],
            aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"],
            region_name="us-east-1",
        )

    def upload_object(self, file_body: bytes, bucket_name: str, key: str, content_type: Optional[str] = None) -> None:
        s3_client = self.boto3_client.resource("s3").Bucket(bucket_name)
        if content_type is None:
            content_type, _ = mimetypes.guess_type(key)
        print(f"Uploading {key} with content type {content_type}")
        s3_client.put_object(Body=file_body, Key=key, ContentType=content_type)

    def upload_from_url(
        self,
        url: str,
        bucket_name: str,
        key_prefix: str,
        target_id: Optional[str] = None,
    ) -> Optional[str]:
        file_name = os.path.basename(url)
        if target_id is not None:
            file_name = insert_image_id(file_name, target_id)

        key = os.path.join(key_prefix, file_name)

        response = requests.get(url)
        if response.status_code == 200:
            self.upload_object(response.content, bucket_name, key)
            print(f"File uploaded to {bucket_name}/{key}")
            return key
        else:
            print(f"Failed to download file from {url}")
            return None

    def get_object(self, bucket_name: str, key: str) -> bytes:
        s3_client = self.boto3_client.resource("s3").Bucket(bucket_name)
        return s3_client.Object(key).get()["Body"].read()


def insert_image_id(url, id):
    base, suffix = url.rsplit(".", 1)
    return f"{base}-{id}.{suffix}"
