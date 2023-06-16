<script lang="ts" setup>
import { useHead } from '@vueuse/head';
useHead({
  title: 'Callbackin',
  meta: [
    {
      name: 'description',
      content: 'Simple App to handle callback to local'
    }
  ]
})
</script>
<template>
  <router-view />
</template>