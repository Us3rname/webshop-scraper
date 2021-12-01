from datetime import datetime
import boto3
import json
from botocore.exceptions import ClientError
import logging
import io
import gzip

class S3Service : 

    def __init__(self) -> None:
        self.s3_client = boto3.client('s3')
        # self.s3_resource = boto3.resource('s3')

    def getPartitionedFilePath(self, datetime : datetime) :
        return '/dt=' + datetime.strftime('%Y-%m-%d') + '/'

    # def saveJsonFile(self, values, bucket_name, file_path):

    #     try:  
    #         s3object = self.s3_resource.Object(bucket_name, file_path)    
    #         s3object.put(
    #             Body=(bytes(json.dumps(values).encode('UTF-8')))
    #         )
    #     except ClientError as e:
    #         logging.error(e)
    #         return False

    def saveJsonGZFile(self, values, bucket, key, default=None, encoding='utf-8'):
        
        # Add extension
        key += '.gz'
        try:  
            inmem = io.BytesIO()
            with gzip.GzipFile(fileobj=inmem, mode='wb') as fh:
                with io.TextIOWrapper(fh, encoding=encoding) as wrapper:
                    wrapper.write(json.dumps(values, ensure_ascii=False, default=default))
            inmem.seek(0)
            self.s3_client.put_object(Bucket=bucket, Body=inmem, Key=key)
        except ClientError as e:
            logging.error(e)
            return False
