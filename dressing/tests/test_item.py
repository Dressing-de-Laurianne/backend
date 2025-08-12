import os

from django.conf import settings
from django.test import TestCase
from PIL import Image
from rest_framework import status
from rest_framework.test import APIClient

from dressing.models import Item


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
        self.assertTrue(Item.objects.filter(description="Blue denim jeans").exists())

    def test_list_items(self):
        url = "/items/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_dict = response.json()
        self.assertGreaterEqual(response_dict["count"], 1)
        self.assertGreaterEqual(len(response_dict["results"]), 1)

    def test_create_item_with_image_base64(self):
        # Create a simple PNG image in base64
        image_b64 = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAgAAAAICAIAAABLbSncAAAA2ElEQVR4nADIADf/Aodg0zdqnSNEvEHuou80mNERMkPE5K34EgTeIdDFFHsyZrFf4o1wts0jzs69tAxcBYsBXmPOAjcdSCCRyEIh80qv0QEOwim0FwU2ALXXpQTKS69oVey08Q4HoOLJNBdWNbGQ9gPD4C0QBc4YHPzMSM/OCCj3O2ajpaydATcAQLRt8/x7usEgSRjyBN9vzQPU8cwfp2TaAD0QJGdc4PQl0JzyXGtaCNyHGaHtKENs9gCDSO5U7pfCMcIohdv0+8LWH+Wez0ibHwEBAAD//7MbYCE3Rcd8AAAAAElFTkSuQmCC"
        data = {
            "title": "Coat",
            "size": "L",
            "type": "Coat",
            "color": "Beige",
            "description": "Red wool sweater",
            "image": image_b64,
        }

        response = self.client.post("/items/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Item.objects.filter(title="Coat").exists())
        item = Item.objects.get(title="Coat")
        self.assertTrue(item.image.name.endswith(".png"))
        image_path = os.path.join(settings.MEDIA_ROOT, item.image.name)
        self.assertTrue(os.path.exists(image_path))
        with Image.open(image_path) as image:
            self.assertEqual(image.size, (8, 8))
        item.image.delete(save=False)
        self.assertFalse(os.path.exists(image_path))

    def test_update_item(self):
        url = f"/items/{self.item.pk}/"
        data = {
            "title": "T-shirt updated",
            "size": "M",
            "type": "Shirt",
            "color": "White",
            "description": "Updated description",
        }
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.item.refresh_from_db()
        self.assertEqual(self.item.title, "T-shirt updated")
        self.assertEqual(self.item.description, "Updated description")

    def test_partial_update_item(self):
        url = f"/items/{self.item.pk}/"
        data = {
            "description": "Partially updated description",
        }
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.item.refresh_from_db()
        self.assertEqual(self.item.description, "Partially updated description")

    def test_delete_item(self):
        url = f"/items/{self.item.pk}/"
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Item.objects.filter(pk=self.item.pk).exists())
