from django.test import RequestFactory
from django.urls import reverse, resolve
from mixer.backend.django import mixer
from django.contrib.auth.models import User, AnonymousUser

from products.views import product_detail
import pytest


@pytest.mark.django_db
class TestViews:
    def test_product_detail_auth(self):
        mixer.blend('products.Product')
        path = reverse('detail', kwargs={'pk': 1})
        request = RequestFactory().get(path)
        request.user = mixer.blend(User)
        response = product_detail(request, pk=1)
        assert response.status_code == 200

    def test_product_detail_unauth(self):
        mixer.blend('products.Product')
        path = reverse('detail', kwargs={'pk': 1})
        request = RequestFactory().get(path)
        request.user = AnonymousUser()
        response = product_detail(request, pk=1)
        assert 'accounts/login' in response.url
