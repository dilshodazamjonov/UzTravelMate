<template>
  <div class="registration-form">
    <el-form :model="form" ref="formRef" label-width="140px">
      <el-form-item label="First Name">
        <el-input v-model="form.firstName" placeholder="Enter your first name" />
      </el-form-item>

      <el-form-item label="Last Name">
        <el-input v-model="form.lastName" placeholder="Enter your last name" />
      </el-form-item>

      <el-form-item label="Age">
        <el-input v-model="form.age" type="number" placeholder="Enter your age" />
      </el-form-item>

      <el-form-item label="Phone">
        <el-input v-model="form.phone" placeholder="Enter your phone number" />
      </el-form-item>

      <el-form-item label="Email">
        <el-input v-model="form.email" type="email" placeholder="Enter your email" />
      </el-form-item>

      <el-form-item label="Password">
        <el-input v-model="form.password" type="password" placeholder="Enter your password" show-password />
      </el-form-item>

      <el-form-item label="Confirm Password">
        <el-input v-model="form.confirmPassword" type="password" placeholder="Confirm your password" show-password />
      </el-form-item>

      <el-form-item label="Avatar URL">
        <el-input v-model="form.avatar" placeholder="Enter avatar image URL" />
      </el-form-item>

      <el-form-item>
        <el-button type="primary" @click="submitForm">Register</el-button>
      </el-form-item>

      <div class="register">
        <span class="account-info">Already have an account?</span>
        <el-button class="signin-btn" link @click="$router.push('/auth/')">Sign In</el-button>
      </div>
    </el-form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import axios from 'axios'

const formRef = ref()
const form = ref({
  firstName: '',
  lastName: '',
  age: '',
  phone: '',
  email: '',
  password: '',
  confirmPassword: '',
})

const submitForm = async () => {
  if (form.value.password !== form.value.confirmPassword) {
    ElMessage.error('Passwords do not match!')
    return
  }

  try {
    const response = await axios.post(
      'https://myblogapi.hamkasb.uz/auth/registration',
      form.value,
      {
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        }
      }
    )
    ElMessage.success('Successfully registered!')
    console.log(response.data)
  } catch (error) {
    ElMessage.error('Error occurred: ' + (error.response?.data?.message || error.message))
  }
}
</script>

<style scoped>
.registration-form {
  max-width: 500px;
  margin: 40px auto;
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  background-color: #fff;
}

.register {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 10px;
}

.account-info {
  font-size: 14px;
  color: #333;
}

.signin-btn {
  margin-left: 5px;
  font-size: 14px;
  color: #007bff;
  text-decoration: underline;
  cursor: pointer;
}

.signin-btn:hover {
  color: #0056b3;
}
</style>
