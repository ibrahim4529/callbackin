<script setup lang="ts">
import { Icon } from '@iconify/vue';
const callbacks = [
    {
        name: 'Callback 1',
        path: '0xjdwjwkhkdbwkdbkwndkwdnw',
        description: 'Callback 1 description',
        local_endpoint: 'http://localhost:3000/callback/0xjdwjwkhkdbwkdbkwndkwdnw',
        is_running: true,
    },
    {
        name: 'Callback 2',
        path: '0xjdwjwkhkdbwkdbkwndkwdnw',
        description: 'Callback 2 description',
        local_endpoint: 'http://localhost:3000/callback/0xjdwjwkhkdbwkdbkwndkwdnw',
        is_running: false,
    }
]
</script>
<template>
    <div class="flex flex-col">
        <nav class="navbar bg-blue-500 px-10">
            <div class="flex-1">
                Callbackin
            </div>
            <div class="flex-none">
                <a href="#" class="btn btn-primary">Logout</a>
            </div>
        </nav>
        <div class="flex flex-row w-full px-10 mt-2">
            <!-- sidebar for list of callback -->
            <div class="w-[30%] pr-4 h-screen">
                <div class="flex flex-col">
                    <button class="btn btn-primary">
                        <Icon icon="mdi:plus" />
                        Tambah Callback
                    </button>

                    <!-- list of callback -->
                    <div class="flex flex-col gap-y-4 mt-4">
                        <div :class="`card p-4 rounded-md ${callback.is_running ? 'bg-green-700': 'bg-red-600'}`" v-for="callback in callbacks">
                            <div class="flex">
                                <div>
                                    <p>Nama: {{ callback.name }}</p>
                                    <p>Path: {{ callback.path }}</p>
                                    <p>Deskripsi: {{ callback.description }}</p>
                                    <p>Local Endpoint: {{ callback.local_endpoint }}</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="w-[70%] bg-red-200 h-screen">
                Hallo
            </div>
        </div>
    </div>
</template>