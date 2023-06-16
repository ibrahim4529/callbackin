<script setup lang="ts">
import { useRouter } from 'vue-router';
import axiosInstance from '../../utils/axios';
import { Urls } from '../../utils/conts';

const router = useRouter();
const TOKEN = new URLSearchParams(window.location.search).get('token');

localStorage.setItem('token', `${TOKEN}`);

const getUserData = async () => {
    const response = await axiosInstance.get(
        Urls.ME
    );
    return response.data
};

getUserData().then((data) => {
    localStorage.setItem('userInfo', JSON.stringify(data));
    router.push('/dashboard');
});


</script>

<template>
    <div>
        <!-- Show Loading icon center bootstrap 5 for 10 secvond  -->
        <div class="d-flex justify-content-center align-items-center" style="height: 100vh;">
            <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
        </div>
    </div>
</template>