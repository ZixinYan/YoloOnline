from django.urls import path
from user.views import login, register, get_user_info, update, get_user_list, updateAvatar, findPassword, updatePwd
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
urlpatterns = [
    #path('/test',TestView.as_view(), name='test'),
    #path('/jwt', JwtTestView.as_view(), name='test'),
    path('login', login, name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('register', register, name='register'),
    path('userlist', get_user_list, name='get_user_info'),
    path('update',update,name='update'),
    path('userinfo',get_user_info,name='get_user_info'),
    path('updateAvatar',updateAvatar,name='updateAvatar'),
    path('findPassword',findPassword,name='findPassword'),
    path('updatePwd',updatePwd,name='updatePassword'),
]