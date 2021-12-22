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
    s3Service = S3Service()
    for record in event['Records']:
        key = record['s3']['object']['key']
        obj = s3.Object(record['s3']['bucket']['name'], key)

        with gzip.GzipFile(fileobj=obj.get()["Body"]) as f:
            file_content = f.read()        
            my_json = file_content.decode('utf8')

            json_data = json.loads(my_json)
            
            splitted_key_path = key.split("/")
            webshop = splitted_key_path[0]
            
            data = None
            record_path = None
            
            print('Webshop', webshop)
            
            if (webshop == 'ah') :
                data = json_data[0]
                record_path = ['products']
            elif (webshop == 'jumbo') :
                data = json_data
                record_path = ['products', 'data']
            else :
                raise Exception('Webshop is unknown')

            store_parquet_file(s3Service, data, record_path, webshop)                           

def store_parquet_file(s3Service, data, record_path, webshop) :
    dic_flattened = pd.json_normalize(data, record_path)
    df = pd.DataFrame(dic_flattened)
    print(df.head())

    file_path = 's3://develop-webshop-scraper-rawzone/' + webshop + '/products' + s3Service.getPartitionedFilePath(datetime.today())
    file_name = 'response - ' + datetime.today().strftime('%Y-%m-%d %H:%M:%S') + '.parquet'
    
    df.to_parquet(file_path + file_name, compression='gzip') 