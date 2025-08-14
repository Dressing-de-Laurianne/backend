from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from dressing.models import Hanger, Item, Tag


class TagAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.tag = Tag.objects.create(tag="NFC_TAG_1")

    def test_create_tag(self):
        url = "/tags/"
        data = {"tag": "NFC_TAG_2"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Tag.objects.filter(tag="NFC_TAG_2").exists())

        data = {"tag": "NFC_TAG_2", "item_id": "1", "hanger_id": "1"}
        response = self.client.post(url, data, format="json")
        response_dict = response.json()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response_dict["error"],
            "Both hanger_id and item_id cannot be non-null at the same time.",
        )

    def test_list_tags(self):
        url = "/tags/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_dict = response.json()
        self.assertGreaterEqual(response_dict["count"], 1)
        self.assertGreaterEqual(len(response_dict["results"]), 1)

    def test_get_tag(self):
        url = f"/tags/{self.tag.pk}/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_dict = response.json()
        self.assertGreaterEqual(response_dict["id"], self.tag.pk)

    def test_update_tag(self):
        url = f"/tags/{self.tag.pk}/"
        data = {"tag": "NFC_TAG_1_updated"}
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.tag.refresh_from_db()
        self.assertEqual(self.tag.tag, "NFC_TAG_1_updated")

        data = {"tag": "NFC_TAG_2", "item_id": "1", "hanger_id": "1"}
        response = self.client.put(url, data, format="json")
        response_dict = response.json()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response_dict["error"],
            "Both hanger_id and item_id cannot be non-null at the same time.",
        )

    def test_partial_update_tag(self):
        url = f"/tags/{self.tag.pk}/"
        data = {"tag": "NFC_TAG_1_patch"}
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.tag.refresh_from_db()
        self.assertEqual(self.tag.tag, "NFC_TAG_1_patch")

        data = {"tag": "NFC_TAG_2", "item_id": "1", "hanger_id": "1"}
        response = self.client.patch(url, data, format="json")
        response_dict = response.json()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response_dict["error"],
            "Both hanger_id and item_id cannot be non-null at the same time.",
        )

    def test_delete_tag(self):
        url = f"/tags/{self.tag.pk}/"
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Tag.objects.filter(pk=self.tag.pk).exists())


def test_tag_adminlist(admin_client):
    tags = [Tag(tag="NFC_TAG_{}".format(i)) for i in range(20)]
    Tag.objects.bulk_create(tags)

    tags[0].hanger_id = Hanger.objects.create(mqtt_topic="Hanger 1")
    tags[0].save()

    tags[1].item_id = Item.objects.create(
        title="T-shirt",
        size="M",
        type="Shirt",
        color="White",
        description="White cotton t-shirt",
    )
    tags[1].save()
    url = "/admin/dressing/tag/"
    response = admin_client.get(url)
    assert response.status_code == 200

    cl = response.context["cl"]
    assert cl.result_count == 20
    assert cl.full_result_count == 20
