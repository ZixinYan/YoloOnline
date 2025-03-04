<!-- eslint-disable no-unused-vars -->
<script setup>
import { ref } from 'vue';
import { onMounted } from 'vue';
import { useRouter } from 'vue-router';

// 加载状态
const isLoading = ref(false); // 控制转圈动画显示
const router = useRouter();

// 路由钩子绑定加载状态
onMounted(() => {
  router.beforeEach((to, from, next) => {
    isLoading.value = true; // 显示加载动画
    next();
  });

  router.afterEach(() => {
    isLoading.value = false; // 隐藏加载动画
  });
});
</script>

<template>
  <!-- 加载动画 -->
  <div v-if="isLoading" class="loading-overlay">
    <div class="spinner"></div>
  </div>

  <!-- 路由视图 -->
  <router-view></router-view>
</template>

<style scoped>
/* 加载动画覆盖层 */
.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(255, 255, 255, 0.8); /* 半透明白色背景 */
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
}

/* 转圈动画样式 */
.spinner {
  width: 50px;
  height: 50px;
  border: 5px solid #ccc; /* 灰色边框 */
  border-top: 5px solid #007bff; /* 蓝色边框 */
  border-radius: 50%;
  animation: spin 1s linear infinite; /* 旋转动画 */
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}
</style>
