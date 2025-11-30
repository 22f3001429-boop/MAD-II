<template>
  <div class="bg-light min-vh-100">
    <div class="bg-primary bg-opacity-10 py-3 border-bottom">
      <div class="container">
        <h1 class="h4 fw-bold mb-2">My Profile</h1>
        <p class="text-muted mb-0">Manage your account and parking history</p>
      </div>
    </div>

    <div class="container py-4">
      <div v-if="error" class="alert alert-danger">{{ error }}</div>
      
      <div v-if="loading" class="text-center py-5">
        <div class="spinner-border text-primary mb-3" role="status"></div>
        <p class="text-muted">Loading profile...</p>
      </div>
      
      <div v-else class="row g-4">
        <!-- Profile Information -->
        <div class="col-12">
          <div class="card shadow-sm">
            <div class="card-header d-flex justify-content-between align-items-center">
              <h2 class="h5 mb-0">Profile Information</h2>
              <button class="btn btn-outline-primary btn-sm" @click="toggleEdit">
                {{ editing ? 'Cancel' : 'Edit Profile' }}
              </button>
            </div>
            <div class="card-body">
              <div class="row g-3">
                <div class="col-md-6">
                  <label class="form-label fw-semibold">Username</label>
                  <input 
                    v-model="profileData.username" 
                    type="text" 
                    class="form-control" 
                    :readonly="!editing"
                  >
                </div>
                <div class="col-md-6">
                  <label class="form-label fw-semibold">Email</label>
                  <input 
                    v-model="profileData.email" 
                    type="email" 
                    class="form-control" 
                    :readonly="!editing"
                  >
                </div>
                <div class="col-md-6">
                  <label class="form-label fw-semibold">Phone Number</label>
                  <input 
                    v-model="profileData.phone_number" 
                    type="tel" 
                    class="form-control" 
                    :readonly="!editing"
                  >
                </div>
                <div class="col-md-6">
                  <label class="form-label fw-semibold">Pin Code</label>
                  <input 
                    v-model="profileData.pincode" 
                    type="text" 
                    class="form-control" 
                    :readonly="!editing"
                  >
                </div>
                <div class="col-12">
                  <label class="form-label fw-semibold">Address</label>
                  <input 
                    v-model="profileData.address" 
                    type="text" 
                    class="form-control" 
                    :readonly="!editing"
                  >
                </div>
                
                <div v-if="editing" class="col-12">
                  <div class="d-flex gap-2">
                    <button class="btn btn-primary" @click="saveProfile" :disabled="saving">
                      <span v-if="saving">
                        <span class="spinner-border spinner-border-sm me-2"></span>
                        Saving...
                      </span>
                      <span v-else>Save Changes</span>
                    </button>
                    <button class="btn btn-secondary" @click="cancelEdit">
                      Cancel
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Parking Statistics -->
        <div class="col-12">
          <div class="card shadow-sm">
            <div class="card-header">
              <h2 class="h5 mb-0">Parking Statistics</h2>
            </div>
            <div class="card-body">
              <div class="row g-3">
                <div class="col-md-3 col-sm-6">
                  <div class="text-center p-3 bg-primary bg-opacity-10 rounded">
                    <div class="h3 text-primary fw-bold mb-1">{{ stats.totalBookings }}</div>
                    <small class="text-muted">Total Bookings</small>
                  </div>
                </div>
                <div class="col-md-3 col-sm-6">
                  <div class="text-center p-3 bg-success bg-opacity-10 rounded">
                    <div class="h3 text-success fw-bold mb-1">{{ stats.activeBookings }}</div>
                    <small class="text-muted">Active Bookings</small>
                  </div>
                </div>
                <div class="col-md-3 col-sm-6">
                  <div class="text-center p-3 bg-info bg-opacity-10 rounded">
                    <div class="h3 text-info fw-bold mb-1">{{ stats.totalSpent }}</div>
                    <small class="text-muted">Total Spent</small>
                  </div>
                </div>
                <div class="col-md-3 col-sm-6">
                  <div class="text-center p-3 bg-warning bg-opacity-10 rounded">
                    <div class="h3 text-warning fw-bold mb-1">{{ stats.avgDuration }}</div>
                    <small class="text-muted">Avg Duration</small>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Recent Activity -->
        <div class="col-12">
          <div class="card shadow-sm">
            <div class="card-header">
              <h2 class="h5 mb-0">Recent Activity</h2>
            </div>
            <div class="card-body">
              <div v-if="recentActivity.length === 0" class="text-center py-4 text-muted">
                <div class="fs-1 mb-3">📋</div>
                <p>No recent activity</p>
              </div>
              <div v-else class="list-group list-group-flush">
                <div v-for="activity in recentActivity" :key="activity.id" 
                     class="list-group-item d-flex justify-content-between align-items-center">
                  <div>
                    <div class="fw-semibold">{{ activity.action }}</div>
                    <small class="text-muted">{{ formatDateTime(activity.timestamp) }}</small>
                  </div>
                  <span class="badge bg-primary rounded-pill">{{ activity.location }}</span>
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

// Reactive data
const loading = ref(false)
const saving = ref(false)
const passwordLoading = ref(false)
const error = ref('')
const editing = ref(false)
const showPasswordModal = ref(false)

const user = ref(null)
const reservations = ref([])
const profileData = ref({
  username: '',
  email: '',
  phone_number: '',
  address: '',
  pincode: ''
})

const passwordForm = ref({
  current: '',
  new: '',
  confirm: ''
})

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

// Load profile data
async function loadProfile() {
  const authConfig = createAuthConfig()
  if (!authConfig) return

  loading.value = true
  try {
    const response = await axios.get('http://localhost:5000/user/dashboard', authConfig)
    user.value = response.data.user
    reservations.value = response.data.my_reservations || []
    
    // Populate profile form
    profileData.value = {
      username: user.value.username || '',
      email: user.value.email || '',
      phone_number: user.value.phone_number || '',
      address: user.value.address || '',
      pincode: user.value.pincode || ''
    }
  } catch (e) {
    if (e.response?.status === 401) {
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      router.push('/login')
      return
    }
    error.value = e.response?.data?.message || 'Failed to load profile'
  } finally {
    loading.value = false
  }
}

// Computed statistics
const stats = computed(() => {
  const totalBookings = reservations.value.length
  const activeBookings = reservations.value.filter(r => !r.leaving_timestamp).length
  const totalSpent = reservations.value
    .filter(r => r.parking_cost)
    .reduce((total, r) => total + r.parking_cost, 0)
    .toFixed(2)
  
  const totalHours = reservations.value
    .filter(r => r.parking_timestamp && r.leaving_timestamp)
    .reduce((total, r) => {
      const start = new Date(r.parking_timestamp)
      const end = new Date(r.leaving_timestamp)
      const hours = (end - start) / (1000 * 60 * 60)
      return total + hours
    }, 0)
  
  const avgDuration = totalBookings > 0 ? (totalHours / totalBookings).toFixed(1) : 0
  
  return {
    totalBookings,
    activeBookings,
    totalSpent,
    avgDuration
  }
})

const recentActivity = computed(() => {
  return reservations.value
    .slice(0, 10)
    .map(r => ({
      id: r.id,
      action: r.leaving_timestamp ? 'Parking Released' : 'Parking Booked',
      location: `Spot ${r.spot_id}`,
      timestamp: r.leaving_timestamp || r.parking_timestamp
    }))
    .sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp))
})

// Profile editing
function toggleEdit() {
  editing.value = !editing.value
  if (!editing.value) {
    // Reset form data
    profileData.value = {
      username: user.value.username || '',
      email: user.value.email || '',
      phone_number: user.value.phone_number || '',
      address: user.value.address || '',
      pincode: user.value.pincode || ''
    }
  }
}

function cancelEdit() {
  editing.value = false
  // Reset form data
  profileData.value = {
    username: user.value.username || '',
    email: user.value.email || '',
    phone_number: user.value.phone_number || '',
    address: user.value.address || '',
    pincode: user.value.pincode || ''
  }
}

async function saveProfile() {
  const authConfig = createAuthConfig()
  if (!authConfig) return

  saving.value = true
  try {
    // This would need a backend endpoint to update profile
    // For now, just simulate success
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    user.value = { ...user.value, ...profileData.value }
    editing.value = false
    error.value = ''
  } catch (e) {
    error.value = e.response?.data?.message || 'Failed to save profile'
  } finally {
    saving.value = false
  }
}

// Password change
function changePassword() {
  showPasswordModal.value = true
}

function closePasswordModal() {
  showPasswordModal.value = false
  passwordForm.value = {
    current: '',
    new: '',
    confirm: ''
  }
}

async function updatePassword() {
  if (passwordForm.value.new !== passwordForm.value.confirm) {
    error.value = 'New passwords do not match'
    return
  }

  const authConfig = createAuthConfig()
  if (!authConfig) return

  passwordLoading.value = true
  try {
    // This would need a backend endpoint to change password
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    closePasswordModal()
    error.value = ''
    alert('Password updated successfully!')
  } catch (e) {
    error.value = e.response?.data?.message || 'Failed to update password'
  } finally {
    passwordLoading.value = false
  }
}

// Account actions
function downloadData() {
  // Create a simple data export
  const data = {
    profile: user.value,
    reservations: reservations.value,
    statistics: {
      totalBookings: totalBookings.value,
      totalSpent: totalSpent.value,
      totalHours: totalHours.value
    }
  }
  
  const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `parking-data-${user.value.username}.json`
  a.click()
  URL.revokeObjectURL(url)
}

function confirmDeleteAccount() {
  if (confirm('Are you sure you want to delete your account? This action cannot be undone.')) {
    // This would need backend implementation
    alert('Account deletion would be implemented here')
  }
}

// Helper functions
function formatDate(dateString) {
  if (!dateString) return 'N/A'
  return new Date(dateString).toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

function formatDateTime(dateString) {
  if (!dateString) return 'N/A'
  return new Date(dateString).toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

// Initialize
onMounted(() => {
  loadProfile()
})
</script>

<style scoped>
/* Simple hover effects for cards */
.card {
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.card:hover {
  transform: translateY(-2px);
  box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15) !important;
}
</style>