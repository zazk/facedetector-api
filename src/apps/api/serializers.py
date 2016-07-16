
from cStringIO import StringIO

import PIL

from django.core.files.base import ContentFile

from rest_framework import serializers

from ..detector.face_detector import detect_coordinates
from .models import (EyeCoordinate, FaceCoordinate, FaceImage, MouthCoordinate,
                     NoseCoordinate)


class EyeCoordinateSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='api:eyecoordinate-detail')

    class Meta:
        model = EyeCoordinate
        fields = ('face_image', 'pk', 'url', 'coordinates', 'created_date',
                  'modified_date',)


class NoseCoordinateSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='api:nosecoordinate-detail')

    class Meta:
        model = NoseCoordinate
        fields = ('face_image', 'pk', 'url', 'coordinates', 'created_date',
                  'modified_date',)


class MouthCoordinateSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='api:mouthcoordinate-detail')

    class Meta:
        model = MouthCoordinate
        fields = ('face_image', 'pk', 'url', 'coordinates', 'created_date',
                  'modified_date',)


class FaceCoordinateSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='api:facecoordinate-detail')

    class Meta:
        model = FaceCoordinate
        fields = ('face_image', 'pk', 'url', 'coordinates', 'created_date',
                  'modified_date',)


class FaceImageSerializer(serializers.ModelSerializer):
    face_coordinates = FaceCoordinateSerializer(many=True, read_only=True)
    eye_coordinates = EyeCoordinateSerializer(many=True, read_only=True)
    nose_coordinates = NoseCoordinateSerializer(many=True, read_only=True)
    mouth_coordinates = MouthCoordinateSerializer(many=True, read_only=True)
    url = serializers.HyperlinkedIdentityField(
        view_name='api:faceimage-detail')

    class Meta:
        model = FaceImage
        fields = (
            'pk', 'url', 'title', 'original_image', 'processed_image',
            'created_date', 'modified_date', 'face_coordinates',
            'eye_coordinates', 'nose_coordinates', 'mouth_coordinates'
        )

    def create(self, validated_data):
        face_image = FaceImage.objects.create(**validated_data)

        (fc, ec, nc, mc, np_array) = detect_coordinates(
            face_image.original_image.path)

        for face_coordinate in fc:
            face_coordinate_obj = FaceCoordinate(coordinates=face_coordinate)
            face_coordinate_obj.face_image = face_image
            face_coordinate_obj.save()

        for eye_coordinate in ec:
            eye_coordinate_obj = EyeCoordinate(coordinates=eye_coordinate)
            eye_coordinate_obj.face_image = face_image
            eye_coordinate_obj.save()

        for nose_coordinate in nc:
            nose_coordinate_obj = NoseCoordinate(coordinates=nose_coordinate)
            nose_coordinate_obj.face_image = face_image
            nose_coordinate_obj.save()

        for mouth_coordinate in mc:
            mouth_coordinate_obj = MouthCoordinate(
                coordinates=mouth_coordinate)
            mouth_coordinate_obj.face_image = face_image
            mouth_coordinate_obj.save()

        pillow_img = PIL.Image.fromarray(np_array)
        f = StringIO()

        try:
            pillow_img.save(f, format='png')
            s = f.getvalue()
            face_image.processed_image.save(
                "{}-processed.png".format(face_image.original_image.name),
                ContentFile(s)
            )
        finally:
            f.close()

        return face_image
