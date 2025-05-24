<template>
  <div class="w-full px-4 max-w-6xl mx-auto py-10 space-y-10">
    <!-- Title -->
    <div class="text-center">
      <h1 class="text-4xl font-bold text-indigo-700">Peptide Activity Prediction</h1>
      <p class="text-gray-600 mt-3 text-base">
        Enter a peptide sequence (10–50 amino acids) to visualize its 3D structure and predict antimicrobial activity.
      </p>
    </div>

    <div class="relative">
      <textarea v-model="sequence"
        class="py-[12.5px] pl-[40px] w-full h-[54px] rounded-full border border-gray-300 bg-white focus:outline-none focus:ring-2 focus:ring-blue-500 px-4 text-lg font-semibold tracking-widest font-mono shadow-sm resize-none transition-all duration-200"
        maxlength="50" placeholder="E.g. ACDEFGHIKLMNPQRSTVWY..."></textarea>

      <!-- Tools -->
      <div class="absolute top-1.5 right-3 flex space-x-2 py-[5px] pr-[20px]">
        <button @click="copyText" class="p-1.5 text-gray-500 hover:text-indigo-600 rounded hover:bg-gray-100"
          title="Copy">
          <ClipboardDocumentIcon class="w-5 h-5" />
        </button>
        <button @click="pasteText" class="p-1.5 text-gray-500 hover:text-indigo-600 rounded hover:bg-gray-100"
          title="Paste">
          <DocumentArrowDownIcon class="w-5 h-5" />
        </button>
      </div>
    </div>


    <!-- Predict Button -->
    <div class="flex justify-center">
      <button @click="submitSequence" :disabled="isLoading"
        class="relative bg-indigo-600 hover:bg-indigo-700 text-white font-semibold px-6 py-2 rounded-xl shadow disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2">
        <svg v-if="isLoading" class="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none"
          viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
          <path class="opacity-75" fill="currentColor"
            d="M4 12a8 8 0 018-8v4l3-3-3-3v4a8 8 0 100 16v-4l-3 3 3 3v-4a8 8 0 01-8-8z" />
        </svg>

        <!-- Icon AI "magic" -->
        <svg v-if="!isLoading" class="h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none"
          viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
        </svg>

        <span>
          {{ isLoading ? 'Processing...' : 'Tiến hành dự đoán' }}
        </span>
      </button>
    </div>

    <!-- Result Section -->
    <div v-if="prediction" class="text-center">
      <p class="text-xl font-medium">
        Result:
        <span :class="prediction === 'AMP' ? 'text-green-600' : 'text-red-500'">{{ prediction }}</span>
      </p>
    </div>

    <!-- 3Dmol.js Viewer -->
    <!-- <div id="viewer" class="mx-auto w-full max-w-xl h-[250px] border rounded shadow"></div> -->
    <div v-show="pdbReady" id="viewer" class="relative w-full h-[250px] border rounded shadow overflow-hidden"></div>

    <!-- IG Visualization -->
    <div v-if="highlightImg" class="text-center">
      <h2 class="text-lg font-semibold text-gray-700 mb-2">Model Explanation (XAI)</h2>
      <img :src="highlightImg" alt="IG XAI Visualization" class="mx-auto rounded shadow border max-w-full" />
    </div>
  </div>

  <div class="pb-4">
    <transition name="fade">
      <div v-if="showContent" class="bg-gray-200 p-2 rounded mt-4 flex justify-center items-center gap-4">
        <span class="text-gray-800 text-base">
          Lưu lại chuỗi nghiên cứu
        </span>

        <button @click="openModal"
          class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-xl flex items-center gap-2">
          <ArrowDownTrayIcon class="w-5 h-5" />
          Lưu lại
        </button>
      </div>

    </transition>
  </div>

  <transition name="fade-zoom">
    <div v-if="isModalOpen" class="fixed inset-0 z-50 flex items-center justify-center backdrop-blur-sm bg-black/30">
      <div class="bg-white rounded-xl p-6 w-96 shadow-lg transform transition-all">
        <h3 class="text-lg font-semibold mb-4 text-gray-800">Nhập tên cần lưu</h3>
        <input v-model="saveName" type="text" placeholder="Tên lưu"
          class="w-full border border-gray-300 rounded px-3 py-2 mb-4 focus:ring-2 focus:ring-blue-400 outline-none" />
        <div class="flex justify-end gap-2">
          <button @click="closeModal" class="px-4 py-2 bg-gray-300 hover:bg-gray-400 rounded">Hủy</button>
          <button @click="save" class="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded">Xác nhận</button>
        </div>
      </div>
    </div>
  </transition>
</template>

<script setup lang="ts">
import { ClipboardDocumentIcon, DocumentArrowDownIcon, ArrowDownTrayIcon } from '@heroicons/vue/24/outline'
import { usePeptidePrediction } from '@/composables/usePeptidePrediction'
import { onMounted, ref, watch } from 'vue'
import Swal from 'sweetalert2'


const {
  sequence,
  prediction,
  highlightImg,
  copyText,
  pasteText,
  submitSequence,
  init3Dmol,
  showContent,
  isLoading,
  pdbReady
} = usePeptidePrediction()

watch(sequence, (val) => {
  // Bỏ dấu và chuyển in hoa
  const noDiacritics = val.normalize("NFD").replace(/[\u0300-\u036f]/g, "")
  sequence.value = noDiacritics.toUpperCase()
})

onMounted(() => {
  const scriptId = '3dmol-script'
  if (!document.getElementById(scriptId)) {
    const script = document.createElement('script')
    script.id = scriptId
    script.src = 'https://3Dmol.csb.pitt.edu/build/3Dmol-min.js'
    script.onload = () => init3Dmol()
    document.body.appendChild(script)
  } else {
    init3Dmol()
  }
})

///MODAL CUSTOM
const isModalOpen = ref(false)
const saveName = ref('')

function openModal() {
  const token = localStorage.getItem('access_token')

  if (!token) {
    Swal.fire({
      icon: 'info',
      title: 'Yêu cầu đăng nhập',
      text: 'Vui lòng đăng nhập để sử dụng chức năng này.',
      confirmButtonText: 'Đăng nhập'
    })
    return
  }
  isModalOpen.value = true
}
function closeModal() {
  isModalOpen.value = false
  saveName.value = ''
}
async function save() {
  if (!saveName.value.trim()) {
    Swal.fire({
      icon: 'warning',
      title: 'Thiếu thông tin',
      text: 'Vui lòng nhập tên để lưu!',
    })
    return
  }

  const token = localStorage.getItem('access_token')
  if (!token) {
    Swal.fire({
      icon: 'error',
      title: 'Lỗi xác thực',
      text: 'Phiên đăng nhập không hợp lệ. Vui lòng đăng nhập lại.',
    })
    return
  }

  try {
    const res = await fetch('http://localhost:8080/access/saveLS', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
      body: JSON.stringify({
        name: saveName.value,
        type: 'single',
        sequence: sequence.value, 
        result: prediction.value// lấy từ v-model chính
      })
    })

    if (!res.ok) throw new Error('Lưu thất bại')

    Swal.fire({
      icon: 'success',
      title: 'Đã lưu thành công!',
      text: `Tên: ${saveName.value}`,
      timer: 1500,
      showConfirmButton: false
    })

    closeModal()
  } catch (err) {
    console.error(err)
    Swal.fire({
      icon: 'error',
      title: 'Lỗi',
      text: 'Đã xảy ra lỗi khi lưu. Vui lòng thử lại.',
    })
  }
}

</script>

<style scoped>
textarea::placeholder {
  color: #94a3b8;
}
</style>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>

<style scoped>
/* Hiệu ứng vào/ra mượt mà */
.fade-zoom-enter-active,
.fade-zoom-leave-active {
  transition: all 0.3s ease;
}

.fade-zoom-enter-from,
.fade-zoom-leave-to {
  opacity: 0;
  transform: scale(0.95) translateY(10px);
}
</style>