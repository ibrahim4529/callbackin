import axios from 'axios';
import { useLocalStorage } from '@vueuse/core';
import { BASE_URL } from './conts';

const axiosInstance = axios.create({
    baseURL: BASE_URL,
});

axiosInstance.interceptors.request.use(
    (config) => {
        const token = useLocalStorage('token', null).value;
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