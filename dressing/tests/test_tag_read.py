import threading
import time

from django.test import TransactionTestCase
from django.test.testcases import SerializeMixin
from rest_framework import status
from rest_framework.test import APIClient

from dressing.models import Hanger, Item, Tag, TagRead


class TagReadTestCaseMixin(TransactionTestCase, SerializeMixin):
    lockfile = __file__

    def setUp(self):
        self.client = APIClient()
        self.client.login(username="admin", password="admin")

        self.tag_read = TagRead.objects.create(tag="NFC_TAG_1")

        self.item = Item.objects.create(
            title="T-shirt",
            size="M",
            type="Shirt",
            color="White",
            description="White cotton t-shirt",
        )
        self.tag_item = Tag.objects.create(tag="myItemTag", item_id=self.item)
        self.hanger = Hanger.objects.create(mqtt_topic="/feed/hanger1")
        self.tag_hanger = Tag.objects.create(tag="myHangerTag", hanger_id=self.hanger)

        self.item_without_tag = Item.objects.create(
            title="T-shirt",
            size="XL",
            type="Shirt",
            color="Red",
            description="Red cotton t-shirt",
        )
        self.tag_without_item = Tag.objects.create(tag="myTagWithoutItem")

        self.hanger_without_tag = Hanger.objects.create(
            mqtt_topic="/feed/hanger_withouttag"
        )
        self.tag_without_hanger = Tag.objects.create(tag="myTagWithoutHanger")


class TagReadAPITestCase_tag_read_api(TagReadTestCaseMixin):
    def test_create_tag_read(self):
        url = "/tag_read/"
        data = {
            "tag": "NFC_TAG_2",
        }

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(TagRead.objects.filter(tag="NFC_TAG_2").exists())

    def test_list_tag_read(self):
        url = "/tag_read/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_dict = response.json()
        self.assertGreaterEqual(response_dict["count"], 1)
        self.assertGreaterEqual(len(response_dict["results"]), 1)

    def test_get_tag_read(self):
        url = f"/tag_read/{self.tag_read.pk}/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_dict = response.json()
        self.assertEqual(response_dict["id"], self.tag_read.pk)
        self.assertEqual(response_dict["tag"], self.tag_read.tag)

    def test_delete_tag_read(self):
        url = f"/tag_read/{self.tag_read.pk}/"
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(TagRead.objects.filter(pk=self.tag_read.pk).exists())


class TagReadAPITestCase_item_with_hanger(TagReadTestCaseMixin):

    def test_associate_item_with_hanger(self):
        data = {
            "tag": self.tag_item.tag,
        }
        response = self.client.post("/tag_read/", data, format="json")
        response_dict = response.json()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_dict["message"]["status"], "wait_hanger")

        self.assertEqual(Item.objects.get(pk=self.item.pk).hanger_id, None)

        data = {
            "tag": self.tag_hanger.tag,
        }
        response = self.client.post("/tag_read/", data, format="json")
        response_dict = response.json()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_dict["message"]["status"], "association_complete")

        self.assertEqual(Item.objects.get(pk=self.item.pk).hanger_id, self.hanger)


class TagReadAPITestCase_hanger_with_item(TagReadTestCaseMixin):

    def test_associate_hanger_with_item(self):
        data = {
            "tag": self.tag_hanger.tag,
        }
        response = self.client.post("/tag_read/", data, format="json")
        response_dict = response.json()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_dict["message"]["status"], "wait_item")

        self.assertEqual(Item.objects.get(pk=self.item.pk).hanger_id, None)

        data = {
            "tag": self.tag_item.tag,
        }
        response = self.client.post("/tag_read/", data, format="json")
        response_dict = response.json()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_dict["message"]["status"], "association_complete")

        self.assertEqual(Item.objects.get(pk=self.item.pk).hanger_id, self.hanger)


class TagReadAPITestCase_tag_with_item(TagReadTestCaseMixin):
    def test_associate_tag_with_item(self):

        # Start the blocking call in a separate thread

        responses = {}

        def blocking_call_item():
            resp = self.client.get(
                "/tag_wait/item/" + str(self.item_without_tag.pk) + "/"
            )
            responses["blocking"] = resp

        thread = threading.Thread(target=blocking_call_item)
        thread.start()
        time.sleep(0.5)

        self.assertEqual(Tag.objects.get(pk=self.tag_without_item.pk).item_id, None)

        # Simulate the action that unblocks the call
        data = {
            "tag": self.tag_without_item.tag,
        }
        response = self.client.post("/tag_read/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Wait for the blocking call to finish and check its response
        thread.join()
        blocking_response = responses["blocking"]
        self.assertEqual(blocking_response.status_code, status.HTTP_200_OK)
        self.assertEqual(blocking_response.json()["status"], "association_complete")
        self.assertEqual(response.json()["message"]["status"], "association_complete")

        self.assertEqual(
            Tag.objects.get(item_id=self.item_without_tag.pk), self.tag_without_item
        )


class TagReadAPITestCase_tag_with_hanger(TagReadTestCaseMixin):
    def test_associate_tag_with_hanger(self):

        # Start the blocking call in a separate thread

        responses = {}

        def blocking_call_hanger():
            resp = self.client.get(
                "/tag_wait/hanger/" + str(self.hanger_without_tag.pk) + "/"
            )
            responses["blocking"] = resp

        thread = threading.Thread(target=blocking_call_hanger)
        thread.start()
        time.sleep(0.5)

        self.assertEqual(Tag.objects.get(pk=self.tag_without_hanger.pk).hanger_id, None)

        # Simulate the action that unblocks the call
        data = {
            "tag": self.tag_without_hanger.tag,
        }
        response = self.client.post("/tag_read/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Wait for the blocking call to finish and check its response
        thread.join()
        blocking_response = responses["blocking"]
        self.assertEqual(blocking_response.status_code, status.HTTP_200_OK)
        self.assertEqual(blocking_response.json()["status"], "association_complete")
        self.assertEqual(response.json()["message"]["status"], "association_complete")

        self.assertEqual(
            Tag.objects.get(hanger_id=self.hanger_without_tag.pk),
            self.tag_without_hanger,
        )


class TagReadAPITestCase_tag_with_error(TagReadTestCaseMixin):
    def test_associate_tag_with_error(self):

        response = self.client.get("/tag_wait/hanger/400/")
        response_dict = response.json()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response_dict["error"], "The id 400 does not exist for type 'hanger'."
        )
