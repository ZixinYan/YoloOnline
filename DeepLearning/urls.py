from django.conf.urls.static import static
# from django.contrib import admin
from django.urls import path
from django.urls.conf import include

from DeepLearning import settings

urlpatterns = [
    path('user/',include('user.urls')),
    path('utils/', include('utils.urls')),
    path('yolov5/',include('yolov5.urls')),
]
