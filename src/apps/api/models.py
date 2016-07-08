

from django.core.urlresolvers import reverse
from django.contrib.postgres.fields import ArrayField
from django.db import models


class FaceImage(models.Model):
    title = models.CharField(max_length=100)
    original_image = models.ImageField(upload_to='uploads/originals/')
    processed_image = models.ImageField(upload_to='uploads/processed/', blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.title


class EyeCoordinate(models.Model):
    face_image = models.ForeignKey(FaceImage, related_name='eye_coordinates')
    coordinates = ArrayField(models.IntegerField(), blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "EyeCoordinate: {}".format(self.pk)


class NoseCoordinate(models.Model):
    face_image = models.ForeignKey(FaceImage, related_name='nose_coordinates')
    coordinates = ArrayField(models.IntegerField(), blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "EyeCoordinate: {}".format(self.pk)


class MouthCoordinate(models.Model):
    face_image = models.ForeignKey(FaceImage, related_name='mouth_coordinates')
    coordinates = ArrayField(models.IntegerField(), blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "EyeCoordinate: {}".format(self.pk)