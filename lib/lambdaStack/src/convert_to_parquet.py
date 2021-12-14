import pandas as pd
import gzip
import json
import boto3
import os 
from s3_service import S3Service
from datetime import datetime

def handler(event, context):

    if 'Records' not in event:
        return None

    if len(event['Records']) <= 0:
        return None

    convert(event)

def convert(event):  

    s3 = boto3.resource('s3')
    bucket_name = os.environ['raw_zone_bucket_name']    
    s3Service = S3Service()

    for record in event['Records']:
        obj = s3.Object(record['s3']['bucket']['name'], record['s3']['object']['key'])

        with gzip.GzipFile(fileobj=obj.get()["Body"]) as f:
            file_content = f.read()        
            my_json = file_content.decode('utf8')

            data = json.loads(my_json)

            dic_flattened = pd.json_normalize(data
            , record_path=['products', 'data'],
            )
            df = pd.DataFrame(dic_flattened)
            print(df.head())

            parquetData = df.to_parquet()            
            file_path = 'jumbo/products' + s3Service.getPartitionedFilePath(datetime.today())
            file_name = 'response - ' + datetime.today().strftime('%Y-%m-%d %H:%M:%S') + '.json'
            
            s3Service.saveGZFile(parquetData, bucket_name, file_path + file_name) 