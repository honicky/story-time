import boto3
import mimetypes
import os
import requests
from typing import Optional


class Boto3Client:
    def __init__(self):
        # These environment variables are stored in the Beam Secrets Manager
        self.boto3_client = boto3.session.Session(
            aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"],
            aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"],
            region_name="us-east-1",
        )

    # def download_objects(self, bucket_name: str, download_path: str) -> None:
    #     s3_client = self.boto3_client.resource("s3").Bucket(bucket_name)

    #     for s3_object in s3_client.objects.all():
    #         filename = os.path.split(s3_object.key)
    #         s3_client.download_file(s3_object.key, f"{download_path}/{filename}")

    def upload_object(self, file_body: bytes, bucket_name: str, key: str) -> None:
        s3_client = self.boto3_client.resource("s3").Bucket(bucket_name)
        mime_type, _ = mimetypes.guess_type(key)
        print(f"Uploading {key} with mime type {mime_type}")
        s3_client.put_object(Body=file_body, Key=key, ContentType=mime_type)

    def upload_from_url(
        self,
        url: str,
        bucket_name: str,
        key_prefix: str,
        target_id: Optional[str] = None,
    ) -> Optional[str]:
        # Get the file name from the URL
        file_name = os.path.basename(url)
        if target_id is not None:
            file_name = insert_image_id(file_name, target_id)

        # Combine the key prefix with the file name
        key = os.path.join(key_prefix, file_name)

        # Download the file from the URL
        response = requests.get(url)
        if response.status_code == 200:
            # Upload the file to S3
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
