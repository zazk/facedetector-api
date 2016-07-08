from rest_framework import routers

from django.conf.urls import url, include

from . import views

router = routers.DefaultRouter()
router.register(r'faceimages', views.FaceImageViewSet)
router.register(r'eyecoordinates', views.EyeCoordinateViewSet)
router.register(r'nosecoordinates', views.NoseCoordinateViewSet)
router.register(r'mouthcoordinates', views.MouthCoordinateViewSet)

urlpatterns = router.urls
