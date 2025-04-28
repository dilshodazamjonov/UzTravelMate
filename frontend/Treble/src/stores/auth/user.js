import { api } from "@/helpers/api";
import { ElMessage } from "element-plus";
import { defineStore } from "pinia";
import { ref } from "vue";
import router from "@/router";

export const authStore = defineStore('authStore', () => {
  const user = ref({})
  const isAuth = ref(false)

  const login = async loginUser => {
    const { data } = await api.post('/auth/login', loginUser).catch(err => {
      console.error(err)
      ElMessage.error(err.response?.data?.message)
    })
    console.log(data);
    sessionStorage.setItem('token', data.token)
    user.value = { ...data.user }
    isAuth.value = true
    router.push({ name: 'home' })
  }

  const logout = () => {
    user.value = {}
    isAuth.value = false
    sessionStorage.removeItem('token')
    router.push({ name: 'sign-in' })
  }

  const checkUser = async () => {
    const {data} = await api.get('auth/checkuser').catch(() => {
      logout()
    })
    console.log(data);
    
    user.value = {...data.user}
    isAuth.value = true
  }

  return {
    user,
    isAuth,
    login,
    logout,
    checkUser,
  }
})