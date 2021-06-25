import json

from test.base_case import BaseCase


class TestSignUp(BaseCase):

    def test_sign_up_successful(self, init_database):
        test_user_info = {
            "username": "quy_dz_123456",
            "password": "Quy@gotit123"
        }
        response = self.test_client.post(url="/auth/sign-up", payload=test_user_info)

        assert response.data
        assert response.status_code == 201

        data = json.loads(response.data)
        assert data["message"] == "User created successfully"
        assert data["user"]["username"] == test_user_info["username"]
        assert type(data["user"]["id"]) is int

    def test_duplicated_username(self, init_database):
        test_user_info = {
            "username": "quy_dz_123456",
            "password": "Quy@gotit123"
        }

        response = self.test_client.post(url="/auth/sign-up", payload=test_user_info)
        assert response.status_code == 201

        response = self.test_client.post(url="/auth/sign-up", payload=test_user_info)

        assert response.status_code == 400
        assert response.data
        data = json.loads(response.data)
        assert data["message"] == "Duplicated username"

    def test_missing_password(self, init_database):
        test_user_info = {
            "username": "quy_dz_123456",
        }
        response = self.test_client.post(url="/auth/sign-up", payload=test_user_info)
        assert response.status_code == 400
        assert response.data
        data = json.loads(response.data)
        assert data["message"]["password"][0] == "Missing data for required field."


class TestSignIn(BaseCase):

    def setup(self):
        super().setup()
        self.sign_up_user_info = {
            "username": "quy_dz_123456",
            "password": "Quy@gotit123"
        }
        response = self.test_client.post(url="/auth/sign-up", payload=self.sign_up_user_info)
        assert response.status_code == 201

    def test_sign_in_successful(self, init_database):
        response = self.test_client.post(url="/auth/sign-in", payload=self.sign_up_user_info)

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["access_token"]
        assert type(data["access_token"]) is str

    def test_user_not_found(self, init_database):
        payload = self.sign_up_user_info
        payload["username"] = "quy_dz_1234"
        response = self.test_client.post(url="/auth/sign-in", payload=payload)

        assert response.status_code == 401
        data = json.loads(response.data)
        assert data["message"] == "Unauthorized"

    def test_empty_password(self, init_database):
        payload = self.sign_up_user_info
        payload["password"] = ""
        response = self.test_client.post(url="/auth/sign-in", payload=payload)
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data["message"]["password"][0] == "Length must be between 8 and 40."
