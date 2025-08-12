from rest_framework import generics

from dressing.models import Outfit, OutfitSerializer


class OutfitList(generics.ListCreateAPIView):
    queryset = Outfit.objects.all()
    serializer_class = OutfitSerializer


class OutfitDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Outfit.objects.all()
    serializer_class = OutfitSerializer
