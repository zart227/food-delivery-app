import { createApp } from "vue";
import router from './router'
import { createPinia } from 'pinia'
import Toast from 'vue-toastification'
import 'vue-toastification/dist/index.css'
import "./assets/styles/style.scss";
import App from "./App.vue";
import './api/interceptor';
// import './index.css'
// import '../node_modules/flowbite-vue/dist/index.css'


const pinia = createPinia()

createApp(App)
    .use(pinia)
    .use(router)
    .use(Toast)
    .mount("#app");
