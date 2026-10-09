import axios from 'axios'
const http = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:5000/api',
  headers: { 'Content-Type': 'application/json' },
  timeout: 10000,
})
http.interceptors.response.use(
  response => response,
  error => Promise.reject(new Error(error.response?.data?.error || 'No fue posible comunicarse con el servidor')),
)
export default http
