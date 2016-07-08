from django.contrib import admin

from .models import FaceImage

@admin.register(FaceImage)
class FaceImageAdmin(admin.ModelAdmin):
    pass
