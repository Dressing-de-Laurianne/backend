from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from dressing.models import Item, Outfit


class OutfitAPITestCase(TestCase):
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
        self.outfit = Outfit.objects.create(
            title="Casual Outfit", description="A casual combination"
        )
        self.outfit.items.set([self.item1, self.item2])

    def test_create_outfit_with_items(self):
        url = "/outfits/"
        data = {
            "title": "Sporty Outfit",
            "description": "For sports activities",
            "items": [self.item1.pk, self.item2.pk],
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        outfit_id = response.json().get("id")
        self.assertTrue(Outfit.objects.filter(pk=outfit_id).exists())
        outfit = Outfit.objects.get(pk=outfit_id)
        self.assertEqual(outfit.items.count(), 2)

    def test_list_outfits(self):
        url = "/outfits/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_dict = response.json()
        self.assertGreaterEqual(response_dict["count"], 1)
        self.assertGreaterEqual(len(response_dict["results"]), 1)
        # Check items in the first outfit
        first_outfit = response_dict["results"][0]
        self.assertIn("items", first_outfit)
        self.assertGreaterEqual(len(first_outfit["items"]), 2)
        self.assertIn("title", first_outfit)
        self.assertIn("description", first_outfit)

    def test_update_outfit_items(self):
        url = f"/outfits/{self.outfit.pk}/"
        data = {
            "title": "Updated Outfit",
            "description": "Updated description",
            "items": [self.item1.pk],
        }
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.outfit.refresh_from_db()
        self.assertEqual(self.outfit.title, "Updated Outfit")
        self.assertEqual(self.outfit.description, "Updated description")
        self.assertEqual(self.outfit.items.count(), 1)
        self.assertEqual(self.outfit.items.first(), self.item1)

    def test_partial_update_outfit_items(self):
        url = f"/outfits/{self.outfit.pk}/"
        data = {"items": [self.item2.pk]}
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.outfit.refresh_from_db()
        self.assertEqual(self.outfit.items.count(), 1)
        self.assertEqual(self.outfit.items.first(), self.item2)

    def test_delete_outfit(self):
        url = f"/outfits/{self.outfit.pk}/"
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Outfit.objects.filter(pk=self.outfit.pk).exists())


def test_outfit_adminlist(admin_client):
    outfits = [
        Outfit(title=f"Outfit {i}", description=f"Description for Outfit {i}")
        for i in range(20)
    ]
    Outfit.objects.bulk_create(outfits)
    outfits[0].items.set(
        [
            Item.objects.create(
                title="T-shirt",
                size="M",
                type="Shirt",
                color="White",
                description="White cotton t-shirt",
            ),
            Item.objects.create(
                title="T-shirt",
                size="M",
                type="Shirt",
                color="White",
                description="White cotton t-shirt",
            ),
        ]
    )
    outfits[0].save()
    url = "/admin/dressing/outfit/"
    response = admin_client.get(url)
    assert response.status_code == 200

    cl = response.context["cl"]
    assert cl.result_count == 20
    assert cl.full_result_count == 20
