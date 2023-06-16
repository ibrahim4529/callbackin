<script setup lang="ts">
import { Icon } from '@iconify/vue';
const props = defineProps({
    icon: {
        type: String,
        default: ''
    },
    text: {
        type: String,
        default: ''
    },
    type: {
        type: String,
        default: 'primary'
    }
})
</script>

<template>
    <button :class="`btn btn-${props.type}`">
        {{ props.text }}
        <Icon v-if="props.icon" :icon="props.icon" class="icon" />
    </button>
</template>

<style scoped>
.icon {
    margin-left: 5px;
    justify-self: center
}
</style>