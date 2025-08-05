from outfit.models import Outfit
from outfit.serializers import OutfitSerializer
from rest_framework import generics

class OutfitList(generics.ListCreateAPIView):
    queryset = Outfit.objects.all()
    serializer_class = OutfitSerializer

class OutfitDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Outfit.objects.all()
    serializer_class = OutfitSerializer