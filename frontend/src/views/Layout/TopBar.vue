<template>
  <el-menu class="top-bar" mode="horizontal" :ellipsis="false">
    <el-menu-item index="0" @click="$router.push('/')">
      <span style="font-size: 20px; font-weight: bold; color: #375196;">
        PharmaQMS
      </span>
    </el-menu-item>
    <div class="flex-grow" />
    <el-menu-item index="1" disabled>
      <span style="color: #999; font-size: 13px;">医药质量管理平台</span>
    </el-menu-item>
  </el-menu>
</template>

<style scoped>
.top-bar {
  height: 56px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  z-index: 100;
}
.top-bar > .el-menu-item {
  border-bottom: none !important;
}
.flex-grow { flex-grow: 1; }
</style>
