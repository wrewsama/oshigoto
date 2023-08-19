<script setup lang="ts">
const props = defineProps({
    data: {
        type:Object,
        required: true
    }
})
</script>

<template>
    <li class="list-group-item d-flex">
        <div class="me-auto fw-bold">
            {{ data.phrase }}
        </div>
        {{ data.count }} occurences
    </li>
</template>