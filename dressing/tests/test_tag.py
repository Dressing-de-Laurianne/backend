from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from dressing.models import Tag


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

    def test_list_tags(self):
        url = "/tags/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_dict = response.json()
        self.assertGreaterEqual(response_dict["count"], 1)
        self.assertGreaterEqual(len(response_dict["results"]), 1)

    def test_update_tag(self):
        url = f"/tags/{self.tag.pk}/"
        data = {"tag": "NFC_TAG_1_updated"}
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.tag.refresh_from_db()
        self.assertEqual(self.tag.tag, "NFC_TAG_1_updated")

    def test_partial_update_tag(self):
        url = f"/tags/{self.tag.pk}/"
        data = {"tag": "NFC_TAG_1_patch"}
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.tag.refresh_from_db()
        self.assertEqual(self.tag.tag, "NFC_TAG_1_patch")

    def test_delete_tag(self):
        url = f"/tags/{self.tag.pk}/"
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Tag.objects.filter(pk=self.tag.pk).exists())
