import pathlib
import boto3
from django.conf import settings
import time


# function to upload a file to s3
# key is the file name in s3
# file_path is the full path to the local file ex.  settings.SITE_ROOT+'/scopes/d_scope.txt'
def download_from_s3(bucket_name, key, file_path, region):
    pathlib.Path(file_path).parent.mkdir(parents=True, exist_ok=True) 
    open(file_path, 'w+') #create if not there
    resource = boto3.resource(
    's3',
    region_name=region,
    aws_access_key_id=settings.AWS_ACCESS_KEY,
    aws_secret_access_key=settings.AWS_SECRET_KEY,
    )
    my_bucket = resource.Bucket(bucket_name)
    my_bucket.download_file(key, file_path)
    #print(open(file_path).read())  
    return file_path

def upload_to_s3(bucket_name, key, file_path, region):
    #upload to s3 function here
    resource = boto3.resource(
    's3',
    region_name=region,
    aws_access_key_id=settings.AWS_ACCESS_KEY,
    aws_secret_access_key=settings.AWS_SECRET_KEY,
    )
    my_bucket = resource.Bucket(bucket_name)
    my_bucket.upload_file(file_path, key)    
    
 
def generate_unique_timestamp():
    current_time = time.time()
    milliseconds = round(current_time * 1000)
    timestamp = f"{time.strftime('%Y%m%d-%H%M%S', time.localtime(current_time))}-{milliseconds}"
    return timestamp