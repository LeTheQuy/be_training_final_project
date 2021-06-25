from test.conftest import TestClient, client


class BaseCase:
    def setup(self):
        self.test_client = TestClient(client)

    def teardown(self):
        pass
