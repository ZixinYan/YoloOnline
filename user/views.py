from datetime import datetime
import json

from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.template.context_processors import request
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from jwt import ExpiredSignatureError, DecodeError
from rest_framework_jwt.settings import api_settings


from user.models import SysUser


# Create your views here.
'''
class TestView(View):
    def get(self,request):
        token = request.META.get('HTTP_AUTHORIZATION')
        if token != None and token != '':
            print('token:',token);
            userList_obj = SysUser.objects.all()
            userList_dict = userList_obj.values() # QuerySet对象转换为字典
            userList_list = list(userList_dict)
            print(userList_list)
            return JsonResponse({
                'code':200,
                'msg':'success',
                'data':'Test Get'
            })
        else:
            return JsonResponse({
                'code':401,
                'msg':'fail',
                'data':'No token'
            })

class JwtTestView(View):
    def get(self,request):
        user = SysUser.objects.get(username='admin',password='123456')
        jwt = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode = api_settings.JWT_ENCODE_HANDLER
        payload = jwt(user)
        token = jwt_encode(payload)
        return JsonResponse({
            'code':200,
            'msg':'success',
            'data':token
        })
'''


@csrf_exempt
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            # 尝试根据用户名和密码查询用户
            user = SysUser.objects.get(username=username, password=password)
            user.login_date = datetime.now()
            user.save()
            # 生成JWT令牌
            jwt = api_settings.JWT_PAYLOAD_HANDLER
            jwt_encode = api_settings.JWT_ENCODE_HANDLER
            payload = jwt(user)
            token = jwt_encode(payload)

            return JsonResponse({
                'code': 0,
                'message': 'success',
                'data': token
            })

        except SysUser.DoesNotExist:
            # 如果查询不到用户，返回用户名或密码错误的消息
            return JsonResponse({
                'code': 1,
                'message': '用户名或密码不正确',
            })

@csrf_exempt
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            # 尝试根据用户名查询用户
            user = SysUser.objects.get(username=username)
            return JsonResponse({
                'code': 1,
                'message': '用户名已存在',
            })
        except SysUser.DoesNotExist:
            # 如果查询不到用户，创建新用户
            user = SysUser.objects.create(username=username, password=password,
                                          create_time=datetime.now(),update_time=datetime.now(),status=1)
            return JsonResponse({
                'code': 0,
                'message': 'success',
            })


@csrf_exempt
def get_user_list(request):
    if request.method == 'GET':
        token = request.META.get('HTTP_AUTHORIZATION')
        if token:
            # 解析JWT令牌
            jwt_decode = api_settings.JWT_DECODE_HANDLER
            payload = jwt_decode(token)

            # 获取所有用户的信息
            users = SysUser.objects.all()
            user_list = []

            for user in users:
                user_list.append({
                    'username': user.username,
                    'password': user.password,
                    'email': user.email,
                    'phone': user.phone_number,
                    'avatar': user.avatar,
                    'status': user.status,
                    'login_date': user.login_date,
                    'create_time': user.create_time,
                    'update_time': user.update_time
                })

            return JsonResponse({
                'code': 0,
                'message': 'success',
                'data': user_list
            })
        else:
            return JsonResponse(
                {'code': 1, 'message': 'token is missing or invalid'},
                status=401
            )

@csrf_exempt
def update(request):
    if request.method == 'PUT':
        token = request.META.get('HTTP_AUTHORIZATION')
        if token:
            # 解析JWT令牌
            jwt_decode = api_settings.JWT_DECODE_HANDLER
            payload = jwt_decode(token)
            # 获取用户名
            username = payload['username']
            data = json.loads(request.body.decode('utf-8'))
            # 获用户对象
            user = SysUser.objects.get(username=username)
            # 更新用户信息
            user.email = data.get('email')
            user.phone_number = data.get('phone_number')
            user.update_time = datetime.now()
            if len(user.phone_number) != 11:
                return JsonResponse({
                    'code': 1,
                    'message': 'Phone number is incorrect'
                })
            user.save()

            return JsonResponse({
                'code': 0,
                'message': 'success'
            })
        else:
            return JsonResponse({
                'code': 1,
                'message': 'No token'
            },status=401)

@csrf_exempt
@api_view(['PATCH'])
def updateAvatar(request):
    if request.method == 'PATCH':
        token = request.META.get('HTTP_AUTHORIZATION')
        if token:
            # 解析JWT令牌
            jwt_decode = api_settings.JWT_DECODE_HANDLER
            payload = jwt_decode(token)
            # 获取用户名
            username = payload['username']
            # 获用户对象
            user = SysUser.objects.get(username=username)
            # 更新用户头像
            user.avatar = request.data.get('avatar')
            user.update_time = datetime.now()
            user.save()

            return JsonResponse({
                'code': 0,
                'message': 'success',
                'data' : user.avatar
            })
        else:
            return JsonResponse(
                {'code': 1, 'message': 'token is missing or invalid'},
                status=401
            )

@csrf_exempt
@api_view(['PATCH'])
def updatePwd(request):
    if request.method == 'PATCH':
        token = request.META.get('HTTP_AUTHORIZATION')
        if token:
            # 解析JWT令牌
            jwt_decode = api_settings.JWT_DECODE_HANDLER
            payload = jwt_decode(token)
            # 获取用户名
            username = payload['username']
            # 获用户对象
            user = SysUser.objects.get(username=username)
            # 更新用户密码
            oldPwd = request.data.get('old_pwd')
            if oldPwd != user.password:
                return JsonResponse({
                    'code': 1,
                    'message': 'Old password is incorrect'
                })
            user.password = request.data.get('new_pwd')
            if(user.password == oldPwd):
                return JsonResponse({
                    'code': 1,
                    'message': 'New password is the same as the old password'
                })
            user.update_time = datetime.now()
            user.save()

            return JsonResponse({
                'code': 0,
                'message': 'success'
            })
        else:
            return JsonResponse(
                {'code': 1, 'message': 'token is missing or invalid'},
                status=401
            )

@csrf_exempt
def findPassword(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')
        try:
            # 尝试根据邮箱查询用户
            user = SysUser.objects.get(email=email)
            user.password = password
            user.save()
            return JsonResponse({
                'code': 0,
                'message': '重置成功',
            })

        except SysUser.DoesNotExist:
            # 如果查询不到用户，返回用户名或邮箱错误的消息
            return JsonResponse({
                'code': 1,
                'message': '用户名或邮箱不正确',
            })


@csrf_exempt
def get_user_info(request):
    if request.method == 'GET':
        # 获取 Authorization 头部中的 token
        token = request.META.get('HTTP_AUTHORIZATION')
        print(token)
        if token:
            try:
                # 解析JWT令牌
                jwt_decode = api_settings.JWT_DECODE_HANDLER
                payload = jwt_decode(token)

                # 获取用户名
                username = payload.get('username')

                if not username:
                    return JsonResponse(
                        {'code': 1, 'message': 'token is missing or invalid'},
                        status=401
                    )

                try:
                    # 获取用户对象
                    user = SysUser.objects.get(username=username)

                    return JsonResponse({
                        'code': 0,
                        'message': 'success',
                        'data': {
                            'username': user.username,
                            'email': user.email,
                            'phone_number': user.phone_number,
                            'avatar': user.avatar,
                            'status': user.status
                        }
                    })
                except SysUser.DoesNotExist:
                    return JsonResponse({
                        'code': 1,
                        'message': 'User not found'
                    })
            except ExpiredSignatureError:
                return JsonResponse(
                    {'code': 1, 'message': 'token is missing or invalid'},
                    status=401
                )