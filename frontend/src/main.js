import './assets/main.css'
import 'primeicons/primeicons.css'
import Toast from "vue-toastification";
import "vue-toastification/dist/index.css";



import { createApp } from 'vue'
import App from './App.vue'

const app = createApp(App)

const options = {
  // You can set your default options here
};

app.use(Toast, options);
app.mount('#app')