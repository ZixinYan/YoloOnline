from django.shortcuts import render

# Create your views here.
import re
import random
import redis
from django.core.mail import send_mail
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.utils.timezone import now
from kombu.utils import json

###         utils/views          ###
# Redis 配置
redis_client = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)
# 请求验证码
@csrf_exempt
def request_verification_code(request):
    if request.method == "POST":
        body = json.loads(request.body)
        email = body.get('email')
        print(email)
        if not email:
            return JsonResponse({
                "code":1,
                "message": "请输入有效的邮箱地址"})
        # 生成验证码
        code = generate_code()
        # 将验证码存储在 Redis 中，设置过期时间为 5 分钟
        redis_client.setex(f"verification_code:{email}", 300, code)
        # 发送验证码邮件
        send_verification_email(email, code)
        return JsonResponse({
            "code": 0,
            "message": "验证码已发送，请查收邮件"})


# 验证验证码
@csrf_exempt
def verify_code(request):
    if request.method == "POST":
        body = json.loads(request.body)
        email = body.get('email')
        code = body.get('code')

        if not email or not code:
            return JsonResponse({
                "code": 1,
                "message": "请输入邮箱和验证码"})

        # 从 Redis 中获取验证码
        stored_code = redis_client.get(f"verification_code:{email}")

        if stored_code is None:
            return JsonResponse({
                "code": 1,
                "message": "验证码已过期或发送失败"})

        if stored_code.decode('utf-8') != code:
            return JsonResponse({"error": "验证码不正确"})

        return JsonResponse({
            "code": 0,
            "message": "验证码验证成功",
            "data": {
                "email": email,
                "code": 114
            }
        })

@csrf_exempt
def upload_file(request):
    if request.method == 'POST':
        token = request.META.get('HTTP_AUTHORIZATION')
        if token:


            if request.FILES.get('file'):
                 file = request.FILES['file']
                 print(file)
                 file_url = upload_file_to_oss(file)
                 if file_url:
                    return JsonResponse({'code': 0, 'message':'success', 'data': file_url})
                 else:
                    return JsonResponse({'code': 1, 'message': '上传失败'})


            return JsonResponse({'code': 1, 'message': '上传失败'})


        else:
            return JsonResponse(
                {'code': 1, 'message': 'token is missing or invalid'},
                status=403
            )






###         utils/function          ###
def check_email(email):
    """验证邮箱格式"""
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(email_regex, email) is not None

# 生成六位数字验证码
def generate_code():
    return str(random.randint(100000, 999999))


# 发送验证码邮件
def send_verification_email(email, code):
    subject = "杂鱼大哥哥，心怀感激的收下验证码吧："
    message = (f"杂鱼~，杂鱼~\n"
               f"真是会给我找麻烦呢，记住了哦！\n"
               f"====================================\n"
               f"{code}\n"
               f"====================================\n"
               f"如果 5 分钟之内都不用的话就不要来找我了哦！\n")
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])

# 上传文件到阿里云OSS
    # utils/aliyun_oss_utils.py
import oss2
import os
import uuid

def upload_file_to_oss(file_obj):
    """
    上传文件到阿里云OSS
    :param object_name: 文件名（带路径）
    :param file_obj: 上传的文件对象
    :return: 上传后的文件URL
    """
    auth = oss2.Auth(settings.OSS_ACCESS_KEY_ID, settings.OSS_ACCESS_KEY_SECRET)
    bucket = oss2.Bucket(auth, settings.OSS_ENDPOINT, settings.OSS_BUCKET_NAME)
    file_extension = os.path.splitext(file_obj.name)[1]
    file_name = f'{uuid.uuid4().hex}{file_extension}'  # 使用uuid生成唯一文件名
    try:
        # 上传文件
        bucket.put_object(file_name, file_obj)
        file_url = f'https://{settings.OSS_BUCKET_NAME}.{settings.OSS_ENDPOINT[8:]}/{file_name}'
        return file_url
    except oss2.exceptions.OssError as e:
        print(f"上传文件失败: {e}")
        return None

