from datetime import timedelta

import pytest


@pytest.fixture(autouse="session")
def accesskey_lifetime(settings):
    settings.SIMPLE_JWT = {"ACCESS_TOKEN_LIFETIME": timedelta(minutes=5), "REFRESH_TOKEN_LIFETIME": timedelta(hours=1)}


@pytest.mark.django_db
class TestToken:
    def test_generate_token(self, user, client):
        """アクセスキーとリフレッシュ用のキーが取得できることを確認"""
        response = client.post("/token/", {"username": "test", "password": "p@ssw0rd"})
        assert response.status_code == 200
        assert "access" in response.data
        assert "refresh" in response.data

    @pytest.mark.parametrize("key_type", ["access", "refresh"])
    def test_generated_token_verify(self, user, client, key_type):
        """アクセスキーとリフレッシュ用のキーが有効であることを確認"""
        response = client.post("/token/", {"username": "test", "password": "p@ssw0rd"})
        accesskey = response.data[key_type]
        response = client.post("/token/verify/", {"token": accesskey})
        assert response.status_code == 200

    def test_refresh_key(self, user, client):
        """リフレッシュ用のキーを利用し有効であることを確認"""
        response = client.post("/token/", {"username": "test", "password": "p@ssw0rd"})
        refreshkey = response.data["refresh"]
        response = client.post("/token/refresh/", {"refresh": refreshkey})
        assert response.status_code == 200
        assert "access" in response.data

    def test_authenticate(self, user, client):
        """アクセスキーを利用してアクセスできることを確認"""
        response = client.post("/token/", {"username": "test", "password": "p@ssw0rd"})
        accesskey = response.data["access"]
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {accesskey}")
        response = client.get("/api/v1/user/")
        assert response.status_code == 200

    @pytest.mark.freeze_time("2022-04-01T00:00:00")
    def test_accesskey_lifetime(self, user, client, freezer):
        """アクセスキーの有効期限をチェック"""
        response = client.post("/token/", {"username": "test", "password": "p@ssw0rd"})
        accesskey = response.data["access"]
        refreshkey = response.data["refresh"]

        freezer.move_to("2022-04-01T00:05:01")
        response = client.post("/token/verify/", {"token": accesskey})
        assert response.status_code == 401

        freezer.move_to("2022-04-01T01:00:01")
        response = client.post("/token/verify/", {"token": refreshkey})
        assert response.status_code == 401
