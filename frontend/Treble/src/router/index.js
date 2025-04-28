import { createRouter, createWebHistory } from 'vue-router'
// import { mainMenu } from './nav/menu'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'dashboardLayout',
      // component: () => import('@/layouts/dashboardLayout.vue'),
      // children: [
      //   ...mainMenu,
      // ]
    },
    {
      path: '/auth',
      name: 'authLayout',
      component: () => import('@/layouts/authLayout.vue'),
      children: [
        {
          path: '',
          name: 'sign-in',
          component: () => import('@/views/auth/signIn.vue'),
          meta: {
            title: 'Tizimga kirish'
          }
        }
      ]
    },
    {
      path: '/registration',
      name: 'registerLayout',
      component: () => import('@/layouts/registrationLayout.vue'),
    }
  ],
})


// import { authStore } from '@/stores/auth/user'

// router.beforeEach(async (to, from, next) => {
//   const store = authStore()
//   document.title = `My_blog | ${to?.meta?.title}`
//   if (['sign-in', 'authLayout'].includes(to.name) || store.isAuth) {
//     next()
//   } else {
//     if (sessionStorage.key('token')) {
//       await store.checkUser()
//       next()
//     } else {
//       next({ name: 'sign-in' })
//     }
//   }
// })


export default router
