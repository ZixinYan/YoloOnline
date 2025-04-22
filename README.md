## YoloOnline: 基于 YOLOv5 的在线检测系统

## 功能特点
- 使用 YOLOv5 进行目标检测。
- 使用opencv进行在线检测，也支持调用三方摄像头进行检测
- 使用 Django 和 Vue.js 开发在线控制台。

### 安装与配置
1. 克隆项目：  
   ```bash
   git clone https://github.com/ZixinYan/YoloOnline.git
   ```
2. 启动应用：
   ```bash
   python manage.py runserver
   ```

### 项目截图
![页面](/doc/panel.png)
![图片检测结果](/result.jpg)

### 其他
学yolov5的时候做的一个小项目，其实搭建好了Django框架，内容还可以自行二开扩展，数据集可以进行训练后直接使用，也支持选择不同模型进行检测

---
