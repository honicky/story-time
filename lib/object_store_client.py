import boto3
import mimetypes
import os

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