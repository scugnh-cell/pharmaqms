import request from "./axios";

export const getChangeList = (params) =>
  request({ url: "/api/change/list", method: "get", params });

export const getActionList = (params) =>
  request({ url: "/api/change/action/list", method: "get", params });

export const createChange = (data) =>
  request({ url: "/api/change/create", method: "post", data });

export const updateChange = (changeId, data) =>
  request({ url: `/api/change/update/${changeId}`, method: "post", data });

export const deleteChange = (changeId) =>
  request({ url: `/api/change/delete/${changeId}`, method: "post" });

export const addActionItem = (data) =>
  request({ url: "/api/change/action/add", method: "post", data });

export const updateActionItem = (itemId, data) =>
  request({ url: `/api/change/action/update/${itemId}`, method: "post", data });

export const deleteActionItem = (itemId) =>
  request({ url: `/api/change/action/delete/${itemId}`, method: "post" });

export const exportChangeList = (params) =>
  request({ url: "/api/change/export", method: "get", params, responseType: "blob" });
