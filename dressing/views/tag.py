from rest_framework import generics, mixins, status
from rest_framework.response import Response

from dressing.models import Tag, TagSerializer


class TagList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        hanger_id = request.data.get("hanger_id")
        item_id = request.data.get("item_id")
        if hanger_id is not None and item_id is not None:
            return Response(
                {
                    "error": "Both hanger_id and item_id cannot be non-null at the same time."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        return self.create(request, *args, **kwargs)


class TagDetail(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView,
):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        # Get the existing tag instance
        tag = self.get_object()
        # Get incoming data
        hanger_id = request.data.get("hanger_id", getattr(tag, "hanger_id", None))
        item_id = request.data.get("item_id", getattr(tag, "item_id", None))
        # Check both hanger_id and item_id are not non-null at the same time
        if hanger_id is not None and item_id is not None:
            return Response(
                {
                    "error": "Both hanger_id and item_id cannot be non-null at the same time."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        # Get the existing tag instance
        tag = self.get_object()
        # Get incoming data
        hanger_id = request.data.get("hanger_id", getattr(tag, "hanger_id", None))
        item_id = request.data.get("item_id", getattr(tag, "item_id", None))
        # Check both hanger_id and item_id are not non-null at the same time
        if hanger_id is not None and item_id is not None:
            return Response(
                {
                    "error": "Both hanger_id and item_id cannot be non-null at the same time."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
