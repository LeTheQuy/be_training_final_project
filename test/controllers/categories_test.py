from test.base_case import BaseCase


class TestGetCategories(BaseCase):

    def test_get_categories_successful(self):
        status_code, data = self.test_client.get(url="/categories")
        assert status_code == 200
        assert data["categories"]
        assert type(data["categories"]) == list


class TestGetCategoryById(BaseCase):
    def test_get_category_by_id_successful(self):
        status_code, data = self.test_client.get(url="/categories/1")
        assert status_code == 200
        assert data["id"]
        assert data["name"]
        assert data["items"]
        assert type(data["items"]) == list

    def test_category_not_found(self):
        status_code, data = self.test_client.get(url="/categories/1000")
        assert status_code == 400
        assert data["message"] == "Invalid category id"

    def test_incorrect_category(self):
        status_code, data = self.test_client.get(url="/categories/abc")
        assert status_code == 404
        assert data["message"] == "404 Not Found: The requested URL was not found on the server. If you entered the " \
                                  "URL manually please check your spelling and try again."
