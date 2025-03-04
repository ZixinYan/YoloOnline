from django.urls import path
from user.views import login, register, get_user_info, update, get_user_list, updateAvatar, findPassword, updatePwd

urlpatterns = [
    #path('/test',TestView.as_view(), name='test'),
    #path('/jwt', JwtTestView.as_view(), name='test'),
    path('login', login, name='login'),
    path('register', register, name='register'),
    path('userlist', get_user_list, name='get_user_info'),
    path('update',update,name='update'),
    path('userinfo',get_user_info,name='get_user_info'),
    path('updateAvatar',updateAvatar,name='updateAvatar'),
    path('findPassword',findPassword,name='findPassword'),
    path('updatePwd',updatePwd,name='updatePassword'),
]