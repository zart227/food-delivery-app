import { createApp } from "vue";
import router from './router'
import { createPinia } from 'pinia'
import "./assets/styles/style.scss";
import App from "./App.vue";

const pinia = createPinia()

createApp(App)
    .use(pinia)
    .use(router)
    .mount("#app");
