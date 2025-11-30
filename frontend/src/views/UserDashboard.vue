<template>
  <div class="bg-light min-vh-100">
    <!-- Header Section -->
    <div class="bg-success bg-opacity-10 py-3 border-bottom">
      <div class="container">
        <div class="d-flex justify-content-between align-items-center">
          <div>
            <h1 class="h4 fw-bold mb-2">Welcome, {{ user?.username || 'User' }}!</h1>
            <p class="text-muted mb-0">Manage your parking reservations and find available spots</p>
          </div>
          <div class="d-flex gap-3 align-items-center">
            <div class="input-group" style="max-width: 300px;">
              <input 
                v-model="searchQuery" 
                type="text" 
                class="form-control form-control-sm" 
                placeholder="Search parking @location"
                @keyup.enter="performSearch"
              >
              <button class="btn btn-outline-primary btn-sm" type="button" @click="performSearch">
                <i class="fas fa-search"></i>
              </button>
            </div>
            <router-link to="/profile" class="btn btn-outline-primary btn-sm">View Profile</router-link>
            <button class="btn btn-outline-danger btn-sm" @click="logout">Logout</button>
          </div>
        </div>
      </div>
    </div>

    <div class="container py-4">
      <!-- Error Display -->
      <div v-if="error" class="alert alert-danger d-flex justify-content-between align-items-center">
        {{ error }}
        <button @click="retryLoad" class="btn btn-sm btn-outline-danger">Retry</button>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="text-center py-5">
        <div class="spinner-border text-primary mb-3" role="status"></div>
        <p class="text-muted">Loading dashboard...</p>
      </div>

      <!-- Main Dashboard Content -->
      <div v-else class="row g-4">
        <!-- Recent Parking History -->
        <div class="col-12">
          <div class="card shadow-sm dashboard-card">
            <div class="card-header bg-primary text-white">
              <h5 class="mb-0">Recent parking history</h5>
            </div>
            <div class="card-body">
              <div v-if="reservations.length === 0" class="text-center py-4 text-muted">
                <p>No parking history yet</p>
              </div>
              <div v-else class="table-responsive">
                <table class="table table-hover">
                  <thead class="table-light">
                    <tr>
                      <th>ID</th>
                      <th>Location</th>
                      <th>Vehicle_no</th>
                      <th>Timestamp</th>
                      <th>Action</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="reservation in recentReservations" :key="reservation.id">
                      <td>{{ reservation.id }}</td>
                      <td>{{ getLocationName(reservation.spot_id) }}</td>
                      <td>{{ user?.username || 'N/A' }}</td>
                      <td>{{ formatDateTime(reservation.parking_timestamp) }}</td>
                      <td>
                        <button 
                          v-if="!reservation.leaving_timestamp" 
                          class="btn btn-danger btn-sm"
                          @click="openReleaseModal(reservation)"
                        >
                          Release
                        </button>
                        <span v-else class="badge bg-success">Parked Out</span>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>



                 <!-- Parking Lots -->
         <div class="col-12">
           <div class="card shadow-sm dashboard-card">
             <div class="card-header bg-success text-white">
               <h5 class="mb-0">Parking Lots @ {{ searchQuery || 'All Locations' }}</h5>
             </div>
            <div class="card-body">
              <div v-if="displayedLots.length === 0" class="text-center py-4 text-muted">
                <p>No parking lots found</p>
              </div>
              <div v-else class="table-responsive">
                <table class="table table-hover">
                  <thead class="table-light">
                    <tr>
                      <th>ID</th>
                      <th>Address</th>
                      <th>Availability</th>
                      <th>Action</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="lot in displayedLots" :key="lot.id">
                      <td>{{ lot.id }}</td>
                      <td>{{ lot.address }}</td>
                      <td>{{ lot.available_spots }}</td>
                      <td>
                        <button 
                          class="btn btn-primary btn-sm"
                          :disabled="lot.available_spots === 0 || hasActiveBooking"
                          @click="openBookModal(lot)"
                        >
                          {{ lot.available_spots === 0 ? 'Full' : 'Book' }}
                        </button>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>

        <!-- Summary Chart -->
        <div class="col-lg-6">
          <div class="card shadow-sm">
            <div class="card-header bg-warning text-dark">
              <h5 class="mb-0">Summary on already used parking spots</h5>
            </div>
            <div class="card-body">
              <div class="d-flex align-items-end justify-content-center gap-3" style="height: 150px;">
                <div class="d-flex flex-column align-items-center">
                  <div class="bg-success rounded-top d-flex align-items-end justify-content-center text-white fw-bold" 
                       :style="{ height: getBarHeight(0) + 'px', width: '60px' }">
                    <small>{{ getMonthlyBookings(0) }}</small>
                  </div>
                  <small class="mt-2 text-muted">Last Month</small>
                </div>
                <div class="d-flex flex-column align-items-center">
                  <div class="bg-primary rounded-top d-flex align-items-end justify-content-center text-white fw-bold" 
                       :style="{ height: getBarHeight(1) + 'px', width: '60px' }">
                    <small>{{ getMonthlyBookings(1) }}</small>
                  </div>
                  <small class="mt-2 text-muted">This Month</small>
                </div>
                <div class="d-flex flex-column align-items-center">
                  <div class="bg-warning rounded-top d-flex align-items-end justify-content-center text-dark fw-bold" 
                       :style="{ height: getBarHeight(2) + 'px', width: '60px' }">
                    <small>{{ getMonthlyBookings(2) }}</small>
                  </div>
                  <small class="mt-2 text-muted">Next Month</small>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Quick Actions -->
        <div class="col-lg-6">
          <div class="card shadow-sm">
            <div class="card-header bg-secondary text-white">
              <h5 class="mb-0">Quick Actions</h5>
            </div>
            <div class="card-body">
              <div class="d-grid gap-3">
                <router-link to="/search" class="btn btn-outline-primary d-flex align-items-center gap-3 text-start">
                  <span class="fs-4">🔍</span>
                  <div>
                    <div class="fw-semibold">Find Parking</div>
                    <small class="text-muted">Search available spots</small>
                  </div>
                </router-link>
                
                <router-link to="/profile" class="btn btn-outline-info d-flex align-items-center gap-3 text-start">
                  <span class="fs-4">👤</span>
                  <div>
                    <div class="fw-semibold">My Profile</div>
                    <small class="text-muted">View account details</small>
                  </div>
                </router-link>
                
                <button class="btn btn-outline-success d-flex align-items-center gap-3 text-start" @click="refreshData">
                  <span class="fs-4">🔄</span>
                  <div>
                    <div class="fw-semibold">Refresh Data</div>
                    <small class="text-muted">Update dashboard</small>
                  </div>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Book Modal -->
    <div v-if="showBookModal" class="modal fade show d-block" style="background: rgba(0,0,0,0.5);" @click="closeModals">
      <div class="modal-dialog" @click.stop>
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Book the parking spot</h5>
            <button type="button" class="btn-close" @click="closeModals"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="confirmBooking">
              <div class="mb-3">
                <label class="form-label">Spot_ID:</label>
                <input type="text" :value="selectedLot?.id" readonly class="form-control">
              </div>
              <div class="mb-3">
                <label class="form-label">Lot_ID:</label>
                <input type="text" :value="selectedLot?.id" readonly class="form-control">
              </div>
              <div class="mb-3">
                <label class="form-label">User ID:</label>
                <input type="text" :value="user?.id" readonly class="form-control">
              </div>
              <div class="mb-3">
                <label class="form-label">Vehicle Number:</label>
                <input 
                  v-model="vehicleNumber" 
                  type="text" 
                  class="form-control" 
                  placeholder="Enter vehicle number"
                  required
                >
              </div>
              <p class="text-muted small fst-italic">etc, Fields...</p>
              <div class="d-flex gap-2 justify-content-end">
                <button type="submit" class="btn btn-primary" :disabled="bookingLoading">
                  {{ bookingLoading ? 'Booking...' : 'Reserve' }}
                </button>
                <button type="button" class="btn btn-secondary" @click="closeModals">
                  Cancel
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>

    <!-- Release Modal -->
    <div v-if="showReleaseModal" class="modal fade show d-block" style="background: rgba(0,0,0,0.5);" @click="closeModals">
      <div class="modal-dialog" @click.stop>
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Release the parking spot</h5>
            <button type="button" class="btn-close" @click="closeModals"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="confirmRelease">
              <div class="mb-3">
                <label class="form-label">Spot_ID:</label>
                <input type="text" :value="selectedReservation?.spot_id" readonly class="form-control">
              </div>
              <div class="mb-3">
                <label class="form-label">Vehicle Number:</label>
                <input type="text" :value="user?.username" readonly class="form-control">
              </div>
              <div class="mb-3">
                <label class="form-label">Parking Time:</label>
                <input type="text" :value="formatDateTime(selectedReservation?.parking_timestamp)" readonly class="form-control">
              </div>
              <div class="mb-3">
                <label class="form-label">Releasing Time:</label>
                <input type="text" :value="new Date().toLocaleString()" readonly class="form-control">
              </div>
              <div class="mb-3">
                <label class="form-label">Total cost:</label>
                <input type="text" :value="'₹' + (selectedReservation?.parking_cost || '0')" readonly class="form-control">
              </div>
              <p class="text-muted small fst-italic">pre-filled data</p>
              <div class="d-flex gap-2 justify-content-end">
                <button type="submit" class="btn btn-primary" :disabled="releaseLoading">
                  {{ releaseLoading ? 'Releasing...' : 'Release' }}
                </button>
                <button type="button" class="btn btn-secondary" @click="closeModals">
                  Cancel
                </button>
              </div>
            </form>
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

// Reactive data
const loading = ref(false)
const bookingLoading = ref(false)
const releaseLoading = ref(false)
const error = ref('')
const lots = ref([])
const reservations = ref([])
const user = ref(null)
const searchQuery = ref('')

// Modal states
const showBookModal = ref(false)
const showReleaseModal = ref(false)
const selectedLot = ref(null)
const selectedReservation = ref(null)
const vehicleNumber = ref('')

// Auth helper
function createAuthConfig() {
  const token = localStorage.getItem('token')
  if (!token) {
    router.push('/login')
    return null
  }
  return {
    headers: { Authorization: `Bearer ${token}` }
  }
}

// Load dashboard data
async function loadDashboard() {
  const authConfig = createAuthConfig()
  if (!authConfig) return

  loading.value = true
  error.value = ''
  
  try {
    const response = await axios.get('http://localhost:5000/user/dashboard', authConfig)
    lots.value = response.data.available_parking_lots || []
    reservations.value = response.data.my_reservations || []
    user.value = response.data.user
  } catch (e) {
    if (e.response?.status === 401) {
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      router.push('/login')
      return
    }
    error.value = e.response?.data?.message || 'Failed to load dashboard'
    console.error('Dashboard load error:', e)
  } finally {
    loading.value = false
  }
}

// Computed properties
const recentReservations = computed(() => {
  return reservations.value.slice(0, 3)
})

const displayedLots = computed(() => {
  if (!searchQuery.value.trim()) {
    return lots.value.slice(0, 3)
  }
  return lots.value.filter(lot => 
    lot.address?.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
    lot.pin_code?.includes(searchQuery.value)
  ).slice(0, 3)
})

const hasActiveBooking = computed(() => {
  return reservations.value.some(r => !r.leaving_timestamp)
})

// Helper functions
function formatDateTime(dateString) {
  if (!dateString) return 'N/A'
  return new Date(dateString).toLocaleString('en-US', {
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

function getLocationName(spotId) {
  return `Spot ${spotId}`
}

function getMonthlyBookings(monthOffset) {
  const targetDate = new Date()
  targetDate.setMonth(targetDate.getMonth() - monthOffset)
  
  return reservations.value.filter(res => {
    if (!res.parking_timestamp) return false
    const resDate = new Date(res.parking_timestamp)
    return resDate.getMonth() === targetDate.getMonth() && 
           resDate.getFullYear() === targetDate.getFullYear()
  }).length
}

function getBarHeight(monthOffset) {
  const count = getMonthlyBookings(monthOffset)
  const maxCount = Math.max(1, ...Array.from({length: 3}, (_, i) => getMonthlyBookings(i)))
  return Math.max(20, (count / maxCount) * 80)
}

function performSearch() {
  // Search is handled by computed property
}
// Modal functions
function openBookModal(lot) {
  selectedLot.value = lot
  showBookModal.value = true
}

function openReleaseModal(reservation) {
  selectedReservation.value = reservation
  showReleaseModal.value = true
}

function closeModals() {
  showBookModal.value = false
  showReleaseModal.value = false
  selectedLot.value = null
  selectedReservation.value = null
  vehicleNumber.value = ''
}

// Booking functions
async function confirmBooking() {
  if (!selectedLot.value) return
  
  const authConfig = createAuthConfig()
  if (!authConfig) return
  
  bookingLoading.value = true
  try {
    await axios.post('http://localhost:5000/api/reserve', {
      lot_id: selectedLot.value.id
    }, authConfig)
    
    await loadDashboard()
    closeModals()
    error.value = ''
  } catch (e) {
    if (e.response?.status === 401) {
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      router.push('/login')
      return
    }
    error.value = e.response?.data?.message || 'Failed to book spot'
  } finally {
    bookingLoading.value = false
  }
}

async function confirmRelease() {
  if (!selectedReservation.value) return
  
  const authConfig = createAuthConfig()
  if (!authConfig) return
  
  releaseLoading.value = true
  try {
    await axios.post('http://localhost:5000/api/release', {
      reservation_id: selectedReservation.value.id
    }, authConfig)
    
    await loadDashboard()
    closeModals()
    error.value = ''
  } catch (e) {
    if (e.response?.status === 401) {
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      router.push('/login')
      return
    }
    error.value = e.response?.data?.message || 'Failed to release spot'
  } finally {
    releaseLoading.value = false
  }
}

function retryLoad() {
  loadDashboard()
}

function logout() {
  localStorage.removeItem('token')
  localStorage.removeItem('user')
  router.push('/')
}

function refreshData() {
  loadDashboard()
}

// Initialize
onMounted(() => {
  loadDashboard()
})
</script>

<style scoped>
.dashboard-card {
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.dashboard-card:hover {
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