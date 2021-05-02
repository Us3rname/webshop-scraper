import io
import gzip
import json
import logging

class S3Service:

    def upload_json_gz(self, s3client, bucket, key, obj, default=None, encoding='utf-8'):

        ''' upload python dict into s3 bucket with gzip archive '''
        inmem = io.BytesIO()
        with gzip.GzipFile(fileobj=inmem, mode='wb') as fh:
            with io.TextIOWrapper(fh, encoding=encoding) as wrapper:
                wrapper.write(json.dumps(
                    obj, ensure_ascii=False, default=default))
        inmem.seek(0)
        s3client.put_object(Bucket=bucket, Body=inmem, Key=key)

    def download_json_gz(self, s3client, bucket, key):
        ''' download gzipped json file from s3 and convert to dict '''
        response = s3client.get_object(Bucket=bucket, Key=key)
        content = response['Body'].read()
        with gzip.GzipFile(fileobj=io.BytesIO(content), mode='rb') as fh:
            return json.load(fh)