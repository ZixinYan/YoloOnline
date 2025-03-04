import {createRouter, createWebHistory} from 'vue-router'
import LoginVue from '@/views/Login.vue'
import LayoutVue from '@/views/Layout.vue'

// 1. Define route components.
const routes = [
    {path: '/', component: LoginVue},
    {path:'/findpassword',component:()=>import('@/views/FindPassword.vue')},
    {path: '/page', component: LayoutVue,redirect:'/main',children:[
        {path:'/main',component:()=>import('@/views/main.vue')},
        {path:'/user/avatar',component:()=>import('@/views/user/UserAvatar.vue')},
        {path:'/user/info',component:()=>import('@/views/user/UserInfo.vue')},
        {path:'/user/resetpassword',component:()=>import('@/views/user/UserResetPassword.vue')},
        {path:'/yolov5',component:()=>import('@/views/yolo/yolov5.vue')}
    ]
    },
]

// 2. Create the router instance and pass the `routes` option
const router = createRouter({
    history: createWebHistory(),
    routes:routes
})

// 3. Export the router instance
export default router
