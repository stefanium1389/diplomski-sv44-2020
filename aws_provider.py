import os
import boto3
from botocore.exceptions import NoCredentialsError
from cloud_provider import CloudProvider

class AWSProvider(CloudProvider):
    def __init__(self, config):
        self.s3 = boto3.client('s3', 
                               aws_access_key_id=config['aws']['access_key_id'],
                               aws_secret_access_key=config['aws']['secret_access_key'])
        self.bucket_name = config['aws']['bucket_name']

    def upload_file(self, file_path, destination):
        try:
            if destination == '':
                destination = file_path
            self.s3.upload_file(file_path, self.bucket_name, destination)
            print("Upload Successful")
        except FileNotFoundError:
            print("The file was not found")
        except NoCredentialsError:
            print("Credentials not available")

    def download_file(self, source, destination):
        try:
            if destination == '':
                destination = source
            if os.path.isdir(destination):
                destination = os.path.join(destination, source.split('/')[-1])
            self.s3.download_file(self.bucket_name, source, destination)
            print("Download Successful")
        except FileNotFoundError:
            print("The file was not found")
        except NoCredentialsError:
            print("Credentials not available")
    
    def list_files(self):
        try:
            response = self.s3.list_objects_v2(Bucket=self.bucket_name)
            files = []
            if 'Contents' in response:
                for obj in response['Contents']:
                    files.append(obj['Key'])
                return files
        except NoCredentialsError:
            print("Credentials not available")
