<template>
  <div class="bg-light min-vh-100">
    <div class="bg-primary bg-opacity-10 py-3 border-bottom">
      <div class="container">
        <div class="d-flex justify-content-between align-items-center">
          <div>
            <h1 class="h4 fw-bold mb-2">Admin Dashboard</h1>
            <p class="text-muted mb-0">Overview of your parking management system</p>
          </div>
          <div class="d-flex gap-3">
            <button class="btn btn-outline-primary btn-sm" @click="refreshData">
              <i class="fas fa-sync-alt me-1"></i>
              Refresh
            </button>
          </div>
        </div>
      </div>
    </div>

    <div class="container py-4">
      <div v-if="error" class="alert alert-danger">{{ error }}</div>
      
      <div v-if="loading" class="text-center py-5">
        <div class="spinner-border text-primary mb-3"></div>
        <p class="text-muted">Loading dashboard...</p>
      </div>
      
      <div v-else>
        <!-- Statistics Cards -->
        <div class="row g-4 mb-5">
          <div class="col-lg-2 col-md-4 col-sm-6">
            <div class="card text-center stat-card">
              <div class="card-body">
                <div class="fs-1 mb-3"></div>
                <div class="h3 text-primary fw-bold">{{ statistics.total_lots || 0 }}</div>
                <div class="text-muted">Total Lots</div>
              </div>
            </div>
          </div>
          
          <div class="col-lg-2 col-md-4 col-sm-6">
            <div class="card text-center stat-card">
              <div class="card-body">
                <div class="fs-1 mb-3"></div>
                <div class="h3 text-success fw-bold">{{ statistics.total_spots || 0 }}</div>
                <div class="text-muted">Total Spots</div>
              </div>
            </div>
          </div>
          
          <div class="col-lg-2 col-md-4 col-sm-6">
            <div class="card text-center stat-card">
              <div class="card-body">
                <div class="fs-1 mb-3 text-success"></div>
                <div class="h3 text-success fw-bold">{{ statistics.available_spots || 0 }}</div>
                <div class="text-muted">Available</div>
              </div>
            </div>
          </div>
          
          <div class="col-lg-2 col-md-4 col-sm-6">
            <div class="card text-center stat-card">
              <div class="card-body">
                <div class="fs-1 mb-3 text-danger"></div>
                <div class="h3 text-danger fw-bold">{{ statistics.occupied_spots || 0 }}</div>
                <div class="text-muted">Occupied</div>
              </div>
            </div>
          </div>
          
          <div class="col-lg-2 col-md-4 col-sm-6">
            <div class="card text-center stat-card">
              <div class="card-body">
                <div class="fs-1 mb-3"></div>
                <div class="h3 text-info fw-bold">{{ statistics.total_users || 0 }}</div>
                <div class="text-muted">Total Users</div>
              </div>
            </div>
          </div>
          
          <div class="col-lg-2 col-md-4 col-sm-6">
            <div class="card text-center stat-card">
              <div class="card-body">
                <div class="fs-1 mb-3"></div>
                <div class="h3 text-warning fw-bold">₹{{ totalRevenue.toLocaleString() }}</div>
                <div class="text-muted">Total Revenue</div>
              </div>
            </div>
          </div>
        </div>

        <!-- Charts Section -->
        <div class="row g-4">
          <div class="col-lg-6">
            <div class="card border-0 shadow-sm">
              <div class="card-header bg-light">
                <h5 class="fw-bold mb-0">Content Distribution</h5>
              </div>
              <div class="card-body">
                <div class="d-flex align-items-center gap-3 mb-3">
                  <div class="d-flex align-items-center gap-2">
                    <div class="bg-primary rounded" style="width: 20px; height: 20px;"></div>
                    <small>Lots</small>
                  </div>
                  <div class="d-flex align-items-center gap-2">
                    <div class="bg-success rounded" style="width: 20px; height: 20px;"></div>
                    <small>Spots</small>
                  </div>
                  <div class="d-flex align-items-center gap-2">
                    <div class="bg-info rounded" style="width: 20px; height: 20px;"></div>
                    <small>Available</small>
                  </div>
                  <div class="d-flex align-items-center gap-2">
                    <div class="bg-warning rounded" style="width: 20px; height: 20px;"></div>
                    <small>Occupied</small>
                  </div>
                </div>
                <div class="progress" style="height: 30px;">
                  <div class="progress-bar bg-primary" :style="{ width: (statistics.total_lots / (statistics.total_lots + statistics.total_spots) * 100) + '%' }"></div>
                  <div class="progress-bar bg-success" :style="{ width: (statistics.total_spots / (statistics.total_lots + statistics.total_spots) * 100) + '%' }"></div>
                  <div class="progress-bar bg-info" :style="{ width: (statistics.available_spots / (statistics.total_lots + statistics.total_spots) * 100) + '%' }"></div>
                  <div class="progress-bar bg-warning" :style="{ width: (statistics.occupied_spots / (statistics.total_lots + statistics.total_spots) * 100) + '%' }"></div>
                </div>
              </div>
            </div>
          </div>
          
          <div class="col-lg-6">
            <div class="card border-0 shadow-sm">
              <div class="card-header bg-light">
                <h5 class="fw-bold mb-0">User Activity</h5>
              </div>
              <div class="card-body">
                <div class="d-flex align-items-center gap-3 mb-3">
                  <div class="d-flex align-items-center gap-2">
                    <div class="bg-purple rounded" style="width: 20px; height: 20px;"></div>
                    <small>Count</small>
                  </div>
                </div>
                <div class="d-flex align-items-end gap-2" style="height: 100px;">
                  <div class="bg-purple rounded-top flex-fill" style="height: 60%;"></div>
                  <div class="bg-purple rounded-top flex-fill" style="height: 80%;"></div>
                  <div class="bg-purple rounded-top flex-fill" style="height: 45%;"></div>
                  <div class="bg-purple rounded-top flex-fill" style="height: 70%;"></div>
                  <div class="bg-purple rounded-top flex-fill" style="height: 55%;"></div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const router = useRouter()
const loading = ref(false)
const error = ref('')
const statistics = ref({})

const totalRevenue = ref(0)

async function loadTotalRevenue() {
  const authConfig = createAuthConfig()
  if (!authConfig) return

  try {
    const res = await axios.get("http://localhost:5000/api/admin/total-revenue", authConfig)
    totalRevenue.value = res.data.total_revenue
  } catch (err) {
    console.error("Failed to load revenue:", err.response?.data || err)
  }
}

// load data on mount
onMounted(() => {
  loadTotalRevenue()
})


function createAuthConfig() {
  const token = localStorage.getItem('token')
  const user = localStorage.getItem('user')
  
  if (!token || !user) {
    router.push('/admin-login')
    return null
  }
  
  try {
    const userData = JSON.parse(user)
    if (userData.role !== 'admin') {
      router.push('/admin-login')
      return null
    }
  } catch (e) {
    router.push('/admin-login')
    return null
  }
  
  return {
    headers: { Authorization: `Bearer ${token}` }
  }
}

async function loadDashboard() {
  const authConfig = createAuthConfig()
  if (!authConfig) return

  loading.value = true
  try {
    const response = await axios.get('http://localhost:5000/admin/dashboard', authConfig)
    statistics.value = response.data.statistics || {}
  } catch (e) {
    if (e.response?.status === 401) {
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      router.push('/admin-login')
      return
    }
    error.value = e.response?.data?.message || 'Failed to load dashboard'
  } finally {
    loading.value = false
  }
}

function refreshData() {
  loadDashboard()
}

onMounted(() => {
  loadDashboard()
})
</script>

<style scoped>
/* Simple hover effects for cards */
.stat-card {
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15) !important;
}

/* Custom colors */
.bg-purple {
  background-color: #6f42c1 !important;
}
</style>