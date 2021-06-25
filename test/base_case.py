import json

from test.conftest import client


class TestClient:
    def __init__(self, flask_client):
        self.client = client
        self.headers = {"Content-Type": "application/json"}

    def post(self, url, payload):
        data = json.dumps(payload)
        return self.client.post(path=url, headers=self.headers, data=data)

    def get(self, url, payload=None):
        data = json.dumps(payload)
        return self.client.get(path=url, headers=self.headers, data=data)


class BaseCase:
    def setup(self):
        self.test_client = TestClient(client)

    def teardown(self):
        pass
