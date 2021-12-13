import pandas as pd
import gzip
import json
import boto3
import os 

def handler(event, context):

    if 'Records' not in event:
        return None

    if len(event['Records']) <= 0:
        return None

    convert(event)

def convert(event):  

    s3 = boto3.resource('s3')
    bucket_name = os.environ['bucket_name']

    for record in event['Records']:
        obj = s3.Object(bucket_name, record['s3']['object']['key'])

        with gzip.GzipFile(fileobj=obj.get()["Body"]) as f:
            file_content = f.read()        
            my_json = file_content.decode('utf8')

            data = json.loads(my_json)
            dic_flattened = pd.json_normalize(data
            , record_path=['products', 'data'],
            # errors='ignore'
            )
            df = pd.DataFrame(dic_flattened)
            print(df.head())
        # df.dropna(subset = ["id"], inplace=True)
            # df.to_parquet(path="output.parquet")

        # if page == 0 :
            # df.to_csv('output - {}.csv'.format('jumbo'))