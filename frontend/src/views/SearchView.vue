<template>
  <div class="bg-light min-vh-100">
    <div class="bg-primary bg-opacity-10 py-3 border-bottom">
      <div class="container">
        <h1 class="h4 fw-bold mb-2">Search Parking</h1>
        <p class="text-muted mb-0">Find parking spots by location or pin code</p>
      </div>
    </div>

    <div class="container py-4">
      <!-- Search Section -->
      <div class="card shadow-sm mb-4">
        <div class="card-body">
          <div class="row g-3">
            <div class="col-md-8">
              <input 
                v-model="searchQuery" 
                type="text" 
                class="form-control" 
                placeholder="Enter location, address, or pin code"
                @keyup.enter="performSearch"
              >
            </div>
            <div class="col-md-4">
              <button class="btn btn-primary w-100" @click="performSearch" :disabled="loading">
                <span v-if="loading">
                  <span class="spinner-border spinner-border-sm me-2"></span>
                  Searching...
                </span>
                <span v-else>Search</span>
              </button>
            </div>
          </div>
          <div class="row g-3 mt-3">
            <div class="col-12">
              <div class="d-flex gap-3 flex-wrap">
                <div class="form-check">
                  <input class="form-check-input" type="radio" v-model="searchType" value="all" name="searchType" id="all">
                  <label class="form-check-label" for="all">All Results</label>
                </div>
                <div class="form-check">
                  <input class="form-check-input" type="radio" v-model="searchType" value="lots" name="searchType" id="lots">
                  <label class="form-check-label" for="lots">Parking Lots Only</label>
                </div>
                <div class="form-check">
                  <input class="form-check-input" type="radio" v-model="searchType" value="available" name="searchType" id="available">
                  <label class="form-check-label" for="available">Available Only</label>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Error Display -->
      <div v-if="error" class="alert alert-danger">
        {{ error }}
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="text-center py-5">
        <div class="spinner-border text-primary mb-3" role="status"></div>
        <p class="text-muted">Searching...</p>
      </div>

      <!-- Search Results -->
      <div v-else-if="hasSearched">
        <!-- Results Summary -->
        <div class="mb-4">
          <h2 class="h5 fw-bold mb-2">
            Search Results for "{{ currentQuery }}"
          </h2>
          <p class="text-muted mb-0">
            Found {{ filteredResults.length }} result(s)
          </p>
        </div>

        <!-- No Results -->
        <div v-if="filteredResults.length === 0" class="text-center py-5">
          <div class="fs-1 mb-3">🔍</div>
          <h3 class="h5 fw-bold mb-2">No results found</h3>
          <p class="text-muted mb-4">Try searching with different keywords or check your spelling.</p>
          <div class="card shadow-sm">
            <div class="card-body">
              <h4 class="h6 fw-bold mb-3">Search suggestions:</h4>
              <ul class="text-start text-muted">
                <li>Try searching by area name (e.g., "Downtown", "Mall")</li>
                <li>Use pin codes (e.g., "400001", "110001")</li>
                <li>Search by landmark names</li>
              </ul>
            </div>
          </div>
        </div>

        <!-- Results Grid -->
        <div v-else class="row g-4">
          <div v-for="lot in filteredResults" :key="lot.id" class="col-lg-6 col-xl-4">
            <div class="card shadow-sm result-card h-100">
              <div class="card-body">
                <div class="d-flex justify-content-between align-items-start mb-3">
                  <h3 class="h6 fw-bold mb-1">{{ lot.prime_location_name }}</h3>
                  <span class="badge" :class="lot.available_spots > 0 ? 'bg-success' : 'bg-danger'">
                    {{ lot.available_spots > 0 ? 'Available' : 'Full' }}
                  </span>
                </div>
                
                <div class="mb-3">
                  <div class="d-flex justify-content-between mb-2">
                    <small class="text-muted">📍 Address:</small>
                    <small class="text-dark">{{ lot.address }}</small>
                  </div>
                  <div class="d-flex justify-content-between mb-2">
                    <small class="text-muted">📮 Pin Code:</small>
                    <small class="text-dark">{{ lot.pin_code }}</small>
                  </div>
                  <div class="d-flex justify-content-between mb-2">
                    <small class="text-muted">🚗 Available Spots:</small>
                    <small class="text-dark">{{ lot.available_spots }}/{{ lot.total_spots }}</small>
                  </div>
                  <div class="d-flex justify-content-between">
                    <small class="text-muted">💰 Rate:</small>
                    <small class="text-dark">₹{{ lot.rate_per_hour }}/hour</small>
                  </div>
                </div>
                
                <div class="d-flex gap-2">
                  <button 
                    class="btn btn-primary btn-sm flex-fill" 
                    @click="bookSpot(lot)"
                    :disabled="lot.available_spots === 0"
                  >
                    Book Spot
                  </button>
                  <button 
                    class="btn btn-outline-secondary btn-sm" 
                    @click="viewDetails(lot)"
                  >
                    Details
                  </button>
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
import { ref, onMounted, computed, watch } from 'vue'
import axios from 'axios'
import { useRouter, useRoute } from 'vue-router'

const router = useRouter()
const route = useRoute()

// Reactive data
const loading = ref(false)
const bookingLoading = ref(false)
const error = ref('')
const searchQuery = ref('')
const currentQuery = ref('')
const searchType = ref('all')
const searchResults = ref([])
const hasSearched = ref(false)
const showBookModal = ref(false)
const selectedLot = ref(null)

// User data
const user = ref(null)
const userReservations = ref([])

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

// Computed properties
const isAdmin = computed(() => {
  const userData = localStorage.getItem('user')
  if (userData) {
    try {
      return JSON.parse(userData).role === 'admin'
    } catch (e) {
      return false
    }
  }
  return false
})

const hasActiveBooking = computed(() => {
  return userReservations.value.some(r => !r.leaving_timestamp)
})

const filteredResults = computed(() => {
  let results = searchResults.value
  
  if (searchType.value === 'available') {
    results = results.filter(lot => lot.available_spots > 0)
  }
  
  return results
})

// Search functionality
async function performSearch() {
  if (!searchQuery.value.trim()) return
  
  const authConfig = createAuthConfig()
  if (!authConfig) return
  
  loading.value = true
  error.value = ''
  currentQuery.value = searchQuery.value.trim()
  
  try {
    const endpoint = isAdmin.value ? '/api/admin/search' : '/api/lots'
    const params = isAdmin.value ? { q: currentQuery.value, type: 'lots' } : {}
    
    const response = await axios.get(`http://localhost:5000${endpoint}`, {
      ...authConfig,
      params
    })
    
    if (isAdmin.value) {
      searchResults.value = response.data.lots || []
    } else {
      // Filter lots based on search query
      const allLots = response.data || []
      searchResults.value = allLots.filter(lot => 
        lot.prime_location_name?.toLowerCase().includes(currentQuery.value.toLowerCase()) ||
        lot.address?.toLowerCase().includes(currentQuery.value.toLowerCase()) ||
        lot.pin_code?.includes(currentQuery.value)
      )
    }
    
    hasSearched.value = true
  } catch (e) {
    if (e.response?.status === 401) {
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      router.push('/login')
      return
    }
    error.value = e.response?.data?.message || 'Search failed'
  } finally {
    loading.value = false
  }
}

function quickSearch(query) {
  searchQuery.value = query
  performSearch()
}

// Booking functionality
async function bookSpot(lot) {
  selectedLot.value = lot
  showBookModal.value = true
}

async function confirmBooking() {
  if (!selectedLot.value) return
  
  const authConfig = createAuthConfig()
  if (!authConfig) return
  
  bookingLoading.value = true
  try {
    await axios.post('http://localhost:5000/api/reserve', {
      lot_id: selectedLot.value.id
    }, authConfig)
    
    closeModal()
    // Refresh search results
    await performSearch()
    error.value = ''
  } catch (e) {
    if (e.response?.status === 401) {
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      router.push('/login')
      return
    }
    error.value = e.response?.data?.message || 'Booking failed'
  } finally {
    bookingLoading.value = false
  }
}

function closeModal() {
  showBookModal.value = false
  selectedLot.value = null
}

function viewDetails(lot) {
  if (isAdmin.value) {
    router.push(`/spots?lot=${lot.id}`)
  } else {
    // Could open a details modal or navigate to a details page
    alert(`Lot Details:\n${lot.prime_location_name}\n${lot.address}\nPrice: ₹${lot.price_per_hour}/hour`)
  }
}

// Load user data for booking checks
async function loadUserData() {
  if (isAdmin.value) return
  
  const authConfig = createAuthConfig()
  if (!authConfig) return
  
  try {
    const response = await axios.get('http://localhost:5000/user/dashboard', authConfig)
    user.value = response.data.user
    userReservations.value = response.data.my_reservations || []
  } catch (e) {
    // Silently fail for user data loading
    console.error('Failed to load user data:', e)
  }
}

// Initialize
onMounted(() => {
  // Check for search query in URL
  if (route.query.q) {
    searchQuery.value = route.query.q
    performSearch()
  }
  
  loadUserData()
})

// Watch for route changes
watch(() => route.query.q, (newQuery) => {
  if (newQuery && newQuery !== searchQuery.value) {
    searchQuery.value = newQuery
    performSearch()
  }
})
</script>

<style scoped>
/* Simple hover effects for cards */
.result-card {
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.result-card:hover {
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