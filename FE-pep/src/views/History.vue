<template>
  <div class="max-w-6xl mx-auto px-4 py-10">
    <h1 class="text-3xl font-bold text-indigo-700 text-center mb-8">Lịch sử dự đoán</h1>

    <!-- Loading -->
    <div v-if="loading" class="flex justify-center items-center h-48">
      <svg class="animate-spin h-10 w-10 text-indigo-600" xmlns="http://www.w3.org/2000/svg" fill="none"
        viewBox="0 0 24 24">
        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
        <path class="opacity-75" fill="currentColor"
          d="M4 12a8 8 0 018-8v4l3-3-3-3v4a8 8 0 100 16v-4l-3 3 3 3v-4a8 8 0 01-8-8z" />
      </svg>
    </div>

    <!-- Error -->
    <div v-if="error" class="text-red-600 text-center mb-4">{{ error }}</div>

    <!-- Table -->
    <div v-if="!loading && history.length > 0" class="overflow-auto rounded-xl border border-gray-200 shadow">
      <table class="min-w-full text-sm text-gray-800">
        <thead class="bg-indigo-100 text-indigo-800 text-left font-semibold text-sm uppercase tracking-wide">
          <tr>
            <th class="px-4 py-3">STT</th>
            <th class="px-4 py-3">Tên</th>
            <th class="px-4 py-3">Loại</th>
            <th class="px-4 py-3">Chuỗi</th>
            <th class="px-4 py-3">Kết quả</th>
            <th class="px-4 py-3">Thời gian</th>
            <th class="px-4 py-3 text-center">Hành động</th>
          </tr>
        </thead>
        <tbody class="divide-y bg-white">
          <tr v-for="(item, index) in history" :key="item._id" class="hover:bg-indigo-50 transition duration-150">
            <td class="px-4 py-2 font-bold text-center">{{ index + 1 }}</td>
            <td class="px-4 py-2 font-medium">{{ item.name }}</td>
            <td class="px-4 py-2 capitalize">{{ item.luu.type }}</td>
            <td class="px-4 py-2 font-mono break-words max-w-[300px]">{{ item.luu.content }}</td>
            <td class="px-4 py-2">
              <span :class="item.luu.result === 'AMP' ? 'text-green-600 font-semibold' : 'text-red-500 font-semibold'">
                {{ item.luu.result }}
              </span>
            </td>
            <td class="px-4 py-2 text-gray-500">{{ formatDate(item.time_change) }}</td>
            <td class="px-4 py-2 text-center">
              <button @click="confirmDelete(item._id)"
                class="text-red-500 hover:text-white hover:bg-red-500 p-1.5 rounded-full transition"
                title="Xoá">
                <TrashIcon class="w-5 h-5" />
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- No data -->
    <div v-if="!loading && history.length === 0" class="text-center text-gray-500 mt-10">
      Không có lịch sử nào.
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import Swal from 'sweetalert2'
import { TrashIcon } from '@heroicons/vue/24/solid'

const history = ref([])
const loading = ref(true)
const error = ref('')
const token = localStorage.getItem('access_token')

function formatDate(dateStr) {
  const date = new Date(dateStr)
  return date.toLocaleString('vi-VN')
}

async function fetchHistory() {
  try {
    const res = await fetch('http://localhost:8080/access/getLS', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
    })

    if (!res.ok) throw new Error('Phiên đăng nhập hết hạn hoặc lỗi mạng.')
    const json = await res.json()
    history.value = json.data
  } catch (err) {
    error.value = err.message
    Swal.fire('Lỗi', err.message, 'error')
  } finally {
    loading.value = false
  }
}

async function confirmDelete(id) {
  const result = await Swal.fire({
    title: 'Bạn có chắc?',
    text: 'Thao tác này sẽ xoá bản ghi khỏi hệ thống.',
    icon: 'warning',
    showCancelButton: true,
    confirmButtonText: 'Xoá',
    cancelButtonText: 'Huỷ'
  })

  if (result.isConfirmed) {
    await deleteHistory(id)
  }
}

async function deleteHistory(id) {
  try {
    const res = await fetch('http://localhost:8080/access/delete', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
      body: JSON.stringify({ id: id })
    })

    if (!res.ok) throw new Error('Xoá thất bại')
    history.value = history.value.filter(item => item._id !== id)

    Swal.fire('Đã xoá!', 'Lịch sử đã được xoá.', 'success')
  } catch (err) {
    Swal.fire('Lỗi', err.message || 'Không thể xoá.', 'error')
  }
}

onMounted(fetchHistory)
</script>
