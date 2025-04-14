<template>
  <div id="particles-js" style="width: 100%; height: 100vh;"></div>
</template>

<script setup>
import { onMounted } from 'vue'
import { tsParticles } from 'tsparticles'

onMounted(() => {
  tsParticles.load('particles-js', {
    particles: {
      number: {
        value: 80,
        density: {
          enable: true,
          value_area: 800
        }
      },
      shape: {
        type: 'circle'
      },
      opacity: {
        value: 0.5,
        random: true,
        anim: {
          enable: true,
          speed: 1,
          opacity_min: 0.1,
          sync: false
        }
      },
      size: {
        value: 3,
        random: true
      },
      links: {
        enable: true,
        distance: 150,
        color: '#ffffff',
        opacity: 0.4,
        width: 1
      }
    },
    interactivity: {
      detect_on: 'canvas',
      events: {
        onhover: {
          enable: true,
          mode: 'repulse'
        },
        onclick: {
          enable: true,
          mode: 'push'
        }
      }
    },
    retina_detect: true
  })
})
</script>

<style scoped>
#particles-js {
  position: absolute;
  top: 0;
  left: 0;
  z-index: -1;
}
</style>