import pandas as pd
from flatten_json import flatten
import gzip
import json
import boto3

def test() :

    s3 = boto3.resource('s3')
    obj = s3.Object('develop-webshop-scraper-landingzone', 'jumbo/products/dt=2021-12-13/response - 2021-12-13 12:33:43.json.gz')

    with gzip.GzipFile(fileobj=obj.get()["Body"]) as f:
    # with open('lib/lambdaStack/src/test.json', 'rb') as f:
        file_content = f.read()        
        my_json = file_content.decode('utf8')
        # print(my_json)
        data = json.loads(my_json)
        dic_flattened = pd.json_normalize(data
        , record_path=['products', 'data'],
        # errors='ignore'
        )
        df = pd.DataFrame(dic_flattened)
        print(df.head())
    # df.dropna(subset = ["id"], inplace=True)
        df.to_parquet(path="output.parquet")

    # if page == 0 :
        df.to_csv('output - {}.csv'.format('jumbo'))                    
    # else :    
    #     df.to_csv('output - {}.csv'.format(category), mode='a', header=False)

if __name__ == "__main__":    
    test()    