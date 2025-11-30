<template>
  <div class="bg-light min-vh-100">
    <!-- Header -->
    <div class="bg-primary bg-opacity-10 py-3 border-bottom">
      <div class="container">
        <h1 class="h4 fw-bold mb-2">My Parking Summary</h1>
        <p class="text-muted mb-0">Your personal parking usage and statistics</p>
      </div>
    </div>

    <div class="container py-4">
      <div v-if="error" class="alert alert-danger">{{ error }}</div>

      <div v-if="loading" class="text-center py-5">
        <div class="spinner-border text-primary mb-3"></div>
        <p class="text-muted">Loading your summary...</p>
      </div>

      <!-- MAIN CONTENT -->
      <div v-else>
        <!-- Stats Section -->
        <div class="mb-5">
          <h2 class="h4 text-primary mb-4">Your Parking Stats</h2>

          <div class="row g-4">
            <div class="col-lg-3 col-md-6">
              <div class="card text-center stat-card">
                <div class="card-body">
                  <div class="h3 text-primary fw-bold">{{ userStats.total_reservations }}</div>
                  <div class="text-muted small mb-2">Total Bookings</div>
                </div>
              </div>
            </div>

            <div class="col-lg-3 col-md-6">
              <div class="card text-center stat-card">
                <div class="card-body">
                  <div class="h3 text-primary fw-bold">{{ userStats.active_reservations }}</div>
                  <div class="text-muted small mb-2">Active Reservations</div>
                </div>
              </div>
            </div>

            <div class="col-lg-3 col-md-6">
              <div class="card text-center stat-card">
                <div class="card-body">
                  <div class="h3 text-primary fw-bold">₹{{ userStats.total_spent }}</div>
                  <div class="text-muted small mb-2">Total Spent</div>
                </div>
              </div>
            </div>

            <div class="col-lg-3 col-md-6">
              <div class="card text-center stat-card">
                <div class="card-body">
                  <div class="h3 text-primary fw-bold">{{ userStats.completed_reservations }}</div>
                  <div class="text-muted small mb-2">Completed Bookings</div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Recent Reservations + Quick Stats -->
        <div class="mb-5">
          <h2 class="h4 text-primary mb-4">Recent Activity</h2>

          <div class="row g-4">
            <!-- Recent Reservations -->
            <div class="col-lg-8">
              <div class="card h-100">
                <div class="card-header">
                  <h5 class="card-title mb-1">🚗 Recent Reservations</h5>
                </div>

                <div class="card-body">
                  <div v-if="userReservations.length === 0" class="text-center text-muted py-4">
                    <p>No reservations yet</p>
                  </div>

                  <div v-else>
                    <div
                      v-for="reservation in userReservations.slice(0, 5)"
                      :key="reservation.id"
                      class="d-flex align-items-center gap-3 mb-3 p-3 bg-light rounded"
                    >
                      <div class="flex-grow-1">
                        <div class="fw-medium">Spot #{{ reservation.spot_id }}</div>
                        <small class="text-muted">
                          {{ new Date(reservation.parking_timestamp).toLocaleDateString() }}
                        </small>
                      </div>
                      <div class="text-end">
                        <div class="fw-bold text-success">₹{{ reservation.parking_cost }}</div>
                        <small class="text-muted">{{ reservation.status }}</small>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Quick Stats -->
            <div class="col-lg-4">
              <div class="card h-100">
                <div class="card-header">
                  <h5 class="card-title mb-1">Quick Stats</h5>
                </div>
                <div class="card-body">
                  <div class="row g-3">
                    <div class="col-12">
                      <div class="text-center p-3 bg-success bg-opacity-10 rounded">
                        <div class="h4 text-success mb-1">{{ userStats.total_reservations }}</div>
                        <small class="text-muted">Total Bookings</small>
                      </div>
                    </div>

                    <div class="col-12">
                      <div class="text-center p-3 bg-warning bg-opacity-10 rounded">
                        <div class="h4 text-warning mb-1">{{ userStats.active_reservations }}</div>
                        <small class="text-muted">Active Now</small>
                      </div>
                    </div>

                    <div class="col-12">
                      <div class="text-center p-3 bg-info bg-opacity-10 rounded">
                        <div class="h4 text-info mb-1">₹{{ userStats.total_spent }}</div>
                        <small class="text-muted">Total Spent</small>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Hourly Pattern (FIXED POSITION) -->
          <div class="card mt-4">
            <div class="card-header">
              <h5 class="card-title mb-1">Hourly Parking Pattern</h5>
            </div>

            <div class="card-body">
              <div class="d-flex align-items-end gap-1" style="height: 100px;">
                <div
                  v-for="(hour, index) in hourlyPatterns"
                  :key="index"
                  class="bg-info rounded-top flex-fill"
                  :style="{ height: (hour.activity / maxHourlyActivity * 100) + '%' }"
                ></div>
              </div>

              <div class="d-flex justify-content-between mt-2">
                <small class="text-muted">6AM</small>
                <small class="text-muted">12PM</small>
                <small class="text-muted">6PM</small>
                <small class="text-muted">12AM</small>
              </div>
            </div>
          </div>
        </div>

        <!-- Insights -->
        <div class="mb-5">
          <h2 class="h4 text-primary mb-4">💡 Insights</h2>

          <div class="row g-4">
            <div class="col-lg-4 col-md-6">
              <div class="card stat-card">
                <div class="card-body">
                  <h6 class="mb-1">Peak Usage Time</h6>
                  <p class="text-muted small mb-0">{{ insights.peakTime }}</p>
                </div>
              </div>
            </div>

            <div class="col-lg-4 col-md-6">
              <div class="card stat-card">
                <div class="card-body">
                  <h6 class="mb-1">Average Cost</h6>
                  <p class="text-muted small mb-0">₹{{ insights.avgCost }} per session</p>
                </div>
              </div>
            </div>

            <div class="col-lg-4 col-md-6">
              <div class="card stat-card">
                <div class="card-body">
                  <h6 class="mb-1">Favorite Location</h6>
                  <p class="text-muted small mb-0">{{ insights.favoriteLocation }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>

      </div><!-- main content end -->
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

const user = ref({})
const userReservations = ref([])
const availableLots = ref([])

const userStats = ref({
  total_reservations: 0,
  active_reservations: 0,
  completed_reservations: 0,
  total_spent: 0
})

const insights = computed(() => {
  const completedReservations = userReservations.value.filter(r => r.status === 'completed')
  const totalCost = completedReservations.reduce((sum, r) => sum + (r.parking_cost || 0), 0)
  const avgCost = completedReservations.length > 0 ? Math.round(totalCost / completedReservations.length) : 0

  return {
    peakTime: 'Based on your usage',
    avgCost,
    favoriteLocation: availableLots.value[0]?.prime_location_name || 'No data'
  }
})

function createAuthConfig() {
  const token = localStorage.getItem('token')
  const user = localStorage.getItem('user')

  if (!token || !user) {
    router.push('/login')
    return null
  }

  return { headers: { Authorization: `Bearer ${token}` } }
}

async function loadUserSummary() {
  const authConfig = createAuthConfig()
  if (!authConfig) return

  loading.value = true

  try {
    const response = await axios.get('http://localhost:5000/user/dashboard', authConfig)

    if (response.data) {
      userStats.value = {
        total_reservations: response.data.my_reservations?.length || 0,
        active_reservations: response.data.my_reservations?.filter(r => r.status === 'active').length || 0,
        completed_reservations: response.data.my_reservations?.filter(r => r.status === 'completed').length || 0,
        total_spent: response.data.my_reservations?.reduce((s, r) => s + (r.parking_cost || 0), 0)
      }

      userReservations.value = response.data.my_reservations || []
      availableLots.value = response.data.available_parking_lots || []
      user.value = response.data.user || {}
    }
  } catch (e) {
    if (e.response?.status === 401) {
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      router.push('/login')
    }

    error.value = e.response?.data?.message || 'Failed to load summary'
  } finally {
    loading.value = false
  }
}

onMounted(() => loadUserSummary())
</script>

<style scoped>
.stat-card {
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15);
}
</style>
