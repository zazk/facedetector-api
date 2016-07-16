from django.conf.urls import include, url

from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'faceimages', views.FaceImageViewSet)
router.register(r'eyecoordinates', views.EyeCoordinateViewSet)
router.register(r'nosecoordinates', views.NoseCoordinateViewSet)
router.register(r'mouthcoordinates', views.MouthCoordinateViewSet)
router.register(r'facecoordinates', views.FaceCoordinateViewSet)

urlpatterns = router.urls
