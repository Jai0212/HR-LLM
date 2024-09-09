import { createRouter, createWebHistory } from 'vue-router';
import InputOutput from '../components/InputOutput.vue';
import UserLogin from '../components/UserLogin.vue';
import UserSignUp from '../components/UserSignUp.vue';

const routes = [
  {
    path: '/',
    name: 'Login',
    component: UserLogin
  },
  {
    path: '/signup',
    name: 'Sign Up',
    component: UserSignUp
  },
  {
    path: '/home',
    name: 'Home',
    component: InputOutput,
    meta: { requiresAuth: true }
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});


router.beforeEach((to, from, next) => {
  const isAuthenticated = !!localStorage.getItem('authToken');

  if (to.matched.some(record => record.meta.requiresAuth) && !isAuthenticated) {
    next({ name: 'Login' });
  } else {
    next();
  }
});

export default router;
