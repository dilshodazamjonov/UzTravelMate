<template>
  <div class="signin">
    <div class="title">Tizimga kirish</div>
    <el-form :model="user" :rules="rules" label-position="top" status-icon ref="form" class="form">
      <el-form-item label="Login" prop="login">
        <el-input>
          <template #prefix>
            <el-icon class="el-input__icon login_input"><User /></el-icon>
          </template>
        </el-input>
      </el-form-item>
      <el-form-item label="Mahfiy kalit" prop="password">
        <el-input>
          <template #prefix>
            <el-icon class="el-input__icon login_input"><Lock /></el-icon>
          </template>
        </el-input>
      </el-form-item>

      <el-button class="login_btn" type="success" @click="login">Kirish</el-button>
    </el-form>
    <div class="register">
      <span class="akk_info">Akkaunt yo'qmi?</span> 
      <button @click="reg_page" class="register_btn">Ro'yxatdan o'ting</button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { authStore } from '@/stores/auth/user'
import { ElMessage } from 'element-plus'

const form = ref(null)
const user = ref({ login: '', password: '' })
const store = authStore()
const router = useRouter()

const rules = {
  login: [{ required: true, message: 'Loginni kiriting', trigger: 'blur' }],
  password: [{ required: true, message: 'Parolni kiriting', trigger: 'blur' }],
}

const login = async () => {
  if (!form.value) return
  form.value.validate(async (valid) => {
    if (valid) {
      try {
        await store.login(user.value)
        ElMessage.success("Tizimga muvaffaqiyatli kirdingiz")
        router.push('/')
      } catch (error) {
        ElMessage.error(error.response?.data?.message || "Login yoki parol xato")
      }
    } else {
      ElMessage.error("Majburiy maydonlarni to'ldiring")
    }
  })
}

const reg_page = () => {
  router.push('/registration')
}
</script>

<style lang="scss" scoped>
.signin {
  background-color: #fff;
  padding: 30px;
  border-radius: 12px;
  display: flex;
  flex-direction: column;
  align-items: center;

  .title {
    font-size: 18px;
    margin-bottom: 20px;
    text-align: center;
    font-weight: 500;
  }
}

.form {
  width: 300px;
}

.akk_info {
  font-size: 14px;
  color: #685f5f;
  margin-top: 10px;
}

.register {
  margin-top: 20px;
}

.register_btn {
  background: none;
  border: none;
  color: #007bff;
  cursor: pointer;
  text-decoration: underline;
  font-size: 14px;
  margin-left: 5px;
}

.register_btn:hover {
  color: #0056b3;
}
</style>
