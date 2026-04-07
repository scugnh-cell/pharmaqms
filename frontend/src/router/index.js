import { createRouter, createWebHistory } from "vue-router";

const routes = [
  {
    path: "/",
    redirect: "/change-management",
  },
  {
    path: "/change-management",
    name: "ChangeManagement",
    component: () => import("@/views/ChangeManagement/index.vue"),
    meta: { name: "变更管理", type: "quality" },
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.afterEach((to) => {
  document.title = (to.meta && to.meta.name) ? `${to.meta.name} - PharmaQMS` : "PharmaQMS";
});

export default router;
