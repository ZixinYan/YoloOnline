from django.urls import path

from utils.views import request_verification_code, verify_code, upload_file

urlpatterns = [
    path('getCode', request_verification_code, name='get_code'),
    path('verifyCode', verify_code, name='verify_code'),
    path('upload', upload_file, name='upload'),
]