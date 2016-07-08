from rest_framework import viewsets

from .models import FaceImage, EyeCoordinate, NoseCoordinate, MouthCoordinate
from .serializers import FaceImageSerializer, EyeCoordinateSerializer, NoseCoordinateSerializer, MouthCoordinateSerializer


class FaceImageViewSet(viewsets.ModelViewSet):
    queryset = FaceImage.objects.all()
    serializer_class = FaceImageSerializer


class EyeCoordinateViewSet(viewsets.ModelViewSet):
    queryset = EyeCoordinate.objects.all()
    serializer_class = EyeCoordinateSerializer


class NoseCoordinateViewSet(viewsets.ModelViewSet):
    queryset = NoseCoordinate.objects.all()
    serializer_class = NoseCoordinateSerializer


class MouthCoordinateViewSet(viewsets.ModelViewSet):
    queryset = MouthCoordinate.objects.all()
    serializer_class = MouthCoordinateSerializer
