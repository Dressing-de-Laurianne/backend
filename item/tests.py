from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from .models import Item


class ItemAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.client.login(username="admin", password="admin")
        self.item = Item.objects.create(
            title="T-shirt",
            size="M",
            type="Shirt",
            color="White",
            description="White cotton t-shirt",
        )

    def test_create_item(self):
        data = {
            "title": "Jeans",
            "size": "M",
            "type": "Pants",
            "color": "Blue",
            "description": "Blue denim jeans",
        }

        response = self.client.post("/items/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Item.objects.count(), 2)
