// src/main.js
import { createApp } from 'vue';
import App from './App.vue';
import router from './router/index';

const app = createApp(App);

app.config.globalProperties.$BACKEND_URL = 'http://127.0.0.1:5000';

const token = localStorage.getItem('authToken');
if (token) {
  app.config.globalProperties.$isAuthenticated = true;
} else {
  app.config.globalProperties.$isAuthenticated = false;
}

app.use(router).mount('#app');
