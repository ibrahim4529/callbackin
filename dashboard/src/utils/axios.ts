import axios from 'axios';
import { useCookies } from '@vueuse/integrations/useCookies';

const BASE_URL = import.meta.env.VITE_BASE_URL;
const { get } = useCookies()

const axiosInstance = axios.create({
    baseURL: BASE_URL,
});


axiosInstance.interceptors.request.use(
    (config) => {
        const token = get('token');
        console.log(token)
        if (token) {
            config.headers['Authorization'] = `Bearer ${token}`;
        }
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

export default axiosInstance;