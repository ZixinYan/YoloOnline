<template>
  <div id="app">
    <!-- 主容器 -->
    <div class="container">
      <!-- 左侧面板 -->
      <div class="panel left-panel">
        <form @submit.prevent="handleSubmit">
          <div class="form-group">
            <label for="model">Model:</label>
            <el-select v-model="yolov5.model" placeholder="选择模型" class="select-box">
              <el-option label="模型1" value="model1"></el-option>
              <el-option label="模型2" value="model2"></el-option>
              <el-option label="模型3" value="model3"></el-option>
            </el-select>
          </div>
          <button type="submit" class="submit-btn" @click="instant()">即时识别</button>
          <button type="submit" class="submit-btn" @click="uploadFile()">图片识别</button>
        </form>
      </div>

      <!-- 垂直拖动条 -->
      <div class="vertical-divider" @mousedown="startResizeHorizontal"></div>

      <!-- 右侧面板 -->
      <div class="panel right-panel">
        <div class="section top-section">
          <div class="operations">
            <h1 id="title">基于yolov5的目标检测</h1>
            <div class="operations2">
                <button class="clear-btn" @click="clearInputs()">清除</button>
                <button @click="handleFileUpload" class="upload_btn">选择图片</button>
            </div>
          </div>
            <div id="image-container">
                  <img class="image" :src="yolov5.filename" />
            </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import request from '@/utils/request.js';
import useTokenStore from '@/pinia/token.js'
import { detectImage, detectInstant} from '@/api/yolov5'
const tokenStore = useTokenStore();
export default {
  name: "ColumnPermutationCipher",
  data() {
    return {
      yolov5: {
        filename:'',
        model:'',
      },
    };
  },
  methods: {
    // 打开配置弹窗
    openConfigModal() {
      this.configModalVisible = true;
    },
    closeConfigModal() {
      this.configModalVisible = false;
    },
    submitConfig() {
      this.closeConfigModal();
    },
    async handleFileUpload() {
    if (window.showOpenFilePicker) {
        const [fileHandle] = await window.showOpenFilePicker(); // 浏览器文件选择
        const file = await fileHandle.getFile();
        this.selectedFile = file;
        this.$message.success("文件上传成功" + "  " + this.selectedFile.name);
    } else {
      // 如果不支持现代 API，使用备用方案
      const fileInput = document.createElement("input");
      fileInput.type = "file";
      fileInput.style.display = "none";
      document.body.appendChild(fileInput);

      // 监听文件选择事件
      fileInput.addEventListener("change", (event) => {
        const files = event.target.files;
        if (files && files.length > 0) {
          this.selectedFile = files[0];
          this.$message.success("文件上传成功: " + this.selectedFile.name);
        } else {
          this.$message.error("未选择文件");
          this.selectedFile = null;
        }
        document.body.removeChild(fileInput); // 移除临时元素
      });

      fileInput.click(); // 触发文件选择
    }
  },


  clearInputs() {
      this.yolov5.model = '';
      this.yolov5.filename = '';
      this.selectedFile = null;
      document.getElementById("image").src = "";
    },

    startResizeHorizontal(event) {
      // 开始拖动水平分隔条
      this.resizing = true;
      this.resizingDirection = "horizontal";
      this.startX = event.clientX;
      this.startWidth = this.$el.querySelector(".left-panel").offsetWidth;
      document.addEventListener("mousemove", this.handleResize);
      document.addEventListener("mouseup", this.stopResize);
    },
    handleResize(event) {
      if (!this.resizing) return;
      if (this.resizingDirection === "horizontal") {
        const deltaX = event.clientX - this.startX;
        const newWidth = this.startWidth + deltaX;
        this.$el.querySelector(".left-panel").style.width = `${newWidth}px`;
      } else if (this.resizingDirection === "vertical") {
        const deltaY = event.clientY - this.startY;
        const newHeight = this.startHeight + deltaY;
        this.$el.querySelector(".top-section").style.height = `${newHeight}px`;
      }
    },
    stopResize() {
      this.resizing = false;
      this.resizingDirection = null;
      document.removeEventListener("mousemove", this.handleResize);
      document.removeEventListener("mouseup", this.stopResize);
    },


    // 后端交互
    async uploadFile() {
      if (!this.selectedFile) {
        this.$message.error("Please select a file first.");
        return;
      }
      const formData = new FormData();
      formData.append("file", this.selectedFile);
      try {
        const res1 = await request.post("/yolov5/upload", formData, {
          headers: {
            "Content-Type": "multipart/form-data",
            "Authorization": tokenStore.getToken(),
          },
        });
        this.yolov5.filename = res1.data.filename;
        this.$message.success("程序正在运行")
        const res = await detectImage(this.yolov5);
        if(res.code == 0){
          this.$message.success("程序运行结束");
          this.yolov5.filename = "/result/" + res.data.filename;
        }
        console.log(this.yolov5.filename)

      } catch (error) {
        this.$message.error(`${error.message}`);
        return null;
      }

    },

    async instant(){
      const res = await detectInstant();
      if(res.code == 1){
        this.$message.error("网络连接不佳")
      }else{
        this.$message.success("程序正在启动，请稍后");
      }
    }
  },

};
</script>

<style scoped>
#app {
  height: 100vh;
  display: flex;
  background-color: #121212;
  color: #ffffff;
  overflow: hidden; /* 禁止滚动条 */
}

.container {
  display: flex;
  width: 100%;
  height: 100%;
}

.panel {
  display: flex;
  flex-direction: column;
  padding: 10px;
  background-color: rgba(0, 0, 0, 0.8);
  border: 2px solid #00bfff;
  border-radius: 8px;
  overflow: hidden;
  gap: 10px; /* 添加面板内子元素间隙 */
}

/* 左侧面板 */
.left-panel {
  width: 30%; /* 左侧面板宽度 */
  padding: 30px;
}

.left-panel .form-group {
  margin-bottom: 15px;
  margin-right: 30px;
}

.left-panel .form-group label {
  display: block;
  margin-bottom: 8px;
  margin-right: 10px;
  font-weight: bold;
  font-size: 14px;
  color: #00bfff;
  text-shadow: 1px 1px 2px #000;
}

.left-panel .form-group el-select {
  width: 100%;
  padding: 12px 15px;
  margin-right: 10px;
  border: 1px solid #00bfff;
  border-radius: 6px;
  background-color: #1c1c1c;
  color: #ffffff;
  font-size: 14px;
  outline: none;
  transition: all 0.3s ease;
}

.left-panel .form-group el-select{
  border-color: #00e6ff;
  box-shadow: 0 0 8px rgba(0, 230, 255, 0.8);
}

.operations {
  margin-top: -10px;
  margin-bottom: 10px;
  display: flex;
  justify-content: space-between;
  gap: 10px; /* 添加间隙 */
}

.operations2 {
  display: flex;
  gap: 10px; /* 按钮之间的间距 */
}


/* 按钮样式 */
button {
  cursor: pointer;
  font-size: 14px;
  font-weight: bold;
  padding: 10px 20px;
  border: none;
  border-radius: 6px;
  color: #121212;
  background-color: #00bfff;
  transition: all 0.3s ease;
}

button:hover {
  background-color: #00a5e0;
  transform: translateY(-2px);
  box-shadow: 0 6px 8px rgba(0, 0, 0, 0.5);
}

button:active {
  background-color: #008db8;
  transform: translateY(1px);
  box-shadow: inset 0 4px 6px rgba(0, 0, 0, 0.6);
}



.cancel-btn:hover {
  background-color: #666;
}

.cancel-btn:active {
  background-color: #333;
}

.left-panel .form-group input {
  margin-bottom: 10px; /* 添加下边距，增加间距 */
}

.submit-btn {
  width: 95%; /* 按钮宽度占满 */
  margin-bottom: 10px; /* 添加下边距 */
}

.submit-btn2 {
  width: calc(50% - 10px); /* 按钮宽度占50%减去间隙的一半 */
  margin: 0 5px 10px 5px; /* 左右间距 5px，下边距 10px */
  display: inline-block; /* 使按钮在同一行排列 */
  text-align: center; /* 居中文本 */
  padding: 10px 0; /* 增加内边距 */
  box-sizing: border-box; /* 确保宽度包括内边距和边框 */
}

/* 上传文件按钮 */
.upload-btn {
  cursor: pointer;
  font-size: 14px;
  font-weight: bold;
  padding: 12px 20px;
  border: none;
  border-radius: 6px;
  color: #121212;
  background-color: #00bfff;
  transition: all 0.3s ease;
}

.upload-btn:hover {
  background-color: #00a5e0;
  transform: translateY(-2px);
  box-shadow: 0 6px 8px rgba(0, 0, 0, 0.5);
}

.upload-btn:active {
  background-color: #008db8;
  transform: translateY(1px);
  box-shadow: inset 0 4px 6px rgba(0, 0, 0, 0.6);
}

.upload-btn input[type="file"] {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  opacity: 0;
  cursor: pointer;
}

/* 清除按钮 */
.clear-btn {
  cursor: pointer;
  font-size: 14px;
  font-weight: bold;
  padding: 12px 20px;
  border: none;
  border-radius: 6px;
  color: #121212;
  background-color: #00bfff;
  transition: all 0.3s ease;
}

.clear-btn:hover {
  background-color: #ff2e2e;
}

.vertical-divider {
  width: 3px; /* 增加宽度，便于操作 */
  background-color: #00bfff;
  cursor: ew-resize;
  transition: background-color 0.2s;
}
.vertical-divider:hover {
  background-color: #00e6ff; /* 提示用户拖动 */
}

/* 右侧面板 */
.right-panel {
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  gap: 10px; /* 添加间隙 */
}

.section {
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  padding: 15px;
  background-color: rgba(20, 20, 20, 0.9);
  border-radius: 6px;
  overflow: hidden;
}

.horizontal-divider {
  height: 5px; /* 增加高度，便于操作 */
  background-color: #00bfff;
  cursor: ns-resize;
  transition: background-color 0.2s;
}
.horizontal-divider:hover {
  background-color: #00e6ff; /* 提示用户拖动 */
}


textarea {
  flex-grow: 1;
  padding: 15px;
  background-color: #1c1c1c;
  color: white;
  border: 1px solid #00bfff;
  border-radius: 6px;
  resize: none;
  font-size: 14px;
  outline: none;
  transition: all 0.3s ease;
}

textarea:focus {
  border-color: #00e6ff;
  box-shadow: 0 0 8px rgba(0, 230, 255, 0.8);
}

/* 弹窗样式 */
.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.8);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-content {
  background-color: #121212;
  padding: 30px;
  border: 2px solid #00bfff;
  border-radius: 8px;
  width: 400px;
  box-shadow: 0 10px 15px rgba(0, 0, 0, 0.5);
}

.modal-content h3 {
  color: #00e6ff;
  font-size: 18px;
  margin-bottom: 20px;
  text-align: center;
  text-shadow: 1px 1px 2px #000;
}

.modal-content .form-group {
  margin-bottom: 15px;
  margin-right: 20px;
}

.modal-content .form-group label {
  color: #00bfff;
  font-size: 14px;
}

.modal-content input {
  width: 100%;
  padding: 10px;
  margin-bottom: 10px;
  border-radius: 6px;
  border: 1px solid #00bfff;
  background-color: #1c1c1c;
  color: white;
}

.modal-content input:focus {
  border-color: #00e6ff;
  box-shadow: 0 0 6px rgba(0, 230, 255, 0.8);
}

#output {
  caret-color: transparent; /* 隐藏光标 */
  resize: none; /* 禁止手动调整大小 */
  background-color: none;
  color: #333; /* 设置文本颜色 */
  border: 1px solid #ccc; /* 设置边框颜色 */
  padding: 10px; /* 添加内边距 */
  font-size: 14px; /* 设置字体大小 */
}

.copy-container {
  position: relative;
  display: flex;
  align-items: center;
  gap: 10px; /* 按钮和文本框的间距 */
}

#output {
  resize: none; /* 禁止调整大小 */
  background-color: #121212; /* 深色背景 */
  color: #00bfff; /* 亮蓝色文字 */
  border: 1px solid #00bfff; /* 边框为亮蓝色 */
  padding: 10px;
  font-size: 14px;
  border-radius: 6px;
  caret-color: transparent; /* 隐藏光标 */
  outline: none;
  font-family: 'Courier New', Courier, monospace; /* 程序员风格字体 */
}

.copy-btn {
  cursor: pointer;
  font-size: 14px;
  font-weight: bold;
  padding: 10px 15px;
  margin-top: -5px;
  margin-bottom: 10px;
  border: none;
  border-radius: 6px;
  color: #fff;
  background-color: #00bfff;
  transition: all 0.3s ease;
}

.copy-btn:hover {
  background-color: #00a5e0;
  transform: translateY(-2px);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.5);
}

.copy-btn:active {
  background-color: #008db8;
  transform: translateY(1px);
  box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.6);
}

#title {
  font-size: 18px; /* 字体大小 */
  font-weight: bold; /* 加粗 */
  margin: 0; /* 去掉默认外边距 */
  padding: 0; /* 去掉内边距 */
  line-height: 40px; /* 设置与按钮一致的高度 */
}

.image {
  width: 100%;  /* 图片宽度充满容器 */
  height: auto;  /* 高度自适应 */
  object-fit: contain;  /* 图片保持比例且不超出容器 */
  border-radius: 6px;  /* 可选：为图片添加圆角 */
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);  /* 可选：给图片添加阴影 */
}

</style>
