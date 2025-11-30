<template>
  <div class="bg-light min-vh-100">
    <div class="bg-primary bg-opacity-10 py-3 border-bottom">
      <div class="container">
        <div class="d-flex justify-content-between align-items-center">
          <div>
            <h1 class="h4 fw-bold mb-2">Parking Lots</h1>
            <p class="text-muted mb-0">Manage and monitor all parking lots</p>
          </div>
          <div class="d-flex gap-3">
            <button class="btn btn-primary" @click="showAddModal = true">
              <i class="fas fa-plus me-1"></i>
              Add New Lot
            </button>
          </div>
        </div>
      </div>
    </div>

    <div class="container py-4">
      <div v-if="error" class="alert alert-danger">{{ error }}</div>
      
      <div v-if="loading" class="text-center py-5">
        <div class="spinner-border text-primary mb-3"></div>
        <p class="text-muted">Loading lots...</p>
      </div>
      
      <div v-else>
        <div class="row g-4">
          <div v-for="lot in lots" :key="lot.id" class="col-lg-6 col-xl-4">
            <div class="card h-100 lot-card">
              <div class="card-body">
                <div class="d-flex justify-content-between align-items-start mb-3">
                  <h5 class="card-title fw-bold mb-0">{{ lot.prime_location_name }}</h5>
                  <span class="badge" :class="lot.available_spots > 0 ? 'bg-success' : 'bg-danger'">
                    {{ lot.available_spots > 0 ? 'Available' : 'Full' }}
                  </span>
                </div>
                
                <div class="mb-3">
                  <div class="d-flex align-items-center mb-2">
                    <i class="fas fa-map-marker-alt text-muted me-2"></i>
                    <span class="text-muted">{{ lot.address }}</span>
                  </div>
                  <div class="d-flex align-items-center mb-2">
                    <i class="fas fa-hashtag text-muted me-2"></i>
                    <span class="text-muted">Pin: {{ lot.pin_code }}</span>
                  </div>
                  <div class="d-flex align-items-center mb-2">
                    <i class="fas fa-money-bill text-muted me-2"></i>
                    <span class="text-muted">₹{{ lot.price_per_hour }}/hour</span>
                  </div>
                  <div class="d-flex align-items-center">
                    <i class="fas fa-car text-muted me-2"></i>
                    <span class="text-muted">{{ lot.available_spots }}/{{ lot.number_of_spots }} spots available</span>
                  </div>
                </div>
                
                <div class="d-flex gap-2">
                  <button class="btn btn-outline-primary btn-sm" @click="viewSpots(lot)">
                    <i class="fas fa-eye me-1"></i>
                    View Spots
                  </button>
                  <button class="btn btn-outline-warning btn-sm" @click="openEditModal(lot)">
                    <i class="fas fa-edit me-1"></i>
                    Edit
                  </button>
                  <button class="btn btn-outline-danger btn-sm" @click="deleteLot(lot)">
                    <i class="fas fa-trash me-1"></i>
                    Delete
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <div v-if="lots.length === 0" class="text-center py-5">
          <div class="fs-1 text-muted mb-3">🏢</div>
          <h3 class="text-muted">No parking lots found</h3>
          <p class="text-muted">Create your first parking lot to get started</p>
          <button class="btn btn-primary" @click="showAddModal = true">
            <i class="fas fa-plus me-1"></i>
            Add New Lot
          </button>
        </div>
      </div>
    </div>

    <!-- Add/Edit Modal -->
    <div v-if="showAddModal || showEditModal" class="modal fade show d-block" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title fw-bold">{{ showEditModal ? 'Edit Lot' : 'Add New Lot' }}</h5>
            <button type="button" class="btn-close" @click="closeModals"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="showEditModal ? updateLot() : addLot()">
              <div class="mb-3">
                <label class="form-label fw-semibold">Prime Location Name</label>
                <input v-model="lotForm.prime_location_name" type="text" class="form-control" required>
              </div>
              
              <div class="mb-3">
                <label class="form-label fw-semibold">Address</label>
                <input v-model="lotForm.address" type="text" class="form-control" required>
              </div>
              
              <div class="row">
                <div class="col-md-6 mb-3">
                  <label class="form-label fw-semibold">Pin Code</label>
                  <input v-model="lotForm.pin_code" type="text" class="form-control" required>
                </div>
                <div class="col-md-6 mb-3">
                  <label class="form-label fw-semibold">Price per Hour (₹)</label>
                  <input v-model="lotForm.price_per_hour" type="number" class="form-control" required>
                </div>
              </div>
              
              <div class="mb-3">
                <label class="form-label fw-semibold">Number of Spots</label>
                <input v-model="lotForm.number_of_spots" type="number" class="form-control" required>
              </div>
              
              <div class="d-flex gap-2 justify-content-end">
                <button type="button" class="btn btn-secondary" @click="closeModals">Cancel</button>
                <button type="submit" class="btn btn-primary" :disabled="loading">
                  <span v-if="loading" class="spinner-border spinner-border-sm me-1"></span>
                  {{ loading ? 'Saving...' : (showEditModal ? 'Update Lot' : 'Add Lot') }}
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
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const router = useRouter()
const lots = ref([])
const loading = ref(false)
const error = ref('')
const showAddModal = ref(false)
const showEditModal = ref(false)
const editingLot = ref(null)

const lotForm = ref({
  prime_location_name: '',
  address: '',
  pin_code: '',
  price_per_hour: '',
  number_of_spots: ''
})

function createAuthConfig() {
  const token = localStorage.getItem('token')
  if (!token) {
    router.push('/admin-login')
    return null
  }
  return {
    headers: { Authorization: `Bearer ${token}` }
  }
}

async function loadLots() {
  const authConfig = createAuthConfig()
  if (!authConfig) return

  loading.value = true
  try {
    const response = await axios.get('http://localhost:5000/api/admin/lots', authConfig)
    lots.value = response.data
  } catch (e) {
    if (e.response?.status === 401) {
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      router.push('/admin-login')
      return
    }
    error.value = e.response?.data?.message || 'Failed to load lots'
  } finally {
    loading.value = false
  }
}

async function addLot() {
  const authConfig = createAuthConfig()
  if (!authConfig) return

  loading.value = true
  try {
    await axios.post('http://localhost:5000/api/admin/lots', lotForm.value, authConfig)
    await loadLots()
    closeModals()
  } catch (e) {
    if (e.response?.status === 401) {
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      router.push('/admin-login')
      return
    }
    error.value = e.response?.data?.message || 'Failed to add lot'
  } finally {
    loading.value = false
  }
}

async function updateLot() {
  loading.value = true
  try {
    await axios.put(`http://localhost:5000/api/admin/lots/${editingLot.value.id}`, lotForm.value, createAuthConfig())
    await loadLots()
    closeModals()
  } catch (e) {
    error.value = e.response?.data?.message || 'Failed to update lot'
  } finally {
    loading.value = false
  }
}

async function deleteLot(lot) {
  if (!confirm(`Are you sure you want to delete "${lot.prime_location_name}"?`)) return
  
  loading.value = true
  try {
    await axios.delete(`http://localhost:5000/api/admin/lots/${lot.id}`, createAuthConfig())
    await loadLots()
  } catch (e) {
    error.value = e.response?.data?.message || 'Failed to delete lot'
  } finally {
    loading.value = false
  }
}

function openEditModal(lot) {
  editingLot.value = lot
  lotForm.value = { ...lot }
  showEditModal.value = true
}

function closeModals() {
  showAddModal.value = false
  showEditModal.value = false
  editingLot.value = null
  lotForm.value = {
    prime_location_name: '',
    address: '',
    pin_code: '',
    price_per_hour: '',
    number_of_spots: ''
  }
}

function viewSpots(lot) {
  router.push(`/spots?lot=${lot.id}`)
}

onMounted(() => {
  loadLots()
})
</script>

<style scoped>
/* Simple hover effects for cards */
.lot-card {
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.lot-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15) !important;
}

/* Modal backdrop */
.modal.show {
  background-color: rgba(0, 0, 0, 0.5);
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .card-body {
    padding: 1rem;
  }
}
</style>