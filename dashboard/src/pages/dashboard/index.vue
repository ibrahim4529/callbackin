<script setup lang="ts">
import { useLocalStorage } from '@vueuse/core'

const userInfo = useLocalStorage('userInfo', {
    name: '',
    email: '',
})

</script>
<template>
    <!-- bootstrap 5 navbar center item user name -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
        <div class="container-fluid">
            <a class="navbar-brand" href="#">Callbackin</a>
            <!-- shoe user here -->
            <div>
                {{ userInfo.name }}
            </div>
        </div>
    </nav>
    <div>
        <div class="container">
            <div class="row">
                <div class="col-md-4">
                    <div class="card card-primary">
                        <div class="card-header">
                            List Callback
                        </div>
                        <div class="card-body">
                            <ul class="list-group list-group-flush">
                                <li class="list-group-item">An item</li>
                                <li class="list-group-item">A second item</li>
                                <li class="list-group-item">A third item</li>
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
<route lang="yaml">
meta:
    requiresAuth: true
</route>