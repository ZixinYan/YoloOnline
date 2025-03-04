from django.urls import path
from django.conf.urls.static import static
from DeepLearning import settings
from yolov5.views import handle_file_upload, detect_image, detect_instant
urlpatterns = [
    path('upload',handle_file_upload,name="upload"),
    path('image',detect_image,name="image"),
    path('instant', detect_instant,name="instant"),
]

