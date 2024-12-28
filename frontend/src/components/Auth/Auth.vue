<script setup>
import Navbar from './Navbar.vue';
import Aside from './Aside.vue';

defineProps({
  access_token: String
})
</script>


<template>
  <Navbar/>
  <Aside :access_token="access_token" />
</template>