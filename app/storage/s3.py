import boto3
from typing import List, Optional
from .base import StorageBackend, Item

class S3StorageBackend(StorageBackend):
    def __init__(self, bucket_name: str, aws_access_key_id: str, aws_secret_access_key: str, region_name: str, endpoint_url: Optional[str]):
        self.bucket_name = bucket_name
        print(f"Initializing S3StorageBackend for bucket: {self.bucket_name} at endpoint: {endpoint_url or 'default AWS'}")
        
        self.s3_client = boto3.client(
            's3',
            endpoint_url=endpoint_url,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=region_name
        )

    def list(self, path: str) -> List[Item]:
        path = path.strip('/')
       
        if path:
            path += '/'
        
        paginator = self.s3_client.get_paginator('list_objects_v2')
       
        page_iterator = paginator.paginate(Bucket=self.bucket_name, Prefix=path, Delimiter='/')
        
        items = []

        
        for page in page_iterator:
            
            if page.get('CommonPrefixes'):
                for prefix in page.get('CommonPrefixes'):
                    if prefix:
                        full_prefix = prefix.get('Prefix')
                        
                        folder_name = full_prefix.replace(path, '', 1).strip('/')
                        items.append(Item(name=folder_name, path=full_prefix.strip('/'), type='folder'))
            
            
            if page.get('Contents'):
                for obj in page.get('Contents'):
                    if obj and not obj.get('Key').endswith('/'): 
                        key = obj.get('Key')
                        file_name = key.replace(path, '', 1)
                        if file_name: 
                            items.append(Item(name=file_name, path=key, type='file'))

        return sorted(items, key=lambda x: (x.type, x.name))