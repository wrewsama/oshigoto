<script setup lang="ts">
const props = defineProps({
    data: {
        type: Object,
        required: true
    }
})
</script>
<template>
    <a :href="data.link" class="list-group-item">
        <h6>{{ data.company }}</h6>
        {{ data.title }}
    </a>
</template>