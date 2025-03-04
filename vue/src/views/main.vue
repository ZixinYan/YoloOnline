<!-- eslint-disable vue/multi-word-component-names -->
<template>
  <div id="app" class="text-container">
    <h1 id="title">{{ welcomeMessage }}</h1>
    <p>{{ description }}</p>
    <el-button type="primary" @click="go">点击查看教程</el-button>

    <!-- 弹窗 -->
    <div v-if="showModal" class="modal-overlay" @click="closeModal">
      <div class="modal-window" @click.stop>
        <p>这是一个弹窗内容。</p>
        <el-button type="success" @click="closeModal">确认</el-button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      welcomeMessage: '',
      description: '',
      showModal: false, // 控制弹窗的显示
    };
  },
  created() {
    this.updateWelcomeMessage();
  },
  methods: {
    updateWelcomeMessage() {
      const currentHour = new Date().getHours();
      if (currentHour < 12) {
        this.welcomeMessage = '早上好，祝您一天好心情';
        this.description = '早晨的阳光充满希望，让我们开始新的一天吧！';
      } else if (currentHour < 18) {
        this.welcomeMessage = '下午好！该好好工作了';
        this.description = '工作的时候别忘记适当休息，保持高效哦！';
      } else {
        this.welcomeMessage = '晚上好，记得早点儿休息';
        this.description = '夜晚是放松的时光，可以读书或者听点音乐。';
      }
    },
    go() {
      this.showModal = true;
    },
    closeModal() {
      this.showModal = false;
    },
  },
};
</script>

<style scoped>
.text-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  text-align: center;
  background: none;
  padding: 20px;
  box-sizing: border-box;
}

h1 {
  font-family: 'Cursive', 'Arial', sans-serif;
  font-style: italic;
  font-size: 50px;
  margin-bottom: 10px;
  color: #3f51b5;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
  user-select: none;
}

p {
  font-size: 18px;
  color: #3f51b5;
  margin-bottom: 40px;
  line-height: 1.5;
}

.el-button {
  font-size: 16px;
  padding: 10px 20px;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.el-button:hover {
  background-color: #1e88e5 !important;
  color: white !important;
  transform: scale(1.05);
}

/* 弹窗背景 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

/* 弹窗窗口 */
.modal-window {
  background: #fff;
  padding: 20px;
  border-radius: 10px;
  text-align: center;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
  z-index: 1001;
  width: 300px;
  max-width: 90%;
}

.modal-window p {
  font-size: 18px;
  color: #333;
  margin-bottom: 20px;
}
</style>
