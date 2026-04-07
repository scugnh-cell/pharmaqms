import axios from "axios";
import Qs from "qs";
import { ElMessage } from "element-plus";

const service = axios.create({
  baseURL: "",
  timeout: 30 * 1000,
  headers: { "Content-Type": "application/json;charset=UTF-8" },
  paramsSerializer: {
    serialize: function (params) {
      return Qs.stringify(params, { arrayFormat: "repeat" });
    },
  },
});

service.interceptors.response.use(
  (response) => response,
  (error) => {
    ElMessage.error(`请求出错: ${error.message}`);
    return Promise.reject(error);
  }
);

export default service;
