from test.base_case import BaseCase


class TestSignUp(BaseCase):

    def test_sign_up_successful(self):
        test_user_info = {
            "username": "quy_dz_123456",
            "password": "Quy@gotit123"
        }
        status_code, data = self.test_client.post(url="/auth/sign-up", payload=test_user_info)

        assert status_code == 201
        assert data
        assert data["message"] == "User created successfully"
        assert data["user"]["username"] == test_user_info["username"]
        assert type(data["user"]["id"]) is int

    def test_duplicated_username(self):
        test_user_info = {
            "username": "quy_dz_1234567",
            "password": "Quy@gotit123"
        }

        status_code, data = self.test_client.post(url="/auth/sign-up", payload=test_user_info)
        assert status_code == 201

        status_code, data = self.test_client.post(url="/auth/sign-up", payload=test_user_info)

        assert status_code == 400
        assert data
        assert data["message"] == "Duplicated username"

    def test_missing_password(self, init_database):
        test_user_info = {
            "username": "quy_dz_123456",
        }
        status_code, data = self.test_client.post(url="/auth/sign-up", payload=test_user_info)
        assert status_code == 400
        assert data["message"]["password"][0] == "Missing data for required field."


class TestSignIn(BaseCase):

    def setup(self):
        super().setup()
        self.sign_up_user_info = {
            "username": "Quyngao_dz_tqn",
            "password": "Quy@gotit123"
        }

    def test_sign_in_successful(self):
        status_code, data = self.test_client.post(url="/auth/sign-in", payload=self.sign_up_user_info)

        assert status_code == 200
        assert data["access_token"]
        assert type(data["access_token"]) is str

    def test_user_not_found(self):
        payload = self.sign_up_user_info
        payload["username"] = "quy_dz_1234"
        status_code, data = self.test_client.post(url="/auth/sign-in", payload=payload)

        assert status_code == 401
        assert data["message"] == "Unauthorized"

    def test_empty_password(self):
        payload = self.sign_up_user_info
        payload["password"] = ""
        status_code, data = self.test_client.post(url="/auth/sign-in", payload=payload)
        assert status_code == 400
        assert data["message"]["password"][0] == "Length must be between 8 and 40."
