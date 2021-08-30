"""
"""
import requests

class Requester():
    def __init__(self, base_url, api_token):
        self._key = api_token
        self._url = base_url

    def _get_headers(self, headers=None):
        header = { "Authorization": f"Bearer {self._key}" }
        if headers:
            header.update(headers)

        return header

    def _get_base_url(self, endpoint):
        return f"{self._url}/{endpoint}"

    def _base_request(self, callback, endpoint, headers=None, **kwargs):
        return callback(self._get_base_url(endpoint), **kwargs,
            headers=self._get_headers(headers))

    def _request_get(self, endpoint, payload={}, headers=None):
        return self._base_request(requests.get, endpoint, headers, params=payload)

    def request_get_paging(self, endpoint, payload={}, headers=None, page=1):
        data = []
        respons = self._request_get(
            endpoint.format(page=page), payload=payload, headers=headers
        )
        data = respons.json()
        if "Link" in respons.headers and 'rel="next"' in respons.headers["Link"]:
            print(respons.headers["Link"])
            respons = self.request_get_paging(
                endpoint, payload=payload, headers=headers, page=page+1
            )
            data.extend(respons)

        return data

    def _request_post(self, endpoint, payload={}, headers=None):
        return self._base_request(requests.post, endpoint, headers, data=payload)

    def _request_delete(self, endpoint, payload={}, headers=None):
        return self._base_request(requests.delete, endpoint, headers, json=payload)

    def _request_put(self, endpoint, payload={}, headers=None):
        return self._base_request(requests.put, endpoint, headers, json=payload)
