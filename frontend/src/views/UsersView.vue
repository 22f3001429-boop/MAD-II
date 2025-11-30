<template>
  <div class="bg-light min-vh-100">
    <div class="bg-primary bg-opacity-10 py-3 border-bottom">
      <div class="container">
        <div class="d-flex justify-content-between align-items-center">
          <div>
            <h1 class="h4 fw-bold mb-2">Users Management</h1>
            <p class="text-muted mb-0">Monitor and manage all registered users</p>
          </div>
          <div class="d-flex gap-3">
            <div class="input-group" style="max-width: 300px;">
              <input 
                v-model="searchQuery" 
                type="text" 
                class="form-control" 
                placeholder="Search users..."
              >
              <button class="btn btn-outline-secondary" type="button">
                <i class="fas fa-search"></i>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="container py-4">
      <div v-if="error" class="alert alert-danger">{{ error }}</div>
      
      <div v-if="loading" class="text-center py-5">
        <div class="spinner-border text-primary mb-3"></div>
        <p class="text-muted">Loading users...</p>
      </div>
      
      <div v-else>
        <!-- Statistics Cards -->
        <div class="row g-4 mb-5">
          <div class="col-lg-3 col-md-6">
            <div class="card text-center stat-card">
              <div class="card-body">
                <div class="fs-1 mb-3">👥</div>
                <div class="h3 text-primary fw-bold">{{ totalUsers }}</div>
                <div class="text-muted">Total Users</div>
              </div>
            </div>
          </div>
          
          <div class="col-lg-3 col-md-6">
            <div class="card text-center stat-card">
              <div class="card-body">
                <div class="fs-1 mb-3 text-success"></div>
                <div class="h3 text-success fw-bold">{{ activeUsers }}</div>
                <div class="text-muted">Active Users</div>
              </div>
            </div>
          </div>
          
          <div class="col-lg-3 col-md-6">
            <div class="card text-center stat-card">
              <div class="card-body">
                <div class="fs-1 mb-3 text-warning"></div>
                <div class="h3 text-warning fw-bold">{{ newUsersThisMonth }}</div>
                <div class="text-muted">New This Month</div>
              </div>
            </div>
          </div>
          
          <div class="col-lg-3 col-md-6">
            <div class="card text-center stat-card">
              <div class="card-body">
                <div class="fs-1 mb-3 text-info"></div>
                <div class="h3 text-info fw-bold">₹{{ totalRevenue.toLocaleString() }}</div>
                <div class="text-muted">Total Revenue</div>
              </div>
            </div>
          </div>
        </div>

        <!-- Users Table -->
        <div class="card border-0 shadow-sm">
          <div class="card-header bg-light">
            <div class="d-flex justify-content-between align-items-center">
              <h5 class="fw-bold mb-0">Registered Users</h5>
              <div class="d-flex gap-2">
                <select v-model="statusFilter" class="form-select form-select-sm" style="width: auto;">
                  <option value="">All Status</option>
                  <option value="active">Active</option>
                  <option value="inactive">Inactive</option>
                </select>
              </div>
            </div>
          </div>
          
          <div class="card-body p-0">
            <div v-if="filteredUsers.length === 0" class="text-center py-5">
              <div class="fs-1 text-muted mb-3">👥</div>
              <h3 class="text-muted">No users found</h3>
              <p class="text-muted">No users match your search criteria</p>
            </div>
            
            <div v-else class="table-responsive">
              <table class="table table-hover mb-0">
                <thead class="table-light">
                  <tr>
                    <th class="border-0">User</th>
                    <th class="border-0">Email</th>
                    <th class="border-0">Role</th>
                    <th class="border-0">Status</th>
                    <th class="border-0">Joined</th>
                    <th class="border-0">Actions</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="user in filteredUsers" :key="user.id">
                    <td>
                      <div class="d-flex align-items-center gap-3">
                        <div class="bg-primary bg-opacity-10 rounded-circle d-flex align-items-center justify-content-center fw-bold text-primary" 
                             style="width: 40px; height: 40px;">
                          {{ user.username.charAt(0).toUpperCase() }}
                        </div>
                        <div>
                          <div class="fw-semibold">{{ user.username }}</div>
                          <small class="text-muted">ID: {{ user.id }}</small>
                        </div>
                      </div>
                    </td>
                    <td>
                      <div class="text-muted">{{ user.email }}</div>
                    </td>
                    <td>
                      <span class="badge" :class="user.role === 'admin' ? 'bg-danger' : 'bg-primary'">
                        {{ user.role }}
                      </span>
                    </td>
                    <td>
                      <span class="badge" :class="user.status === 'active' ? 'bg-success' : 'bg-secondary'">
                        {{ user.status }}
                      </span>
                    </td>
                    <td>
                      <div class="text-muted">{{ formatDate(user.created_at) }}</div>
                    </td>
                    <td>
                      <div class="d-flex gap-2">
                        <button class="btn btn-sm btn-outline-primary" @click="viewUserDetails(user)">
                          <i class="fas fa-eye"></i>
                        </button>
                        <button class="btn btn-sm btn-outline-warning" @click="editUser(user)">
                          <i class="fas fa-edit"></i>
                        </button>
                        <button class="btn btn-sm btn-outline-danger" @click="deleteUser(user)">
                          <i class="fas fa-trash"></i>
                        </button>
                      </div>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- User Details Modal -->
    <div v-if="showModal" class="modal fade show d-block" tabindex="-1">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">User Details</h5>
            <button type="button" class="btn-close" @click="closeModal"></button>
          </div>
          <div class="modal-body">
            <div class="row g-3">
              <div class="col-md-6">
                <label class="form-label fw-semibold">Username:</label>
                <div class="form-control-plaintext">{{ selectedUser?.username }}</div>
              </div>
              <div class="col-md-6">
                <label class="form-label fw-semibold">Email:</label>
                <div class="form-control-plaintext">{{ selectedUser?.email }}</div>
              </div>
              <div class="col-md-6">
                <label class="form-label fw-semibold">Role:</label>
                <div class="form-control-plaintext">
                  <span class="badge" :class="selectedUser?.role === 'admin' ? 'bg-danger' : 'bg-primary'">
                    {{ selectedUser?.role }}
                  </span>
                </div>
              </div>
              <div class="col-md-6">
                <label class="form-label fw-semibold">Status:</label>
                <div class="form-control-plaintext">
                  <span class="badge" :class="selectedUser?.status === 'active' ? 'bg-success' : 'bg-secondary'">
                    {{ selectedUser?.status }}
                  </span>
                </div>
              </div>
              <div class="col-md-6">
                <label class="form-label fw-semibold">Joined:</label>
                <div class="form-control-plaintext">{{ formatDate(selectedUser?.created_at) }}</div>
              </div>
              <div class="col-md-6">
                <label class="form-label fw-semibold">Last Login:</label>
                <div class="form-control-plaintext">{{ formatDate(selectedUser?.last_login) || 'Never' }}</div>
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="closeModal">Close</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'

const loading = ref(false)
const error = ref('')
const users = ref([])
const searchQuery = ref('')
const statusFilter = ref('')
const showModal = ref(false)
const selectedUser = ref(null)

function createAuthConfig() {
  const token = localStorage.getItem('token')
  return {
    headers: { Authorization: `Bearer ${token}` }
  }
}

async function loadUsers() {
  loading.value = true
  error.value = null

  try {
    const token = localStorage.getItem("token")

    const res = await axios.get("http://localhost:5000/api/admin/users", {
      headers: {
        Authorization: `Bearer ${token}`
      }
    })

    users.value = res.data

  } catch (e) {
    error.value = e?.response?.data?.message || 'Failed to load users'
  } finally {
    loading.value = false
  }
}

function viewUserDetails(user) {
  selectedUser.value = user
  showModal.value = true
}

function editUser(user) {
  console.log('Edit user:', user)
}

function deleteUser(user) {
  console.log('Delete user:', user)
}

function closeModal() {
  showModal.value = false
  selectedUser.value = null
}

function formatDate(dateString) {
  if (!dateString) return 'N/A'
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const totalUsers = computed(() => users.value.length)
const activeUsers = computed(() => users.value.filter(u => u.status === 'active').length)
const newUsersThisMonth = computed(() => {
  const thisMonth = new Date().getMonth()
  return users.value.filter(u => new Date(u.created_at).getMonth() === thisMonth).length
})
const totalRevenue = ref(125000)

const filteredUsers = computed(() => {
  let filtered = users.value

  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    filtered = filtered.filter(user => 
      user.username.toLowerCase().includes(query) ||
      user.email.toLowerCase().includes(query)
    )
  }

  if (statusFilter.value) {
    filtered = filtered.filter(user => user.status === statusFilter.value)
  }

  return filtered
})

onMounted(() => {
  loadUsers()
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

/* Table styling */
.table th {
  font-weight: 600;
  color: #495057;
}

.table td {
  vertical-align: middle;
}

/* Modal backdrop */
.modal.show {
  background-color: rgba(0, 0, 0, 0.5);
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .table-responsive {
    font-size: 0.875rem;
  }
}
</style>