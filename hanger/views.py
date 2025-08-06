from rest_framework import generics

from hanger.models import Hanger
from hanger.serializers import HangerSerializer


class HangerList(generics.ListCreateAPIView):
    queryset = Hanger.objects.all()
    serializer_class = HangerSerializer


class HangerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Hanger.objects.all()
    serializer_class = HangerSerializer
