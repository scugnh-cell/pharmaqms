<template>
  <div class="app-layout">
    <el-container class="top-container">
      <el-header>
        <TopBar />
      </el-header>
      <el-container class="main-container">
        <MenuBar />
        <el-container>
          <el-main>
            <router-view />
          </el-main>
          <el-footer>
            <el-text>PharmaQMS v1.0</el-text>
          </el-footer>
        </el-container>
      </el-container>
    </el-container>
    <el-backtop :right="16" :bottom="60" />
  </div>
</template>

<script setup>
import TopBar from "./views/Layout/TopBar.vue";
import MenuBar from "./views/Layout/MenuBar.vue";
</script>

<style>
.app-layout {
  height: 100%;
  width: 100%;
  position: absolute;
  top: 0;
  left: 0;
}
.top-container {
  height: 100%;
}
.top-container > .el-header {
  padding: 0 !important;
  height: 56px !important;
}
.main-container {
  max-height: calc(100vh - 56px);
}
.main-container .el-main {
  height: 100%;
  background: #eff3fa;
}
.main-container .el-footer {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 34px;
  background-color: #eff3fa;
  color: #8c8c8c;
}
</style>
