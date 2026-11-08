import axios from 'axios';

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE,
  headers: { 'Content-Type': 'application/json' },
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

export const itemsApi = {
  getAll: (params) => api.get('/api/items', { params }),
  getById: (id) => api.get(`/api/items/${id}`),
  create: (data) => api.post('/api/items', data),
  update: (id, data) => api.put(`/api/items/${id}`, data),
  delete: (id) => api.delete(`/api/items/${id}`),
  getRecommendations: (id) => api.get(`/api/recommendations/${id}`),
};

export const searchApi = {
  textSearch: (query, filters) => api.post('/api/search/text', { query, ...filters }),
  imageSearch: (formData) => api.post('/api/search/image', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  }),
};

export const contributionsApi = {
  submit: (formData) => api.post('/api/contributions', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  }),
  getAll: () => api.get('/api/contributions'),
  approve: (id) => api.post(`/api/contributions/${id}/approve`),
  reject: (id, notes) => api.post(`/api/contributions/${id}/reject`, { notes }),
};

export const authApi = {
  login: (creds) => api.post('/api/auth/login', creds),
  register: (data) => api.post('/api/auth/register', data),
  me: () => api.get('/api/auth/me'),
};

export const regionsApi = {
  getAll: () => api.get('/api/regions'),
  getCategories: () => api.get('/api/categories'),
};

export const aiApi = {
  categorize: (formData) => api.post('/api/ai/categorize', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  }),
};

export const adminApi = {
  getStats: () => api.get('/api/admin/stats'),
  getItems: (params) => api.get('/api/admin/items', { params }),
  updateStatus: (id, status) => api.put(`/api/admin/items/${id}/status`, { status }),
};

export default api;
