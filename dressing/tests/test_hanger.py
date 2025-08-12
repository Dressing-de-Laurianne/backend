from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from dressing.models import Hanger


class HangerAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.hanger = Hanger.objects.create(mqtt_topic="/feed/hanger1")

    def test_create_hanger(self):
        url = "/hangers/"
        data = {"mqtt_topic": "/feed/hanger2"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Hanger.objects.filter(mqtt_topic="/feed/hanger2").exists())

    def test_list_hangers(self):
        url = "/hangers/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_update_hanger(self):
        url = f"/hangers/{self.hanger.pk}/"
        data = {"mqtt_topic": "/feed/hanger1-updated"}
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.hanger.refresh_from_db()
        self.assertEqual(self.hanger.mqtt_topic, "/feed/hanger1-updated")

    def test_partial_update_hanger(self):
        url = f"/hangers/{self.hanger.pk}/"
        data = {"mqtt_topic": "/feed/hanger1-patch"}
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.hanger.refresh_from_db()
        self.assertEqual(self.hanger.mqtt_topic, "/feed/hanger1-patch")

    def test_delete_hanger(self):
        url = f"/hangers/{self.hanger.pk}/"
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Hanger.objects.filter(pk=self.hanger.pk).exists())
