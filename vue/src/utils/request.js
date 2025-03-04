import axios from 'axios';
import { ElMessage } from 'element-plus';
import router from '@/router/index.js';
import { useTokenStore } from '@/pinia/token.js';

const baseURL = '/api';
const instance = axios.create({ baseURL });

instance.interceptors.request.use(
    config => {
        const token = useTokenStore().getToken();
        console.log('当前token:', token);  // 打印token值
        if (token) {
            const encodedToken = encodeURIComponent(token);
            config.headers.Authorization = encodedToken;
        }
        return config;
    },
    err => {
        return Promise.reject(err);
    }
);

// 添加响应拦截器
instance.interceptors.response.use(
    result => {
        if (result.data.code === 0) {
            return result.data;
        } else {
            ElMessage.error(result.data.message ? result.data.message : '服务异常'); // 弹出错误信息
            return Promise.reject(result.data); // 异步的状态转化成失败的状态
        }
    },
    err => {
        if (err.response.status === 401) {
            ElMessage.error('请先登录！');
            router.push('/');
        } else {
            ElMessage.error('服务异常,请重新登录');
            router.push('/');
        }
        return Promise.reject(err); // 异步的状态转化成失败的状态
    }
);

export default instance;
