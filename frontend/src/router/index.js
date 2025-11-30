import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'home',
    component: () => import('../views/HomeView.vue'),
  },
  {
    path: '/admin/dashboard',
    name: 'admin-dashboard',
    component: () => import('../views/AdminDashboard.vue'),
  },
  {
    path: '/dashboard',
    name: 'user-dashboard',
    component: () => import('../views/UserDashboard.vue'),
  },
  {
    path: '/lots',
    name: 'lots',
    component: () => import('../views/LotsView.vue'),
  },
  {
    path: '/spots',
    name: 'spots',
    component: () => import('../views/SpotsView.vue'),
  },
  {
    path: '/users',
    name: 'users',
    component: () => import('../views/UsersView.vue'),
  },
  {
    path: '/login',
    name: 'login',
    component: () => import('../views/LoginView.vue'),
  },
  {
    path: '/register',
    name: 'register',
    component: () => import('../views/RegisterView.vue'),
  },
  {
    path: '/admin-login',
    name: 'admin-login',
    component: () => import('../views/AdminLoginView.vue'),
  },
  {
    path: '/search',
    name: 'search',
    component: () => import('../views/SearchView.vue'),
  },
  {
    path: '/profile',
    name: 'profile',
    component: () => import('../views/ProfileView.vue'),
  },
  {
    path: '/admin/summary',
    name: 'admin-summary',
    component: () => import('../views/AdminSummary.vue'),
  },
  {
    path: '/summary',
    name: 'user-summary',
    component: () => import('../views/UserSummary.vue'),
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router 