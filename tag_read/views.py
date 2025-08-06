import logging
import time

from rest_framework import generics, mixins, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from hanger.models import Hanger
from hanger.serializers import HangerSerializer
from item.models import Item
from item.serializers import ItemSerializer
from tag.models import Tag
from tag.serializers import TagSerializer
from tag_read.models import TagRead
from tag_read.serializers import TagReadSerializer

logger = logging.getLogger(__name__)

# Variables globales pour la gestion des associations
TAG_WAIT_ID = None
TAG_WAIT_TYPE = None
TAG_FOUND_ID = None

ITEM_FOUND = None
HANGER_FOUND = None


def tag_received(tag_received: str):
    """
    Function to handle the reception of a tag.
    It updates the global variables based on the tag received.
    """
    global TAG_WAIT_ID, TAG_WAIT_TYPE, TAG_FOUND_ID
    global ITEM_FOUND, HANGER_FOUND

    TAG_FOUND_NAME = tag_received["tag"]
    tag = Tag.objects.filter(tag=TAG_FOUND_NAME).first()
    if tag is None:
        tag = Tag.objects.create(tag=TAG_FOUND_NAME)
    TAG_FOUND_ID = tag.pk

    logger.info(f"TAG_FOUND_ID: {TAG_FOUND_ID}, TAG_FOUND_NAME: {TAG_FOUND_NAME}")

    message = {}
    if TAG_WAIT_ID is not None:
        if TAG_WAIT_TYPE == "item":
            tag.item_id = Tag.objects.get(pk=TAG_WAIT_ID)
            tag.save()
            message_object = TagSerializer(tag.item_id).data
        elif TAG_WAIT_TYPE == "hanger":
            tag.hanger_id = Hanger.objects.get(pk=TAG_WAIT_ID)
            tag.save()
            message_object = HangerSerializer(tag.hanger_id).data

        message = {
            "status": "association_complete",
            "tag": TagSerializer(tag).data,
            "object": message_object,
        }
        TAG_WAIT_ID = None  # Reset if no tag found

    else:
        if tag.hanger_id is not None:
            HANGER_FOUND = tag.hanger_id
            message = {
                "status": "wait_item",
                "hanger": HangerSerializer(HANGER_FOUND).data,
            }
        elif tag.item_id is not None:
            ITEM_FOUND = tag.item_id
            message = {"status": "wait_hanger", "item": ItemSerializer(ITEM_FOUND).data}

        if ITEM_FOUND is not None and HANGER_FOUND is not None:
            item = Item.objects.filter(pk=ITEM_FOUND.pk).first()
            if item is not None:
                item.hanger_id = HANGER_FOUND
                item.save()
            message = {
                "status": "association_complete",
                "item": ItemSerializer(item).data,
                "hanger": HangerSerializer(HANGER_FOUND).data,
            }
            ITEM_FOUND = None
            HANGER_FOUND = None
    return message


class TagReadList(
    mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView
):
    queryset = TagRead.objects.all()
    serializer_class = TagReadSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        tag_read = self.create(request, *args, **kwargs)
        response = tag_received(tag_read.data)
        tag_read.data["message"] = response
        return tag_read


class TagReadDetail(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView,
):
    queryset = TagRead.objects.all()
    serializer_class = TagReadSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


@api_view(["GET"])
def tag_wait(request, type: str, id: int):
    """
    Send a item or hanger ID to wait for a tag.
    This function checks if a tag is waiting for an item or hanger ID.
    """
    if request.method == "GET":
        # Receives an item ID in the URL, stores it in a global variable, and waits until the variable is reset to None before responding
        global TAG_WAIT_ID, TAG_WAIT_TYPE
        if (type == "item" and Item.objects.filter(pk=id).exists() is False) and (
            type == "hanger" and Hanger.objects.filter(pk=id).exists() is False
        ):
            return Response(
                {"error": f"The id {id} does not exist for type '{type}'."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        TAG_WAIT_ID = id
        TAG_WAIT_TYPE = type

        logger.info(f"Item waiting for tag (POST /tag_read/): {TAG_WAIT_ID}")
        # Active wait until TAG_WAIT_ID is reset to None
        while TAG_WAIT_ID is not None:
            time.sleep(0.5)

        return Response(
            {
                "status": "association_complete",
                "id": id,
                "type": TAG_WAIT_TYPE,
                "tag_id": TAG_FOUND_ID,
            }
        )
