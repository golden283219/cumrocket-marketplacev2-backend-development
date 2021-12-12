import pytest
from django.contrib.auth.models import User
from django.urls import reverse

pytestmark = pytest.mark.django_db


def test_sync_view_no_login(client, mocker):
    patched = mocker.patch("blockchain.views.sync_blockchain.delay")

    User.objects.create(username="test", email="test@test.com")
    response = client.get(reverse("sync"))

    patched.assert_not_called()
    assert response.status_code == 401


def test_sync_view_success(client, mocker):
    patched = mocker.patch("blockchain.views.sync_blockchain.delay")

    user = User.objects.create(username="test", email="test@test.com")
    client.force_login(user)
    response = client.get(reverse("sync"))

    patched.assert_called_once()
    assert response.status_code == 200
