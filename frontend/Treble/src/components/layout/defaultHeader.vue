<template>
  <el-header>
    <div class="header_nav">
      <img @click="$router.push('/')" src="/src/img/treble_logo.png" alt="treble_logo" />
      <!-- <div class="link">
        <router-link
          v-for="link of mainMenu"
          :key="link.name"
          :to="{ name: link.name }"
          :class="`link ${link.name} ${route.name === link.name ? 'active' : ''}`"
        >
          <component :is="link?.meta?.icon" />
          {{ link?.meta?.title }}
        </router-link>
      </div> -->
      <div class="login_user">
        <el-icon @click="$router.push('/loginUser')" class="user_icon"><user /></el-icon>
      </div>
    </div>
  </el-header>
  <el-main>
    <div class="info_box">
      <!-- <div class="info_one">
        <img :src="infoImg" alt="info_img" />
        <div class="info_text">
          Lorem ipsum dolor sit amet consectetur adipisicing elit. Ducimus, illum! Iusto accusantium
          dignissimos officia libero a dolor sequi, dolorum quae fuga eius repudiandae corporis
          minus amet aliquam iure dolorem quibusdam. Lorem ipsum dolor sit amet consectetur
          adipisicing elit. Ducimus, illum! Iusto accusantium dignissimos officia libero a dolor
          sequi, dolorum quae fuga eius repudiandae corporis minus amet aliquam iure dolorem
          quibusdam. Lorem ipsum dolor sit amet consectetur adipisicing elit. Ducimus, illum! Iusto
          accusantium dignissimos officia libero a dolor sequi, dolorum quae fuga eius repudiandae
          corporis minus amet aliquam iure dolorem quibusdam.
        </div>
      </div> -->
      <div class="info_one">
        <div class="info_text">
          <img src="@/img/info.jpg" alt="info_img" />
          Mana rasm to‘g‘ri ko‘rinmoqda!
        </div>
      </div>
      <div class="info_two">
        <img src="/src/img/treble_logo.png" alt="info_img" />
        <div class="info_text">
          Lorem ipsum dolor sit amet consectetur adipisicing elit. Ducimus, illum! Iusto accusantium
          dignissimos officia libero a dolor sequi, dolorum quae fuga eius repudiandae corporis
          minus amet aliquam iure dolorem quibusdam. Lorem ipsum dolor sit amet consectetur
          adipisicing elit. Ducimus, illum! Iusto accusantium dignissimos officia libero a dolor
          sequi, dolorum quae fuga eius repudiandae corporis minus amet aliquam iure dolorem
          quibusdam. Lorem ipsum dolor sit amet consectetur adipisicing elit. Ducimus, illum! Iusto
          accusantium dignissimos officia libero a dolor sequi, dolorum quae fuga eius repudiandae
          corporis minus amet aliquam iure dolorem quibusdam.
        </div>
      </div>
    </div>
  </el-main>
</template>

<script setup>
import { useRoute } from 'vue-router'
const route = useRoute()
</script>

<style lang="scss">
@import '@/styles/layout/defaultHeader.scss';

img {
  cursor: pointer;
  width: 100px;
  height: 100px;
  border-radius: 50%;
  filter: brightness(0) invert(1);
}

.login_text {
  font-size: 17px;
  color: #fff;
}

.login_user {
  display: flex;
  gap: 10px;
  align-items: center;
  cursor: pointer;
  font-size: 20px;
  color: #fff;
}

.info_one,
.info_two {
  background-color: #000;
}

.user_icon {
  font-size: 28px;
  border-radius: 50%;
  transition: ease 0.3s;
  padding: 4px;
}

.user_icon:hover {
  background-color: #1c3d5f;
}

.link {
  display: flex;
  align-items: center;
  gap: 5px;
}

.icon {
  font-size: 18px;
}
</style>
