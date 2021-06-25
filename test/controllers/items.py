from test.base_case import BaseCase


class TestGetLatestAddedItems(BaseCase):
    def test_get_latest_with_items_per_page_successful(self, init_database):
        status_code, data = self.test_client.get(url="/items?order=newest&items_per_page=4")
        assert status_code == 200
        assert type(data["items"]) == list
        assert len(data["items"]) == 4
        for item in data["items"]:
            assert item["id"]
            assert item["title"]
            assert item["description"]
            assert item["category"]["id"]
            assert item["category"]["name"]

    def test_get_all_items_without_items_per_page_param_successful(self, init_database):
        status_code, data = self.test_client.get(url="items")
        assert status_code == 200
        assert data["items"]
        assert type(data["items"]) == list
        for item in data["items"]:
            assert item["id"]
            assert item["title"]
            assert item["description"]
            assert item["category"]["id"]
            assert item["category"]["name"]

    def test_invalid_order_param(self, init_database):
        status_code, data = self.test_client.get(url="items?order=oldest&items_per_page=4")
        assert status_code == 400
        assert data["message"]["order"][0] == "Must be one of: newest."


class TestGetItemsByCategoryId(BaseCase):
    def test_get_latest_with_items_per_page_successful(self, init_database):
        page = 1
        item_per_page = 20
        status_code, data = self.test_client.get(url=f"/categories/1/items?page={page}&items_per_page={item_per_page}")
        assert status_code == 200
        assert data["items"]
        assert len(data["items"]) <= item_per_page
        assert data["current_page"] == page
        assert type(data["total_items"]) is int
        assert data["items_per_page"] == item_per_page
        assert type(data["items"]) == list
        for item in data["items"]:
            assert item["id"]
            assert item["title"]
            assert item["description"]
            assert item["category"]["id"]
            assert item["category"]["name"]

    def test_category_not_found(self, init_database):
        page = 1
        item_per_page = 20
        status_code, data = self.test_client.get(
            url=f"/categories/100/items?page={page}&items_per_page={item_per_page}")
        assert status_code == 400
        assert data["message"] == "Invalid category id"

    def test_invalid_items_per_page(self, init_database):
        page = 1
        item_per_page = "abc"
        status_code, data = self.test_client.get(url=f"/categories/1/items?page={page}&items_per_page={item_per_page}")
        assert status_code == 400
        assert data["message"]["items_per_page"][0] == "Not a valid integer."


class TestGetItemDetail(BaseCase):
    def test_get_item_detail_without_authorization_successful(self, init_database):
        status_code, data = self.test_client.get(url=f"/categories/1/items/1")
        assert status_code == 200
        assert type(data["id"]) is int
        assert data["title"]
        assert data["description"]
        assert data["category"]["id"]
        assert data["category"]["name"]
        assert data["editable"] is False

    def test_get_editable_item_detail_successful(self, init_database, login_default_user):
        status_code, data = self.test_client.get(url=f"/categories/1/items/1", access_token=login_default_user)
        assert status_code == 200
        assert type(data["id"]) is int
        assert data["title"]
        assert data["description"]
        assert data["category"]["id"]
        assert data["category"]["name"]
        assert data["editable"] is True

    def test_item_not_found(self, init_database, login_default_user):
        status_code, data = self.test_client.get(url=f"/categories/1/items/1000")
        assert status_code == 400
        assert data["message"] == "Invalid item id"


class TestAddItem(BaseCase):
    def test_add_item_successful(self, init_database, login_default_user):
        item_info = {
            "title": "Big Baby",
            "description": "Quy dzzzzzzzzzz   ",
        }
        category_id = 1
        status_code, data = self.test_client.post(url=f"/categories/{category_id}/items",
                                                  payload=item_info,
                                                  access_token=login_default_user)
        assert status_code == 201
        assert data["message"] == "Item added"
        assert data["item"]["title"] == item_info["title"].lower().strip()
        assert data["item"]["description"] == item_info["description"].strip()
        assert data["item"]["category"]["id"] == category_id
        assert data["item"]["category"]["name"]

    def test_duplicated_item(self, init_database, login_default_user):
        item_info = {
            "title": "Big Baby",
            "description": "Quy dzzzzzzzzzz   ",
        }
        category_id = 1
        status_code, data = self.test_client.post(url=f"/categories/{category_id}/items",
                                                  payload=item_info,
                                                  access_token=login_default_user)
        assert status_code == 201

        status_code, data = self.test_client.post(url=f"/categories/{category_id}/items",
                                                  payload=item_info,
                                                  access_token=login_default_user)

        assert status_code == 400
        assert data["message"] == "Duplicated item title"

    def test_add_item_without_user_authorization(self, init_database):
        item_info = {
            "title": "Big Baby",
            "description": "Quy dzzzzzzzzzz   ",
        }
        category_id = 1
        status_code, data = self.test_client.post(url=f"/categories/{category_id}/items", payload=item_info)

        assert status_code == 401
        assert data["message"] == "Unauthorized"


class TestUpdateItem(BaseCase):
    def test_edit_item_successful(self, init_database, login_default_user):
        updated_item_info = {
            "title": "Big Baby",
            "description": "Quy dzzzzzzzzzz",
            "category_id": 2
        }

        status_code, data = self.test_client.put(url=f"/categories/1/items/1",
                                                 payload=updated_item_info,
                                                 access_token=login_default_user)

        assert status_code == 200
        assert data["message"] == "Item updated"
        assert data["item"]["title"] == updated_item_info["title"].lower().strip()
        assert data["item"]["description"] == updated_item_info["description"].strip()
        assert data["item"]["category"]["id"] == updated_item_info["category_id"]
        assert data["item"]["category"]["name"]

    def test_permission_denied(self, init_database):
        updated_item_info = {
            "title": "Big Baby",
            "description": "Quy dzzzzzzzzzz",
            "category_id": 2
        }
        sign_up_new_user_info = {
            "username": "quy_dz_123456",
            "password": "Quy@gotit123"
        }
        status_code, data = self.test_client.post(url="/auth/sign-up", payload=sign_up_new_user_info)
        assert status_code == 201

        status_code, data = self.test_client.post(url="/auth/sign-in", payload=sign_up_new_user_info)
        assert status_code == 200

        status_code, data = self.test_client.put(url=f"/categories/1/items/1", payload=updated_item_info,
                                                 access_token=data["access_token"])

        assert status_code == 403
        assert data["message"] == "This item is not editable by yourself"

    def test_new_category_not_found(self, init_database, login_default_user):
        updated_item_info = {
            "title": "Big Baby",
            "description": "Quy dzzzzzzzzzz",
            "category_id": 10000
        }

        status_code, data = self.test_client.put(url=f"/categories/1/items/1",
                                                 payload=updated_item_info,
                                                 access_token=login_default_user)

        assert status_code == 400
        assert data["message"] == "Invalid new category id"


class TestDeleteItem(BaseCase):
    def test_delete_item_successful(self, init_database, login_default_user):
        status_code, data = self.test_client.delete(url=f"/categories/1/items/1",
                                                    access_token=login_default_user)
        assert status_code == 200
        assert data["message"] == "Item deleted"

    def test_invalid_access_token(self, init_database, login_default_user):
        invalid_access_token = login_default_user + "xxx"
        status_code, data = self.test_client.delete(url=f"/categories/1/items/1",
                                                    access_token=invalid_access_token)
        assert status_code == 401
        assert data["message"] == "Unauthorized"

    def test_item_and_category_dont_match(self, init_database, login_default_user):
        status_code, data = self.test_client.delete(url=f"/categories/1/items/12",
                                                    access_token=login_default_user)
        assert status_code == 400
        assert data["message"] == "Category and item don't match"
