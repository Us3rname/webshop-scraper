
import requests
from requests.exceptions import HTTPError
from requests import Response
import sys

class ApiService:


    # def __init__(self):
    #     return null


    def do_get_request(self, url: str, params: str = None, 
                    headers: dict = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:81.0) Gecko/20100101 Firefox/81.0','charset' : 'utf-8'} 
        ) -> Response:

        try:
            response = requests.get(
                url, 
                headers= headers,
                params=params,
            )

            # If the response was successful, no Exception will be raised
            response.raise_for_status()
        except HTTPError as http_err:
            print(sys.argv[1:])
            print(f'HTTP error occurred: {http_err}')  # Python 3.6
        except Exception as err:
            print(sys.argv[1:])
            print(f'Other error occurred: {err}')  # Python 3.6
        else :
            return response