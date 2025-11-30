<template>
  <div class="bg-light min-vh-100">
    <div class="bg-primary bg-opacity-10 py-3 border-bottom">
      <div class="container">
        <h1 class="h4 fw-bold mb-2">Admin Summary</h1>
        <p class="text-muted mb-0">Comprehensive analytics and insights for your parking management system</p>
      </div>
    </div>

    <div class="container py-4">
      <div v-if="error" class="alert alert-danger">{{ error }}</div>
      
      <div v-if="loading" class="text-center py-5">
        <div class="spinner-border text-primary mb-3"></div>
        <p class="text-muted">Loading summary...</p>
      </div>
      
      <div v-else>
        <div class="mb-5">
          <div class="mb-4">
            <h2 class="h4 text-primary">Key Metrics</h2>
          </div>
          <div class="row g-4">
            <div class="col-lg-3 col-md-6">
              <div class="card text-center metric-card">
                <div class="card-body">
                  <div class="fs-1 mb-3"></div>
                  <h3 class="text-primary fw-bold">{{ statistics.total_lots || 0 }}</h3>
                  <p class="text-muted small mb-2">Total Parking Lots</p>
                </div>
              </div>
            </div>
            
            <div class="col-lg-3 col-md-6">
              <div class="card text-center metric-card">
                <div class="card-body">
                  <div class="fs-1 mb-3"></div>
                  <h3 class="text-primary fw-bold">{{ statistics.total_spots || 0 }}</h3>
                  <p class="text-muted small mb-2">Total Parking Spots</p>
                </div>
              </div>
            </div>
            
            <div class="col-lg-3 col-md-6">
              <div class="card text-center metric-card">
                <div class="card-body">
                  <div class="fs-1 mb-3"></div>
                  <h3 class="text-primary fw-bold">{{ statistics.total_users || 0 }}</h3>
                  <p class="text-muted small mb-2">Active Users</p>
                </div>
              </div>
            </div>
            
            <div class="col-lg-3 col-md-6">
              <div class="card text-center metric-card">
                <div class="card-body">
                  <div class="fs-1 mb-3"></div>
                  <h3 class="text-primary fw-bold">₹{{ totalRevenue.toLocaleString() }}</h3>
                  <p class="text-muted small mb-2">Total Revenue</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="mb-5">
          <div class="mb-4">
            <h2 class="h4 text-primary">Analytics Dashboard</h2>
          </div>
          
          <div class="row g-4 mb-4">

            <div class="col-lg-6">
              <div class="card h-100">
                <div class="card-header">
                  <h5 class="card-title mb-1">Parking Utilization</h5>
                  <p class="text-muted small mb-0">Real-time occupancy overview</p>
                </div>
                <div class="card-body text-center">
                  <div class="position-relative d-inline-block">
                    <div class="position-absolute top-50 start-50 translate-middle text-center">
                      <div class="h3 text-primary fw-bold">{{ utilizationPercentage }}%</div>
                      <div class="small text-muted">Occupied</div>
                    </div>
                    <svg width="120" height="120" viewBox="0 0 100 100">
                      <circle
                        cx="50"
                        cy="50"
                        r="40"
                        fill="none"
                        stroke="#e9ecef"
                        stroke-width="8"
                      />
                      <circle
                        cx="50"
                        cy="50"
                        r="40"
                        fill="none"
                        stroke="#0d6efd"
                        stroke-width="8"
                        stroke-dasharray="251.2"
                        :stroke-dashoffset="utilizationOffset"
                        stroke-linecap="round"
                        transform="rotate(-90 50 50)"
                      />
                    </svg>
                  </div>
                </div>
              </div>
            </div>

            <div class="col-lg-6">
              <div class="card h-100">
                <div class="card-header">
                  <h5 class="card-title mb-1">Recent Users</h5>
                  <p class="text-muted small mb-0">Latest registered users</p>
                </div>
                <div class="card-body">
                  <div v-if="recentUsers.length === 0" class="text-center text-muted py-4">
                    No recent users
                  </div>
                  <div v-else>
                    <div 
                      v-for="user in recentUsers.slice(0, 5)" 
                      :key="user.id"
                      class="d-flex align-items-center gap-3 mb-3"
                    >
                      <div class="bg-primary bg-opacity-10 rounded-circle p-2">
                        <span class="text-primary"></span>
                      </div>
                      <div class="flex-grow-1">
                        <div class="fw-medium">{{ user.username }}</div>
                        <small class="text-muted">{{ user.email }}</small>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>



          <div class="row">
            <div class="col-12">
              <div class="card">
                <div class="card-header">
                  <h5 class="card-title mb-1">System Overview</h5>
                  <p class="text-muted small mb-0">Current system status</p>
                </div>
                <div class="card-body">
                  <div class="row g-4">
                    <div class="col-md-3 col-6">
                      <div class="text-center">
                        <div class="h3 text-success mb-1">{{ statistics.available_spots || 0 }}</div>
                        <small class="text-muted">Available Spots</small>
                      </div>
                    </div>
                    <div class="col-md-3 col-6">
                      <div class="text-center">
                        <div class="h3 text-danger mb-1">{{ statistics.occupied_spots || 0 }}</div>
                        <small class="text-muted">Occupied Spots</small>
                      </div>
                    </div>
                    <div class="col-md-3 col-6">
                      <div class="text-center">
                        <div class="h3 text-info mb-1">{{ statistics.total_lots || 0 }}</div>
                        <small class="text-muted">Total Lots</small>
                      </div>
                    </div>
                    <div class="col-md-3 col-6">
                      <div class="text-center">
                        <div class="h3 text-warning mb-1">{{ statistics.total_reservations || 0 }}</div>
                        <small class="text-muted">Total Reservations</small>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="mb-5">
          <div class="mb-4 d-flex justify-content-between align-items-center">
            <h2 class="h4 text-primary">Top Performing Lots</h2>
            <button 
              class="btn btn-outline-success" 
              @click="exportCSV"
              :disabled="exportLoading"
            >
              <span v-if="exportLoading" class="spinner-border spinner-border-sm me-2"></span>
              Export CSV Report
            </button>
          </div>
          <div class="row g-4">
            <div 
              v-for="lot in topPerformingLots" 
              :key="lot.id"
              class="col-lg-4 col-md-6"
            >
              <div class="card metric-card">
                <div class="card-body">
                  <div class="d-flex justify-content-between align-items-start mb-3">
                    <h6 class="card-title mb-0">{{ lot.prime_location_name }}</h6>
                    <span class="badge bg-success-subtle text-success">{{ lot.utilization }}%</span>
                  </div>
                  <div class="mb-3">
                    <div class="progress" style="height: 8px;">
                      <div 
                        class="progress-bar bg-success" 
                        :style="{ width: lot.utilization + '%' }"
                      ></div>
                    </div>
                  </div>
                  <div class="d-flex justify-content-between">
                    <span class="text-muted small">Revenue</span>
                    <span class="fw-bold">₹{{ lot.revenue.toLocaleString() }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          <div class="row g-4 mt-4">
            <div class="col-lg-6">
              <div class="card h-100">
                <div class="card-header">
                  <h5 class="card-title mb-1">Parking Utilization Chart</h5>
                  <p class="text-muted small mb-0">Current parking lot utilization</p>
                </div>
                <div class="card-body">
                  <canvas ref="utilizationChart" width="400" height="200"></canvas>
                </div>
              </div>
            </div>
            
            <div class="col-lg-6">
              <div class="card h-100">
                <div class="card-header">
                  <h5 class="card-title mb-1">Revenue by Lot</h5>
                  <p class="text-muted small mb-0">Revenue distribution across parking lots</p>
                </div>
                <div class="card-body">
                  <canvas ref="revenueChart" width="400" height="200"></canvas>
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
const recentUsers = ref([])
const parkingLots = ref([])
const exportLoading = ref(false)
const utilizationChart = ref(null)
const revenueChart = ref(null)
let utilizationChartInstance = null
let revenueChartInstance = null

const totalRevenue = computed(() => {
  return parkingLots.value.reduce((sum, lot) => {
    return sum + (lot.occupied_spots * lot.price_per_hour * 2)
  }, 0)
})

const utilizationPercentage = computed(() => {
  const total = (statistics.value.total_spots || 0)
  const occupied = (statistics.value.occupied_spots || 0)
  return total > 0 ? Math.round((occupied / total) * 100) : 0
})

const utilizationCircumference = computed(() => {
  return 2 * Math.PI * 40
})

const utilizationOffset = computed(() => {
  const percentage = utilizationPercentage.value / 100
  return utilizationCircumference.value * (1 - percentage)
})

const topPerformingLots = computed(() => {
  return parkingLots.value
    .filter(lot => lot.number_of_spots > 0)
    .map(lot => ({
      ...lot,
      utilization: Math.round((lot.occupied_spots || 0) / lot.number_of_spots * 100),
      revenue: (lot.occupied_spots || 0) * lot.price_per_hour * 2
    }))
    .sort((a, b) => b.utilization - a.utilization)
    .slice(0, 6)
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

async function loadSummary() {
  const authConfig = createAuthConfig()
  if (!authConfig) return

  loading.value = true
  try {
    const response = await axios.get('http://localhost:5000/admin/dashboard', authConfig)
    statistics.value = response.data.statistics || {}
    recentUsers.value = response.data.recent_users || []
    parkingLots.value = response.data.parking_lots || []
    
    // Create charts after data is loaded
    setTimeout(createCharts, 100)
  } catch (e) {
    if (e.response?.status === 401) {
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      router.push('/admin-login')
      return
    }
    error.value = e.response?.data?.message || 'Failed to load summary'
  } finally {
    loading.value = false
  }
}

async function exportCSV() {
  const authConfig = createAuthConfig()
  if (!authConfig) return

  exportLoading.value = true

  try {
    const response = await axios.get(
      'http://localhost:5000/api/admin/export-csv',
      {
        ...authConfig,
        responseType: 'blob' // IMPORTANT for file download
      }
    )

    // Create download link
    const blob = new Blob([response.data], { type: 'text/csv' })
    const url = window.URL.createObjectURL(blob)
    
    const link = document.createElement('a')
    link.href = url
    link.download = 'parking_report.csv'
    link.click()

    window.URL.revokeObjectURL(url)

  } catch (e) {
    alert('Failed to download CSV: ' + (e.response?.data?.message || 'Unknown error'))
  } finally {
    exportLoading.value = false
  }
}


function createCharts() {
  if (utilizationChart.value && parkingLots.value.length > 0) {
    const ctx1 = utilizationChart.value.getContext('2d')
    if (utilizationChartInstance) {
      utilizationChartInstance.destroy()
    }
    
    utilizationChartInstance = new Chart(ctx1, {
      type: 'doughnut',
      data: {
        labels: ['Available', 'Occupied'],
        datasets: [{
          data: [statistics.value.available_spots || 0, statistics.value.occupied_spots || 0],
          backgroundColor: ['#28a745', '#dc3545'],
          borderWidth: 2
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: 'bottom'
          }
        }
      }
    })
  }
  
  if (revenueChart.value && parkingLots.value.length > 0) {
    const ctx2 = revenueChart.value.getContext('2d')
    if (revenueChartInstance) {
      revenueChartInstance.destroy()
    }
    
    const lotNames = parkingLots.value.map(lot => lot.prime_location_name)
    const revenues = parkingLots.value.map(lot => (lot.occupied_spots || 0) * lot.price_per_hour * 2)
    
    revenueChartInstance = new Chart(ctx2, {
      type: 'bar',
      data: {
        labels: lotNames,
        datasets: [{
          label: 'Revenue (₹)',
          data: revenues,
          backgroundColor: '#007bff',
          borderColor: '#0056b3',
          borderWidth: 1
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          y: {
            beginAtZero: true
          }
        }
      }
    })
  }
}

onMounted(async () => {
  await loadSummary()
  setTimeout(createCharts, 100) // Small delay to ensure DOM is ready
})
</script>

<style scoped>
/* Simple hover effects for cards */
.metric-card {
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.metric-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15) !important;
}

.btn {
  transition: transform 0.2s ease;
}

.btn:hover {
  transform: translateY(-1px);
}
</style>