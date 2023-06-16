<script setup lang="ts">
import { Icon } from '@iconify/vue';
import { Urls } from '../../utils/conts';
</script>

<template>
    <div class="d-flex justify-content-center align-items-center" style="height: 100vh;">
        <a class="btn btn-primary btn-lg" type="button" :href="Urls.LOGIN">
            Login with Github
            <Icon icon="akar-icons:github-fill" class="icon" />
        </a>
    </div>
</template>

<style scoped>
.icon {
    font-size: 32px;
    margin-left: 5px;
}
</style>