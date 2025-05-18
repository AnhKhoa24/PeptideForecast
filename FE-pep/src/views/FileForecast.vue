<template>
  <section class="min-h-screen pt-24 pb-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-5xl mx-auto p-6 bg-white rounded-2xl shadow-xl">
      <h2 class="text-2xl font-bold mb-6 text-blue-700 flex items-center">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 mr-2 text-blue-700" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 4H7a2 2 0 01-2-2V6a2 2 0 012-2h7l5 5v11a2 2 0 01-2 2z" />
        </svg>
        Dự đoán peptide từ file FASTA
      </h2>

      <form @submit.prevent="submitFile" class="flex flex-col gap-4">
        <label class="block">
          <span class="text-gray-700 font-medium">Chọn file FASTA</span>
          <input
            type="file"
            accept=".fasta,.fa,.fna"
            @change="onFileChange"
            class="mt-1 block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
          />
        </label>

        <div class="flex gap-4 flex-wrap">
          <button
            type="submit"
            :disabled="!file"
            class="bg-blue-600 text-white px-6 py-2 rounded-xl hover:bg-blue-700 disabled:opacity-50 flex items-center gap-2"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
              <path d="M3 3a1 1 0 011-1h4a1 1 0 011 1v5H3V3zM2 9a1 1 0 011-1h14a1 1 0 011 1v8a2 2 0 01-2 2H4a2 2 0 01-2-2V9z" />
            </svg>
            Dự đoán và xem PDF
          </button>

          <a
            v-if="pdfUrl"
            :href="pdfUrl"
            download="predictions.pdf"
            class="bg-green-600 text-white px-6 py-2 rounded-xl hover:bg-green-700 flex items-center gap-2"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
              <path d="M9 2a1 1 0 00-1 1v9H5a1 1 0 00-.8 1.6l5 6a1 1 0 001.6 0l5-6A1 1 0 0015 12h-3V3a1 1 0 00-1-1H9z" />
            </svg>
            Tải PDF
          </a>

          <a
            v-if="excelUrl"
            :href="excelUrl"
            download="predictions.xlsx"
            class="bg-yellow-500 text-white px-6 py-2 rounded-xl hover:bg-yellow-600 flex items-center gap-2"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
              <path d="M3 3a1 1 0 011-1h12a1 1 0 011 1v14a1 1 0 01-1 1H4a1 1 0 01-1-1V3zm4.293 7.293a1 1 0 011.414 0L10 11.586l1.293-1.293a1 1 0 011.414 1.414L11.414 13l1.293 1.293a1 1 0 01-1.414 1.414L10 14.414l-1.293 1.293a1 1 0 01-1.414-1.414L8.586 13 7.293 11.707a1 1 0 010-1.414z" />
            </svg>
            Tải Excel
          </a>
        </div>
      </form>

      <div v-if="loading" class="mt-6 text-blue-600 font-medium">Đang xử lý file... ⏳</div>
      <div v-if="error" class="mt-4 text-red-500">Lỗi: {{ error }}</div>

      <iframe
        v-if="pdfUrl"
        :src="pdfUrl"
        class="mt-8 w-full h-[700px] border rounded-xl shadow-md"
      />
    </div>
  </section>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useFileForecast } from '@/composables/useFileForecast'

const file = ref<File | null>(null)
const {
  uploadFastaFilePDF,
  uploadFastaFileExcel,
  loading,
  error,
  pdfUrl,
  excelUrl
} = useFileForecast()

const onFileChange = (e: any) => {
  const target = e.target
  file.value = target.files?.[0] || null
}

const submitFile = async () => {
  if (file.value) {
    await uploadFastaFilePDF(file.value)
    await uploadFastaFileExcel(file.value)
  }
}
</script>

<style scoped>
</style>
