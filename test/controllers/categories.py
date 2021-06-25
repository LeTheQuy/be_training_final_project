import json

from test.base_case import BaseCase


class TestGetCategories(BaseCase):

    def test_get_categories_successful(self, init_database):
        response = self.test_client.get(url="/categories")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["categories"]
        assert type(data["categories"]) == list


class TestGetCategoryById(BaseCase):
    def test_get_category_by_id_successful(self, init_database):
        response = self.test_client.get(url="/categories/1")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["id"]
        assert data["name"]
        assert data["items"]
        assert type(data["items"]) == list

    def test_category_not_found(self, init_database):
        response = self.test_client.get(url="/categories/1000")
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data["message"] == "Invalid category id"

    def test_incorrect_category(self, init_database):
        response = self.test_client.get(url="/categories/abc")
        assert response.status_code == 404
        data = json.loads(response.data)
        assert data["message"] == "404 Not Found: The requested URL was not found on the server. If you entered the " \
                                  "URL manually please check your spelling and try again."
