<template>
    <div>
        <canvas id="GPUFrame"></canvas>
        <div id="map"></div>
    </div>
</template>

<script setup>
import { onMounted } from 'vue';
import start from './gridmain'

onMounted(() => {
    console.log("app mounted")
    start()
})
</script>

