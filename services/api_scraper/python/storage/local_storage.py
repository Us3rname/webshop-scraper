import io
import gzip
import json
import logging
import os
import errno


class LocalStorageService:

    def upload_json_gz(self, root_dir, file_location, obj, default=None, encoding='utf-8'):

        ''' upload python dict into s3 bucket with gzip archive '''
        # inmem = io.BytesIO()
        # with gzip.GzipFile(fileobj=inmem, mode='wb') as fh:
        #     with io.TextIOWrapper(fh, encoding=encoding) as wrapper:
        #         wrapper.write(json.dumps(
        #             obj, ensure_ascii=False, default=default))
        # inmem.seek(0)
        
        if not os.path.exists(os.path.dirname(root_dir + file_location)):
            try:
                os.makedirs(os.path.dirname(root_dir + file_location))
            except OSError as exc: # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise


        file = open(root_dir + file_location, "w", encoding='utf-8')
        file.write(obj)
        file.close()



    def download_json_gz(self, s3client, bucket, key):
        ''' download gzipped json file from s3 and convert to dict '''
        response = s3client.get_object(Bucket=bucket, Key=key)
        content = response['Body'].read()
        with gzip.GzipFile(fileobj=io.BytesIO(content), mode='rb') as fh:
            return json.load(fh)