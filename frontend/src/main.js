import './assets/main.css'
import 'primeicons/primeicons.css'
import Toast from "vue-toastification";
import "vue-toastification/dist/index.css";
import router from './router';
import mitt from 'mitt'
import { VueMasonryPlugin } from "vue-masonry";
import { autoAnimatePlugin } from '@formkit/auto-animate/vue';
import { createPinia } from "pinia";



const emitter = mitt()


import { createApp } from 'vue'
import App from './App.vue'

const app = createApp(App)

app.config.globalProperties.emitter = emitter

app.use(createPinia()); 
app.use(autoAnimatePlugin)
app.use(VueMasonryPlugin)
app.use(router);
app.use(Toast);
app.mount('#app')