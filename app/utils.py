import requests
import time


class MakeRequestSync:
    @staticmethod
    def make_request_post(url, headers, data):
        """
        Make a request post
        """
        retry = 5
        while True:
            try:
                response = requests.post(url, headers=headers, json=data)
                return response
            except Exception as e:
                retry -= 1
                if retry == 0:
                    return e
                time.sleep(1.2)
                continue

    @staticmethod
    def make_request_post_with_params(url, headers, data, params):
        """
        Make a request post with params
        """
        retry = 5
        while True:
            try:
                response = requests.post(url, headers=headers, json=data, params=params)
                return response
            except Exception as e:
                retry -= 1
                if retry == 0:
                    return e
                time.sleep(1.2)
                continue