import logging
import time

from rest_framework import generics, mixins, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from dressing.models import (
    Hanger,
    HangerSerializer,
    Item,
    ItemSerializer,
    Tag,
    TagRead,
    TagReadSerializer,
    TagSerializer,
)
from dressing.shared import namespace

logger = logging.getLogger(__name__)

manager = None
manager_namespace = None

# Variables globales pour la gestion des associations
# ns = get_manager_namespace()
# ns.TAG_WAIT_ID = None
# ns.TAG_WAIT_TYPE = None
# ns.TAG_FOUND_ID = None

# ns.ITEM_FOUND = None
# ns.HANGER_FOUND = None


def tag_received(tag_received: str):
    """
    Function to handle the reception of a tag.
    It updates the global variables based on the tag received.
    """
    ns = namespace

    ns.TAG_FOUND_NAME = tag_received["tag"]
    tag = Tag.objects.filter(tag=ns.TAG_FOUND_NAME).first()
    if tag is None:
        tag = Tag.objects.create(tag=ns.TAG_FOUND_NAME)
    ns.TAG_FOUND_ID = tag.pk

    logger.info(f"TAG_FOUND_ID: {ns.TAG_FOUND_ID}, TAG_FOUND_NAME: {ns.TAG_FOUND_NAME}")

    message = {}
    if ns.TAG_WAIT_ID is not None:
        if ns.TAG_WAIT_TYPE == "item":
            tag.item_id = Item.objects.get(pk=ns.TAG_WAIT_ID)
            tag.save()
            message_object = ItemSerializer(tag.item_id).data
        elif ns.TAG_WAIT_TYPE == "hanger":
            tag.hanger_id = Hanger.objects.get(pk=ns.TAG_WAIT_ID)
            tag.save()
            message_object = HangerSerializer(tag.hanger_id).data

        message = {
            "status": "association_complete",
            "tag": TagSerializer(tag).data,
            "object": message_object,
        }
        ns.TAG_WAIT_ID = None  # Reset if no tag found

    else:
        if tag.hanger_id is not None:
            ns.HANGER_FOUND = tag.hanger_id
            message = {
                "status": "wait_item",
                "hanger": HangerSerializer(ns.HANGER_FOUND).data,
            }
        elif tag.item_id is not None:
            ns.ITEM_FOUND = tag.item_id
            message = {
                "status": "wait_hanger",
                "item": ItemSerializer(ns.ITEM_FOUND).data,
            }

        if ns.ITEM_FOUND is not None and ns.HANGER_FOUND is not None:
            item = Item.objects.filter(pk=ns.ITEM_FOUND.pk).first()
            if item is not None:
                item.hanger_id = ns.HANGER_FOUND
                item.save()
            message = {
                "status": "association_complete",
                "item": ItemSerializer(item).data,
                "hanger": HangerSerializer(ns.HANGER_FOUND).data,
            }
            ns.ITEM_FOUND = None
            ns.HANGER_FOUND = None
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
        ns = namespace
        if (type == "item" and Item.objects.filter(pk=id).exists() is False) and (
            type == "hanger" and Hanger.objects.filter(pk=id).exists() is False
        ):
            return Response(
                {"error": f"The id {id} does not exist for type '{type}'."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        ns.TAG_WAIT_ID = id
        ns.TAG_WAIT_TYPE = type

        logger.info(f"Item waiting for tag (POST /tag_read/): {ns.TAG_WAIT_ID}")
        # Active wait until TAG_WAIT_ID is reset to None
        while ns.TAG_WAIT_ID is not None:
            time.sleep(0.5)

        return Response(
            {
                "status": "association_complete",
                "id": id,
                "type": ns.TAG_WAIT_TYPE,
                "tag_id": ns.TAG_FOUND_ID,
            }
        )
