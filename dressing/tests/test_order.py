from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from dressing.models import Item, Order


class OrderAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.item1 = Item.objects.create(
            title="T-shirt",
            size="M",
            type="Shirt",
            color="White",
            description="White cotton t-shirt",
        )
        self.item2 = Item.objects.create(
            title="Jeans",
            size="L",
            type="Pants",
            color="Blue",
            description="Blue denim jeans",
        )
        self.order = Order.objects.create(status="Pending")
        self.order.items.set([self.item1, self.item2])

    def test_create_order_with_items(self):
        url = "/orders/"
        data = {"status": "Pending", "items": [self.item1.pk, self.item2.pk]}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        order_id = response.json().get("id")
        self.assertTrue(Order.objects.filter(pk=order_id).exists())
        order = Order.objects.get(pk=order_id)
        self.assertEqual(order.items.count(), 2)

    def test_list_orders(self):
        url = "/orders/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_dict = response.json()
        self.assertGreaterEqual(response_dict["count"], 1)
        self.assertGreaterEqual(len(response_dict["results"]), 1)
        # Check items in the first order
        first_order = response_dict["results"][0]
        self.assertIn("items", first_order)
        self.assertGreaterEqual(len(first_order["items"]), 2)

    def test_update_order_items(self):
        url = f"/orders/{self.order.pk}/"
        data = {"status": "Delivered", "items": [self.item1.pk]}
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.order.refresh_from_db()
        self.assertEqual(self.order.status, "Delivered")
        self.assertEqual(self.order.items.count(), 1)
        self.assertEqual(self.order.items.first(), self.item1)

    def test_partial_update_order_items(self):
        url = f"/orders/{self.order.pk}/"
        data = {"items": [self.item2.pk]}
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.order.refresh_from_db()
        self.assertEqual(self.order.items.count(), 1)
        self.assertEqual(self.order.items.first(), self.item2)

    def test_delete_order(self):
        url = f"/orders/{self.order.pk}/"
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Order.objects.filter(pk=self.order.pk).exists())
