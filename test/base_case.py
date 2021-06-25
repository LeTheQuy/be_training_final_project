import json

from test.conftest import client


class TestClient:
    def __init__(self, flask_client):
        self.client = client
        self.headers = {"Content-Type": "application/json"}

    def update_access_token_to_header(self, access_token):
        headers = self.headers
        if access_token:
            headers["Authorization"] = access_token
        return headers

    def post(self, url, payload, access_token=None):
        data = json.dumps(payload)
        response = self.client.post(path=url, headers=self.update_access_token_to_header(access_token), data=data)
        return response.status_code, json.loads(response.data)

    def put(self, url, payload, access_token=None):
        data = json.dumps(payload)
        response = self.client.put(path=url, headers=self.update_access_token_to_header(access_token), data=data)
        return response.status_code, json.loads(response.data)

    def delete(self, url, payload=None, access_token=None):
        data = json.dumps(payload)
        response = self.client.delete(path=url, headers=self.update_access_token_to_header(access_token), data=data)
        return response.status_code, json.loads(response.data)

    def get(self, url, payload=None, access_token=None):
        data = json.dumps(payload)
        response = self.client.get(path=url, headers=self.update_access_token_to_header(access_token), data=data)
        return response.status_code, json.loads(response.data)


class BaseCase:
    def setup(self):
        self.test_client = TestClient(client)

    def teardown(self):
        pass
