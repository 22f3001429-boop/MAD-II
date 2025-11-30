<template>
  <div class="min-vh-100 d-flex align-items-center justify-content-center bg-light">
    <div class="card shadow-lg" style="max-width: 400px; width: 100%;">
      <div class="card-header text-center bg-danger text-white">
        <router-link to="/" class="text-white text-decoration-none mb-3 d-block">← Back to Home</router-link>
        <div class="mb-3">
          <div class="fs-1 mb-2">🔐</div>
          <h1 class="h3 mb-1">Admin Portal</h1>
          <p class="mb-0 opacity-75">Administrator access</p>
        </div>
      </div>
      
      <div class="card-body p-4">
        <form @submit.prevent="login">
          <div v-if="error" class="alert alert-danger">
            {{ error }}
          </div>
          
          <div class="mb-3">
            <label class="form-label fw-semibold">Admin Username</label>
            <input 
              v-model="username" 
              type="text" 
              class="form-control" 
              placeholder="Enter admin username"
              required 
            />
          </div>
          
          <div class="mb-3">
            <label class="form-label fw-semibold">Admin Password</label>
            <input 
              v-model="password" 
              type="password" 
              class="form-control" 
              placeholder="Enter admin password"
              required 
            />
          </div>
          
          <button class="btn btn-danger w-100 py-2" :disabled="loading">
            <span v-if="loading">
              <span class="spinner-border spinner-border-sm me-2"></span>
              Signing in...
            </span>
            <span v-else>Admin Sign In</span>
          </button>
        </form>
        
        <div class="text-center mt-4">
          <p class="text-muted">
            <router-link to="/login" class="text-decoration-none">User Login</router-link>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const username = ref('')
const password = ref('')
const loading = ref(false)
const error = ref('')
const router = useRouter()

async function login() {
  loading.value = true
  error.value = ''
  try {
    const res = await axios.post('http://localhost:5000/auth/admin-login', {
      username: username.value,
      password: password.value
    })
    
    localStorage.setItem('token', res.data.token)
    localStorage.setItem('user', JSON.stringify(res.data.user))
    
    router.push('/admin/dashboard')
  } catch (e) {
    error.value = e.response?.data?.message || 'Admin login failed.'
  } finally {
    loading.value = false
  }
}
</script>