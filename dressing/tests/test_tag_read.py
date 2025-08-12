import threading

from django.test import TransactionTestCase
from rest_framework import status
from rest_framework.test import APIClient

from dressing.models import Hanger, Item, Tag


class TagReadAPITestCase(TransactionTestCase):
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

    def test_associate_tag_with_item(self):

        # Start the blocking call in a separate thread

        responses = {}

        def blocking_call():
            resp = self.client.get(
                "/tag_wait/item/" + str(self.item_without_tag.pk) + "/"
            )
            responses["blocking"] = resp

        thread = threading.Thread(target=blocking_call)
        thread.start()

        # self.assertEqual(Tag.objects.get(item_id=self.item_without_tag), None)
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
        blocking_response_dict = blocking_response.json()
        self.assertEqual(blocking_response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            blocking_response_dict["message"]["status"], "association_complete"
        )

        self.assertEqual(
            Tag.objects.get(item_id=self.item_without_tag.pk), self.tag_without_item
        )
