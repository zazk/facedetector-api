
from cStringIO import StringIO

import PIL
from rest_framework import serializers

from django.core.files.base import  ContentFile

from ..detector.face_detector import detect_coordinates
from .models import FaceImage, EyeCoordinate, NoseCoordinate, MouthCoordinate


class FaceImageSerializer(serializers.ModelSerializer):
    eye_coordinates = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    nose_coordinates = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    mouth_coordinates = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = FaceImage
        fields = ('pk', 'title', 'original_image', 'processed_image', 'created_date', 'modified_date',
                  'eye_coordinates', 'nose_coordinates', 'mouth_coordinates')

    def create(self, validated_data):
        face_image = FaceImage.objects.create(**validated_data)

        (ec, nc, mc, np_array) = detect_coordinates(face_image.original_image.path)

        for eye_coordinate in ec:
            print eye_coordinate
            print type(eye_coordinate)
            eye_coordinate_obj = EyeCoordinate(coordinates=eye_coordinate)
            eye_coordinate_obj.face_image = face_image
            eye_coordinate_obj.save()

        for nose_coordinate in nc:
            print nose_coordinate
            print type(nose_coordinate)
            nose_coordinate_obj = NoseCoordinate(coordinates=nose_coordinate)
            nose_coordinate_obj.face_image = face_image
            nose_coordinate_obj.save()

        for mouth_coordinate in mc:
            print mouth_coordinate
            print type(mouth_coordinate)
            mouth_coordinate_obj = MouthCoordinate(coordinates=mouth_coordinate)
            mouth_coordinate_obj.face_image = face_image
            mouth_coordinate_obj.save()

        pillow_img = PIL.Image.fromarray(np_array)
        f = StringIO()

        try:
            pillow_img.save(f, format='png')
            s = f.getvalue()
            face_image.processed_image.save("{}-processed.png".format(face_image.original_image.name), ContentFile(s))
        finally:
            f.close()

        return face_image


class EyeCoordinateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EyeCoordinate
        fields = ('face_image', 'coordinates', 'created_date', 'modified_date',)


class NoseCoordinateSerializer(serializers.ModelSerializer):
    class Meta:
        model = NoseCoordinate
        fields = ('face_image', 'coordinates', 'created_date', 'modified_date',)


class MouthCoordinateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MouthCoordinate
        fields = ('face_image', 'coordinates', 'created_date', 'modified_date',)
