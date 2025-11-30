<template>
  <div class="page">
    <div class="page-header">
      <div class="container">
        <div class="header-content">
          <div>
            <h1 class="page-title">Parking Spots</h1>
            <p class="page-subtitle">Monitor and manage all parking spots</p>
          </div>
          <div class="header-actions">
            <div class="dropdown">
              <button 
                class="btn btn-outline-primary dropdown-toggle d-flex align-items-center gap-2" 
                type="button" 
                data-bs-toggle="dropdown" 
                aria-expanded="false"
              >
                <span></span>
                <span>{{ selectedLotName || 'All Lots' }}</span>
              </button>
              <ul class="dropdown-menu">
                <li>
                  <a 
                    class="dropdown-item d-flex align-items-center gap-2" 
                    href="#" 
                    @click.prevent="selectLot('', 'All Lots')"
                    :class="{ 'active': selectedLot === '' }"
                  >
                    <span></span>
                    <span>All Lots</span>
                    <span v-if="selectedLot === ''" class="ms-auto text-primary">✓</span>
                  </a>
                </li>
                <li><hr class="dropdown-divider"></li>
                <li v-for="lot in lots" :key="lot.id">
                  <a 
                    class="dropdown-item d-flex align-items-center gap-2" 
                    href="#" 
                    @click.prevent="selectLot(lot.id, lot.prime_location_name)"
                    :class="{ 'active': selectedLot === lot.id.toString() }"
                  >
                    <span>🅿️</span>
                    <div class="flex-grow-1">
                      <div>{{ lot.prime_location_name }}</div>
                      <small class="text-muted">{{ lot.available_spots }}/{{ lot.number_of_spots }} available</small>
                    </div>
                    <span v-if="selectedLot === lot.id.toString()" class="text-primary">✓</span>
                  </a>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="container">
      <div v-if="error" class="alert alert-danger">{{ error }}</div>
      
      <div v-if="loading" class="loading">
        <div class="spinner"></div>
        <p>Loading spots...</p>
      </div>
      
      <div v-else>
        <div class="row g-3 mb-4">
          <div class="col-xl-3 col-lg-3 col-md-6 col-sm-6">
            <div class="card text-center h-100 shadow-sm">
              <div class="card-body">
                <div class="fs-1 mb-3"></div>
                <h3 class="text-primary fw-bold mb-1">{{ totalSpots }}</h3>
                <p class="text-muted small mb-0">TOTAL SPOTS</p>
              </div>
            </div>
          </div>
          
          <div class="col-xl-3 col-lg-3 col-md-6 col-sm-6">
            <div class="card text-center h-100 shadow-sm">
              <div class="card-body">
                <div class="fs-1 mb-3 text-success"></div>
                <h3 class="text-success fw-bold mb-1">{{ availableSpots }}</h3>
                <p class="text-muted small mb-0">AVAILABLE</p>
              </div>
            </div>
          </div>
          
          <div class="col-xl-3 col-lg-3 col-md-6 col-sm-6">
            <div class="card text-center h-100 shadow-sm">
              <div class="card-body">
                <div class="fs-1 mb-3 text-danger"></div>
                <h3 class="text-danger fw-bold mb-1">{{ occupiedSpots }}</h3>
                <p class="text-muted small mb-0">OCCUPIED</p>
              </div>
            </div>
          </div>
          
          <div class="col-xl-3 col-lg-3 col-md-6 col-sm-6">
            <div class="card text-center h-100 shadow-sm">
              <div class="card-body">
                <div class="fs-1 mb-3 text-info"></div>
                <h3 class="text-info fw-bold mb-1">{{ utilizationRate }}%</h3>
                <p class="text-muted small mb-0">UTILIZATION</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Spots by Lot -->
        <div v-if="groupedSpots.length === 0" class="empty-state">
          <div class="empty-icon"></div>
          <h3>No parking spots found</h3>
          <p>Create parking lots to see spots here</p>
        </div>

        <div v-else class="lots-container">
          <div v-for="lotGroup in groupedSpots" :key="lotGroup.lot.id" class="lot-section card mb-4">
            <div class="card-header">
              <div class="lot-header">
                <div class="lot-info">
                  <h3 class="lot-name">{{ lotGroup.lot.prime_location_name }}</h3>
                  <p class="lot-address">{{ lotGroup.lot.address }}</p>
                </div>
                <div class="lot-stats">
                  <div class="lot-stat">
                    <span class="stat-value">{{ lotGroup.available }}</span>
                    <span class="stat-label">Available</span>
                  </div>
                  <div class="lot-stat">
                    <span class="stat-value">{{ lotGroup.occupied }}</span>
                    <span class="stat-label">Occupied</span>
                  </div>
                  <div class="lot-stat">
                    <span class="stat-value">{{ lotGroup.total }}</span>
                    <span class="stat-label">Total</span>
                  </div>
                </div>
              </div>
            </div>
            
            <div class="card-body">
              <div class="spots-grid">
                <div 
                  v-for="spot in lotGroup.spots" 
                  :key="spot.id" 
                  class="spot-card"
                  :class="{ 
                    'available': spot.status === 'A', 
                    'occupied': spot.status === 'O' 
                  }"
                >
                  <div class="spot-number">{{ spot.spot_number }}</div>
                  <div class="spot-status">
                    {{ spot.status === 'A' ? 'Available' : 'Occupied' }}
                  </div>
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
import { useRoute } from 'vue-router'

const route = useRoute()
const loading = ref(false)
const error = ref('')
const spots = ref([])
const lots = ref([])
const selectedLot = ref('')
const selectedLotName = ref('All Lots')

function createAuthConfig() {
  const token = localStorage.getItem('token')
  return {
    headers: { Authorization: `Bearer ${token}` }
  }
}

async function loadSpots() {
  loading.value = true
  try {
    const response = await axios.get('http://localhost:5000/api/spots', createAuthConfig())
    spots.value = response.data
  } catch (e) {
    error.value = e.response?.data?.message || 'Failed to load spots'
  } finally {
    loading.value = false
  }
}

async function loadLots() {
  try {
    const response = await axios.get('http://localhost:5000/api/lots', createAuthConfig())
    lots.value = response.data
  } catch (e) {
    console.error('Failed to load lots:', e)
  }
}

const totalSpots = computed(() => spots.value.length)
const availableSpots = computed(() => spots.value.filter(s => s.status === 'A').length)
const occupiedSpots = computed(() => spots.value.filter(s => s.status === 'O').length)
const utilizationRate = computed(() => {
  if (totalSpots.value === 0) return 0
  return Math.round((occupiedSpots.value / totalSpots.value) * 100)
})

const filteredSpots = computed(() => {
  if (!selectedLot.value) return spots.value
  return spots.value.filter(spot => spot.lot_id === parseInt(selectedLot.value))
})

const groupedSpots = computed(() => {
  const groups = {}
  filteredSpots.value.forEach(spot => {
    if (!groups[spot.lot_id]) {
      const lot = lots.value.find(l => l.id === spot.lot_id) || {
        id: spot.lot_id,
        prime_location_name: spot.lot_name || 'Unknown Lot',
        address: spot.lot_address || 'Unknown Address'
      }
      groups[spot.lot_id] = {
        lot,
        spots: [],
        total: 0,
        available: 0,
        occupied: 0
      }
    }
    groups[spot.lot_id].spots.push(spot)
    groups[spot.lot_id].total++
    if (spot.status === 'A') {
      groups[spot.lot_id].available++
    } else {
      groups[spot.lot_id].occupied++
    }
  })
  return Object.values(groups)
})

function selectLot(lotId, lotName) {
  selectedLot.value = lotId.toString()
  selectedLotName.value = lotName
}

function filterByLot() {
  // Filtering is handled by computed property
}

onMounted(async () => {
  // Check if we have a lot filter from query params
  if (route.query.lot) {
    selectedLot.value = route.query.lot
  }
  await Promise.all([loadSpots(), loadLots()])
})
</script>

<style scoped>
.header-content {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
}

.header-actions {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.stats-grid {
  margin-bottom: 2rem;
}

.stat-card {
  transition: all 0.2s ease;
}

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-lg);
}

.stat-icon {
  font-size: 2rem;
  margin-bottom: 0.5rem;
}

.stat-icon.available {
  color: var(--success-color);
}

.stat-icon.occupied {
  color: var(--danger-color);
}

.stat-number {
  font-size: 2rem;
  font-weight: 700;
  color: var(--primary-color);
  margin-bottom: 0.25rem;
}

.stat-label {
  color: var(--gray-600);
  font-size: 0.875rem;
  font-weight: 500;
}

.lot-section {
  margin-bottom: 2rem;
}

.lot-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.lot-name {
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--gray-800);
  margin: 0 0 0.25rem 0;
}

.lot-address {
  color: var(--gray-600);
  margin: 0;
  font-size: 0.875rem;
}

.lot-stats {
  display: flex;
  gap: 2rem;
}

.lot-stat {
  text-align: center;
}

.stat-value {
  display: block;
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--primary-color);
}

.stat-label {
  font-size: 0.75rem;
  color: var(--gray-600);
  text-transform: uppercase;
  font-weight: 500;
}

.spots-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
  gap: 1rem;
  margin-top: 1rem;
}

.spot-card {
  background: var(--white);
  border: 2px solid var(--gray-300);
  border-radius: var(--border-radius);
  padding: 1rem;
  text-align: center;
  transition: all 0.2s ease;
  cursor: pointer;
}

.spot-card:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}

.spot-card.available {
  border-color: var(--success-color);
  background: #f0fdf4;
}

.spot-card.available:hover {
  background: #dcfce7;
}

.spot-card.occupied {
  border-color: var(--danger-color);
  background: #fef2f2;
}

.spot-card.occupied:hover {
  background: #fee2e2;
}

.spot-number {
  font-size: 1.25rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
}

.spot-card.available .spot-number {
  color: var(--success-color);
}

.spot-card.occupied .spot-number {
  color: var(--danger-color);
}

.spot-status {
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
}

.spot-card.available .spot-status {
  color: var(--success-color);
}

.spot-card.occupied .spot-status {
  color: var(--danger-color);
}

.empty-state {
  text-align: center;
  padding: 4rem 2rem;
}

.empty-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
}

.empty-state h3 {
  color: var(--gray-800);
  margin-bottom: 0.5rem;
}

.empty-state p {
  color: var(--gray-600);
}

.dropdown-menu {
  min-width: 300px;
  max-height: 400px;
  overflow-y: auto;
}

.dropdown-item {
  padding: 0.75rem 1rem;
  border-bottom: 1px solid #f8f9fa;
}

.dropdown-item:last-child {
  border-bottom: none;
}

.dropdown-item:hover {
  background-color: #f8f9fa;
}

.dropdown-item.active {
  background-color: #e3f2fd;
  color: #1976d2;
}

.dropdown-toggle {
  min-width: 200px;
  justify-content: space-between;
}

@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    gap: 1rem;
    align-items: stretch;
  }

  .lot-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }

  .lot-stats {
    gap: 1rem;
  }

  .spots-grid {
    grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
    gap: 0.75rem;
  }

  .spot-card {
    padding: 0.75rem;
  }

  .dropdown-menu {
    min-width: 250px;
  }

  .dropdown-toggle {
    min-width: 150px;
  }
}
</style>