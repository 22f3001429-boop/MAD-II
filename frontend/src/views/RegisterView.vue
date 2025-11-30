<template>
  <div class="min-vh-100 d-flex align-items-center justify-content-center bg-light py-5">
    <div class="card shadow-lg" style="max-width: 500px; width: 100%;">
      <div class="card-header text-center bg-primary text-white">
        <router-link to="/" class="text-white text-decoration-none mb-3 d-block">← Back to Home</router-link>
        <div class="mb-3">
          <div class="fs-1 mb-2"></div>
          <h1 class="h3 mb-1">Vehile Parking</h1>
          <p class="mb-0 opacity-75">Create your account</p>
        </div>
      </div>
      
      <div class="card-body p-4">
        <form @submit.prevent="register">
          <div v-if="error" class="alert alert-danger">
            {{ error }}
          </div>
          
          <div class="row g-3">
            <div class="col-md-6">
              <label class="form-label fw-semibold">Username</label>
              <input 
                v-model="username" 
                type="text" 
                class="form-control" 
                placeholder="Choose a username"
                required 
              />
            </div>
            <div class="col-md-6">
              <label class="form-label fw-semibold">Email Address</label>
              <input 
                v-model="email" 
                type="email" 
                class="form-control" 
                placeholder="your@email.com"
                required 
              />
            </div>
          </div>
          
          <div class="row g-3 mt-1">
            <div class="col-md-6">
              <label class="form-label fw-semibold">Phone Number</label>
              <input 
                v-model="phoneNumber" 
                type="tel" 
                class="form-control" 
                placeholder="Your phone number"
                required 
              />
            </div>
            <div class="col-md-6">
              <label class="form-label fw-semibold">Pincode</label>
              <input 
                v-model="pincode" 
                type="text" 
                class="form-control" 
                placeholder="Area pincode"
                required 
              />
            </div>
          </div>
          
          <div class="mb-3 mt-3">
            <label class="form-label fw-semibold">Full Address</label>
            <input 
              v-model="address" 
              type="text" 
              class="form-control" 
              placeholder="Enter your complete address"
              required 
            />
          </div>
          
          <div class="mb-3">
            <label class="form-label fw-semibold">Password</label>
            <input 
              v-model="password" 
              type="password" 
              class="form-control" 
              placeholder="Create a strong password"
              required 
            />
          </div>
          
          <button class="btn btn-primary w-100 py-2" :disabled="loading">
            <span v-if="loading">
              <span class="spinner-border spinner-border-sm me-2"></span>
              Creating Account...
            </span>
            <span v-else>Create Account</span>
          </button>
        </form>
        
        <div class="text-center mt-4">
          <p class="text-muted">Already have an account? 
            <router-link to="/login" class="text-decoration-none">Sign in here</router-link>
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
const email = ref('')
const phoneNumber = ref('')
const address = ref('')
const pincode = ref('')
const password = ref('')
const loading = ref(false)
const error = ref('')
const router = useRouter()

async function register() {
  loading.value = true
  error.value = ''
  try {
    const res = await axios.post('http://localhost:5000/auth/register', {
      username: username.value,
      email: email.value,
      phone_number: phoneNumber.value,
      address: address.value,
      pincode: pincode.value,
      password: password.value
    })
    
    localStorage.setItem('token', res.data.token)
    localStorage.setItem('user', JSON.stringify(res.data.user))
    
    // Check if user is admin and redirect accordingly
    if (res.data.user && res.data.user.role === 'admin') {
      router.push('/admin/dashboard')
    } else {
      router.push('/dashboard')
    }
  } catch (e) {
    error.value = e.response?.data?.message || 'Registration failed.'
  } finally {
    loading.value = false
  }
}
</script>