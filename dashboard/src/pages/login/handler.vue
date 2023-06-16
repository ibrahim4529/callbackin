<script setup lang="ts">
// import { useLocalStorage } from '@vueuse/core';
import { useCookies } from '@vueuse/integrations/useCookies';
import axiosInstance from '../../utils/axios';
const { set } = useCookies();
const TOKEN = new URLSearchParams(window.location.search).get('token');
set('token', TOKEN);

const getUserName = async () => {
    const response = await axiosInstance.get('/auth/me');
    return response.data
};

getUserName().then((data) => {
    console.log(data);
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