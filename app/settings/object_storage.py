import os
from botocore.exceptions import ClientError
import boto3
import logging

from app.settings import get_settings
from fastapi import BackgroundTasks, File, UploadFile

FILE_DESTINATION = "app/static/images"

logger = logging.getLogger(__name__)
s3 = boto3.client(
    service_name            = "s3", 
    aws_access_key_id       = get_settings().OBJECT_STORAGE_ACCESS_KEY,
    aws_secret_access_key   = get_settings().OBJECT_STORAGE_SECRET_KEY,
    region_name             = get_settings().OBJECT_STORAGE_REGION,
    endpoint_url            = f"https://{get_settings().OBJECT_STORAGE_ENDPOINT_PUBLIC}"
)

def upload_file_to_bucket(file_obj, bucket, folder, object_name=None):
    """Upload a file to an S3 bucket
    :param file_obj: File to upload
    :param bucket: Bucket to upload to
    :param folder: Folder to upload to
    :param object_name: S3 object name. If not specified then FILE_DESTINATION is used
    :return: True if file was uploaded, else False
    """
    print("buckets ->", s3.list_buckets())
    print(type(file_obj))
    if object_name is None:
        object_name = FILE_DESTINATION
    # Upload the file
    try:
        response = s3.put_object(Bucket="generated", Key=f"{object_name}", Body=file_obj)
    except ClientError as e:
        logging.error(e)
        return False
