from rest_framework import generics

from outfit.models import Outfit
from outfit.serializers import OutfitSerializer


class OutfitList(generics.ListCreateAPIView):
    queryset = Outfit.objects.all()
    serializer_class = OutfitSerializer


class OutfitDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Outfit.objects.all()
    serializer_class = OutfitSerializer
