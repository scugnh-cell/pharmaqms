<template>
  <el-aside width="180px">
    <el-menu :default-active="activeIndex" router class="menu-container">
      <el-menu-item index="/change-management">
        <el-icon><Document /></el-icon>
        <span>变更管理</span>
      </el-menu-item>
    </el-menu>
  </el-aside>
</template>

<script setup>
import { computed } from "vue";
import { useRoute } from "vue-router";

const route = useRoute();
const activeIndex = computed(() => route.path);
</script>

<style scoped>
.menu-container {
  height: 100%;
}
</style>
