<template>
  <div>
    <nav class="navbar navbar-expand-lg navbar-light bg-white shadow-sm fixed-top" v-if="showNavbar">
      <div class="container-fluid">
        <router-link class="navbar-brand d-flex align-items-center text-decoration-none" to="/">
          <span class="bg-primary text-white rounded d-flex align-items-center justify-content-center me-2 fw-bold fs-4" 
                style="width: 2rem; height: 2rem;">P</span>
          {{ isAdmin ? 'Parking Admin' : 'Vehile Parking' }}
        </router-link>
        
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
          <span class="navbar-toggler-icon"></span>
        </button>
        
        <div class="collapse navbar-collapse" id="navbarNav">
          <!-- Search Bar -->
          <div class="mx-auto" style="max-width: 400px;" v-if="showNavbar">
            <div class="input-group">
              <input 
                v-model="searchQuery" 
                type="text" 
                class="form-control" 
                placeholder="Search parking @location/pin code"
                @keyup.enter="performSearch"
              >
              <button class="btn btn-primary" @click="performSearch">
                <i class="fas fa-search"></i>
              </button>
            </div>
          </div>

          <!-- Navigation Links -->
          <ul class="navbar-nav ms-auto">
            <!-- Admin Navigation -->
            <template v-if="isAdmin">
              <li class="nav-item">
                <router-link class="nav-link" to="/admin/dashboard">Dashboard</router-link>
              </li>
              <li class="nav-item">
                <router-link class="nav-link" to="/admin/summary">Summary</router-link>
              </li>
              <li class="nav-item">
                <router-link class="nav-link" to="/lots">Lots</router-link>
              </li>
              <li class="nav-item">
                <router-link class="nav-link" to="/spots">Spots</router-link>
              </li>
              <li class="nav-item">
                <router-link class="nav-link" to="/users">Users</router-link>
              </li>
            </template>
            <!-- User Navigation -->
            <template v-else>
              <li class="nav-item">
                <router-link class="nav-link" to="/dashboard">Dashboard</router-link>
              </li>
              <li class="nav-item">
                <router-link class="nav-link" to="/summary">Summary</router-link>
              </li>
              <li class="nav-item">
                <router-link class="nav-link" to="/profile">Profile</router-link>
              </li>
            </template>
            <li class="nav-item" v-if="showLogout">
              <button class="btn btn-outline-danger ms-2" @click="logout">
                Logout
              </button>
            </li>
          </ul>
        </div>
      </div>
    </nav>
    <div :style="showNavbar ? 'padding-top: 80px;' : ''">
      <router-view />
    </div>
    <NotificationToast ref="notifications" />
  </div>
</template>

<script setup>
import { useRouter, useRoute } from 'vue-router'
import { computed, ref, onMounted, watch, provide } from 'vue'
import axios from 'axios'
import NotificationToast from './components/NotificationToast.vue'

const router = useRouter()
const route = useRoute()
const userRole = ref(null)
const searchQuery = ref('')

function logout() {
  localStorage.removeItem('token')
  localStorage.removeItem('user')
  userRole.value = null
  router.push('/login')
}

function performSearch() {
  if (searchQuery.value.trim()) {
    router.push({
      path: '/search',
      query: { q: searchQuery.value.trim() }
    })
  }
}

function getUserRole() {
  const user = localStorage.getItem('user')
  if (user) {
    try {
      const userData = JSON.parse(user)
      userRole.value = userData.role
    } catch (e) {
      userRole.value = null
    }
  } else {
    userRole.value = null
  }
}

onMounted(() => {
  getUserRole()
})

watch(() => route.path, () => {
  getUserRole()
})

const showLogout = computed(() => !['/login', '/register', '/'].includes(route.path))
const showNavbar = computed(() => !['/login', '/register', '/'].includes(route.path))
const isAdmin = computed(() => userRole.value === 'admin')
</script> 

<style scoped>
.navbar-brand {
  font-size: 1.5rem;
  font-weight: 700;
  color: #0d6efd;
}

.navbar-brand:hover {
  color: #0b5ed7;
}

.nav-link.router-link-active {
  color: #0d6efd !important;
  font-weight: 600;
}

.nav-link:hover {
  color: #0d6efd;
}
</style>