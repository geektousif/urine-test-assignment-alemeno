from django.urls import path
from .views import UrineStripImageView

urlpatterns = [
    path('image_upload/', UrineStripImageView.as_view(), name='urine_strip_image_upload')
]