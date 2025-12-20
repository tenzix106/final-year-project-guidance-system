<template>
  <div class="space-y-6">
    <div class="flex items-center justify-between">
      <h2 class="text-2xl font-bold text-gray-900">User Management</h2>
      <div class="flex items-center space-x-4">
        <select v-model="roleFilter" class="input-field">
          <option value="">All Roles</option>
          <option value="student">Students</option>
          <option value="admin">Admins</option>
        </select>
        <input
          v-model="searchQuery"
          type="text"
          placeholder="Search users..."
          class="input-field"
        />
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="flex items-center justify-center py-12">
      <Loader2 class="w-8 h-8 animate-spin text-primary-600" />
    </div>

    <!-- Users Table -->
    <div v-else class="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
      <table class="min-w-full divide-y divide-gray-200">
        <thead class="bg-gray-50">
          <tr>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">User</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">University</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Program</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Role</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Auth Provider</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Joined</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
          </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
          <tr v-for="user in users" :key="user.id" class="hover:bg-gray-50">
            <td class="px-6 py-4 whitespace-nowrap">
              <div>
                <div class="text-sm font-medium text-gray-900">{{ user.full_name || 'N/A' }}</div>
                <div class="text-sm text-gray-500">{{ user.email }}</div>
              </div>
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
              {{ user.university || 'N/A' }}
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
              {{ user.program || 'N/A' }}
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              <span :class="[
                'px-2 py-1 text-xs font-medium rounded-full',
                user.role === 'admin' ? 'bg-purple-100 text-purple-800' : 'bg-blue-100 text-blue-800'
              ]">
                {{ user.role }}
              </span>
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
              {{ user.auth_provider }}
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
              {{ new Date(user.created_at).toLocaleDateString() }}
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm">
              <button
                @click="toggleRole(user)"
                class="text-primary-600 hover:text-primary-900 font-medium"
              >
                {{ user.role === 'admin' ? 'Make Student' : 'Make Admin' }}
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Pagination -->
    <div v-if="pagination.pages > 1" class="flex items-center justify-between bg-white px-6 py-4 rounded-xl border border-gray-200">
      <div class="text-sm text-gray-700">
        Showing <span class="font-medium">{{ (pagination.page - 1) * pagination.per_page + 1 }}</span>
        to <span class="font-medium">{{ Math.min(pagination.page * pagination.per_page, pagination.total) }}</span>
        of <span class="font-medium">{{ pagination.total }}</span> results
      </div>
      <div class="flex space-x-2">
        <button
          @click="loadPage(pagination.page - 1)"
          :disabled="!pagination.has_prev"
          class="px-4 py-2 border border-gray-300 rounded-lg text-sm font-medium text-gray-700 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          Previous
        </button>
        <button
          @click="loadPage(pagination.page + 1)"
          :disabled="!pagination.has_next"
          class="px-4 py-2 border border-gray-300 rounded-lg text-sm font-medium text-gray-700 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          Next
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { Loader2 } from 'lucide-vue-next'
import axios from 'axios'

const loading = ref(true)
const users = ref([])
const searchQuery = ref('')
const roleFilter = ref('')
const pagination = ref({
  page: 1,
  per_page: 20,
  total: 0,
  pages: 0,
  has_next: false,
  has_prev: false
})

const fetchUsers = async (page = 1) => {
  loading.value = true
  try {
    const token = localStorage.getItem('auth_token')
    const response = await axios.get(buildApiUrl(API_ENDPOINTS.ADMIN.USERS), {
      headers: { Authorization: `Bearer ${token}` },
      params: {
        page,
        per_page: 20,
        search: searchQuery.value,
        role: roleFilter.value
      }
    })
    users.value = response.data.users
    pagination.value = response.data.pagination
  } catch (error) {
    console.error('Error fetching users:', error)
  } finally {
    loading.value = false
  }
}

const loadPage = (page) => {
  fetchUsers(page)
}

const toggleRole = async (user) => {
  if (!confirm(`Are you sure you want to change ${user.email}'s role to ${user.role === 'admin' ? 'student' : 'admin'}?`)) {
    return
  }
  
  try {
    const token = localStorage.getItem('auth_token')
    const newRole = user.role === 'admin' ? 'student' : 'admin'
    await axios.patch(
      buildApiUrl(API_ENDPOINTS.ADMIN.USER_ROLE(user.id)),
      { role: newRole },
      { headers: { Authorization: `Bearer ${token}` } }
    )
    await fetchUsers(pagination.value.page)
  } catch (error) {
    console.error('Error updating user role:', error)
    alert('Failed to update user role')
  }
}

watch([searchQuery, roleFilter], () => {
  fetchUsers(1)
}, { debounce: 300 })

onMounted(() => {
  fetchUsers()
})
</script>
