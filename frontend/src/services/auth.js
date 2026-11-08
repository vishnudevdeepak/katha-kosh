import { authApi } from './api';

export const getToken = () => localStorage.getItem('token');
export const setToken = (token) => localStorage.setItem('token', token);
export const removeToken = () => localStorage.removeItem('token');
export const isAuthenticated = () => !!getToken();

export const loginUser = async (email, password) => {
  const res = await authApi.login({ username: email, password });
  setToken(res.data.access_token);
  return res.data;
};

export const logoutUser = () => {
  removeToken();
};
