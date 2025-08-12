from rest_framework import generics

from dressing.models import Hanger, HangerSerializer


class HangerList(generics.ListCreateAPIView):
    queryset = Hanger.objects.all()
    serializer_class = HangerSerializer


class HangerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Hanger.objects.all()
    serializer_class = HangerSerializer
