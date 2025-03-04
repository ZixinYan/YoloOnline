import json
import shutil
import subprocess
import threading

from django.db.models.expressions import result
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os
import torch
import cv2
import numpy as np
import uuid

from torch.fx.experimental.unification.multipledispatch.dispatcher import source

from DeepLearning import settings

# 允许的图片格式
ALLOWED_IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.png']
@csrf_exempt
def handle_file_upload(request):
    if request.method == 'POST':
        token = request.META.get('HTTP_AUTHORIZATION')
        if token:
            print("当前工作目录: ", os.getcwd())
            file = request.FILES.get('file')
            if not file:
                return JsonResponse({
                    'code' : 1,
                    'message': '没有上传文件'
                })
            file_extension = os.path.splitext(file.name)[1].lower()
            if file_extension not in ALLOWED_IMAGE_EXTENSIONS:
                return JsonResponse({
                    'code': 1,
                    'message': '只支持上传jpg、jpeg、png格式的图片'
                })
            unique_filename = file.name.split('.')[0] + '_' + uuid.uuid1().hex + file_extension
            file_path = os.path.join('project', 'yolov5', 'detect', unique_filename)
            try:
                with open(file_path, 'wb') as f:
                    for chunk in file.chunks():
                        f.write(chunk)
                # 返回上传成功的响应
                return JsonResponse({
                    'code': 0,
                    'message': '文件上传成功',
                    'data': {
                        'filename': unique_filename
                    }
                })
            except Exception as e:
                print(str(e))
                return JsonResponse(
                    {'code': 1, 'message': '文件上传失败', 'data': str(e)}
                )
        else:
            return JsonResponse({
                'code' : 1,
                'message' : 'token失效或缺少，请重新登录'
            },status=401)

@csrf_exempt
def detect_image(request):
    if request.method == 'POST':
        token = request.META.get('HTTP_AUTHORIZATION')
        if token:
            body = json.loads(request.body)
            filename = body.get("filename")
            print(filename)
            if not filename:
                return JsonResponse({
                    'code': 1,
                    'message': '请上传文件'
                })
            file_path = os.path.join('project', 'yolov5', 'detect', filename)
            if not os.path.exists(file_path):
                return JsonResponse({
                    'code': 1,
                    'message': '文件不存在'
                })
            # 调用模型进行目标检测
            # result = detect_online(file_path)
            result = detect(file_path, filename)
            return result
        else:
            return JsonResponse({
                'code' :1,
                'message': 'token失效或缺少.请重新登录'
            },status=401)


@csrf_exempt
def detect_instant(request):
    # 确保只处理 POST 请求
    if request.method != 'POST':
        return JsonResponse({
            'code': 1,
            'message': '仅支持 POST 请求'
        }, status=400)

    # 验证 Token
    token = request.META.get('HTTP_AUTHORIZATION')
    if not token:
        return JsonResponse({
            'code': 1,
            'message': '缺少认证令牌',
        }, status=401)

    try:
        # 启动后台线程来处理视频流
        threading.Thread(target=process_video_stream).start()

        # 线程启动成功后，返回响应
        return JsonResponse({
            'code': 0,
            'message': '视频流处理已启动'
        })

    except Exception as e:
        return JsonResponse({
            'code': 1,
            'message': '处理视频流时发生错误',
            'data': str(e)
        }, status=500)


# 在后台线程中进行视频流处理
def process_video_stream_online():
    cap = cv2.VideoCapture(0)
    window_name = 'YOLO'
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    try:
        # 加载 YOLOv5 模型
        model = torch.hub.load('ultralytics/yolov5', 'custom',
                               path='E:\\Biancheng\\DeepLearning\\project\\yolov5\\runs\\train\\exp11\\weights\\last.pt',
                               force_reload=True)
        while cap.isOpened():
            ret, frame = cap.read()  # 读取每一帧
            if not ret:
                break
            # 模型推理
            results = model(frame)
            result_frame = np.squeeze(results.render())
            # 显示推理结果
            cv2.imshow(window_name, result_frame)

            # 如果窗口关闭或按下 'q' 键，退出循环
            if cv2.getWindowProperty(window_name, cv2.WND_PROP_VISIBLE) < 1:
                break
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()
    except Exception as e:
        print(f"Error in video processing: {e}")
        cap.release()
        cv2.destroyAllWindows()


def process_video_stream():
    try:
        weights_path = './project/yolov5/runs/train/exp11/weights/last.pt'
        command = [
            'python', './project/yolov5/detect.py',
            '--source', '0',  # 使用默认摄像头
            '--weights', weights_path,
            '--view-img',  # 显示图像
            '--nosave'  # 不保存结果
        ]

        print("Start running YOLOv5 detect.py script...")

        # 运行命令并捕获输出
        result = subprocess.run(command, capture_output=True, text=True)

        # 打印标准输出和标准错误
        print("stdout:", result.stdout)
        print("stderr:", result.stderr)

        # 如果命令执行失败，返回错误信息
        if result.returncode != 0:
            return JsonResponse({
                'code': 1,
                'message': f'命令执行失败: {result.stderr}',
            })

        return JsonResponse({
            'code': 0,
            'message': '视频流处理完成',
        })

    except Exception as e:
        # 捕获其他异常并返回
        return JsonResponse({
            'code': 1,
            'message': f'出现错误: {str(e)}',
        })


# 使用在线模型进行detect
def detect_online(file_path):
    try:
        model = torch.hub.load('ultralytics/yolov5', 'custom',
                            path='E:\\Biancheng\\DeepLearning\\project\\yolov5\\runs\\train\\exp11\\weights\\last.pt',
                            force_reload=True)
        frame = cv2.imread(file_path)
        results = model(frame)
        detections = []
        for *xyxy, conf, cls in results.xyxy[0]:
            label = results.names[int(cls)]
            confidence = conf.item()
            xmin, ymin, xmax, ymax = map(int, xyxy)
            detections.append({
                'label': label,
                'confidence': confidence,
                'bbox': [xmin, ymin, xmax, ymax]
             })

        # 将检测结果绘制到图像上
        result_img = np.squeeze(results.render())

        # 生成一个唯一的文件名
        unique_filename = str(uuid.uuid4()) + '.jpg'

        # 保存图片到服务器路径
        save_dir = os.path.join('project','yolov5', 'result')
        save_path = os.path.join(save_dir, unique_filename)
        cv2.imwrite(save_path, result_img)
    except Exception as e:
        print(str(e))
        return JsonResponse({
            'code':1,
            'message':'网络问题，切换网络环境重试一下'
        })

    # 返回检测结果和图像的文件路径
    return JsonResponse({
        'code': 0,
        'message': '检测成功',
        'data': {
            'detections': detections,
            'filename': save_path  # 返回图片路径
        }
    })

# 本地detect.py
def detect(file_path,filename):
    try:
        weights_path = './project/yolov5/runs/train/exp11/weights/last.pt'
        command = [
            'python', './project/yolov5/detect.py',
            '--source', file_path,  # 输入文件路径
            '--weights', weights_path,  # 模型权重路径
            '--exist-ok'  # 如果文件存在则覆盖
        ]
        result = subprocess.run(command,capture_output=True,text=True)
        print("stdout:", result.stdout)
        print("stderr:", result.stderr)
        delete(file_path)

        source_path = os.path.join('project', 'yolov5', 'result', filename)
        destination_path = os.path.join('vue', 'public', 'result',filename)
        shutil.move(source_path, destination_path)
        return JsonResponse({
            'code': 0,
            'message': '检测成功',
            'data': {
                'filename': filename,  # 返回结果图像的路径
            }
        })
    except Exception as e:
        return JsonResponse({
            'code': 1,
            'message': f'出现错误: {str(e)}',
        })



def delete(file_path):
    try:
        if not os.path.exists(file_path):
            return JsonResponse({
                'code': 1,
                'message': '文件不存在'
            })
        os.remove(file_path)
        return JsonResponse({
            'code': 0,
            'message': '文件删除成功'
        })
    except Exception as e:
        return JsonResponse({
            'code': 1,
            'message': '删除文件失败',
            'data': str(e)
        })