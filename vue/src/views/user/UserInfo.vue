<script setup>
import { ref } from 'vue'
import useUserInfoStore from '@/pinia/userInfo.js'
const userInfoStore = useUserInfoStore()
const userInfo = ref({...userInfoStore.user})

const rules = {
    phone_number: [
        { required: true, message: '请输入手机号', trigger: 'blur' },
        {
            pattern: /^\S{11}$/,
            message: '手机号格式不正确',
            trigger: 'blur'
        }
    ],
    email: [
        { required: true, message: '请输入用户邮箱', trigger: 'blur' },
        { type: 'email', message: '邮箱格式不正确', trigger: 'blur' }
    ]
}
import { updateUserInfoService } from '@/api/user.js'
import { ElMessage } from 'element-plus'

const updateUserInfo = async () => {
    if(userInfo.value.phone_number === '' || userInfo.value.email === ''){
        ElMessage.error('请填写完整信息')
        return
    }else if(userInfo.value.phone_number === userInfoStore.user.phone_number && userInfo.value.email === userInfoStore.user.email){
        ElMessage.error('信息未修改')
        return
    }else if(userInfo.value.phone_number.length !== 11){
        ElMessage.error('手机号格式不正确')
        return
    }else{
      await updateUserInfoService(userInfo.value)
      ElMessage.success('修改成功')
      userInfoStore.setUser(userInfo.value)
    }

}
</script>
<template>
    <el-card class="page-container">
        <template #header>
            <div class="header">
                <span>基本资料</span>
            </div>
        </template>
        <el-row>
            <el-col :span="12">
                <el-form :model="userInfo" :rules="rules" label-width="100px" size="large">
                    <el-form-item label="登录名称" class="header">
                        <el-input v-model="userInfo.username" disabled></el-input>
                    </el-form-item>
                    <el-form-item label="手机号" prop="phone_number" class="header">
                        <el-input v-model="userInfo.phone_number"></el-input>
                    </el-form-item>
                    <el-form-item label="用户邮箱" prop="email" class="header">
                        <el-input v-model="userInfo.email"></el-input>
                    </el-form-item>
                    <el-form-item>
                        <el-button type="primary" @click="updateUserInfo()">提交修改</el-button>
                    </el-form-item>
                </el-form>
            </el-col>
        </el-row>
    </el-card>
</template>

<style lang="scss" scoped>
.header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    user-select: none;
    .extra {
        display: flex;
        align-items: center;
        user-select: none;
    }
}
</style>
