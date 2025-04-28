<template>
  <el-container>
    <default-header />
    <el-main><router-view /></el-main>
  </el-container>
</template>
<script setup>
import DefaultHeader from '@/components/layout/defaultHeader.vue'
</script>
<style lang="scss">
.el-container {
  display: block;
}
</style>
