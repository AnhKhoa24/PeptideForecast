<template>
  <div class="relative overflow-hidden bg-white">
    <!-- Section Hero -->
    <div class="mx-auto max-w-7xl px-6 py-24 lg:flex lg:items-center lg:justify-between lg:px-8">
      <div class="max-w-2xl">
        <h1 class="text-4xl font-bold tracking-tight text-gray-900 sm:text-5xl">
          Dự đoán Peptide kháng khuẩn
        </h1>
        <p class="mt-6 text-lg leading-8 text-gray-600">
          Ứng dụng AI để phân loại peptide có khả năng kháng khuẩn, hỗ trợ nghiên cứu y sinh và phát triển thuốc.
        </p>
        <div class="mt-10 flex items-center gap-x-6">
          <RouterLink to="/predict"
            class="rounded-md bg-blue-600 px-4 py-2 text-sm font-semibold text-white shadow-sm hover:bg-blue-700">
            🔬 Bắt đầu dự đoán
          </RouterLink>
          <a href="#about" class="text-sm font-semibold text-gray-900 hover:text-blue-700">
            Tìm hiểu thêm →
          </a>
        </div>
      </div>

      <!-- Hình ảnh peptide -->
      <div class="mt-10 lg:mt-0 lg:ml-12">
        <img
          :src="peptideImage"
          alt="peptide"
          class="w-full max-w-md rounded-lg shadow-xl ring-1 ring-gray-300"
        />
      </div>
    </div>

    <!-- Section giới thiệu -->
    <div id="about" class="bg-gray-50 py-16 px-6 lg:px-8">
      <div class="mx-auto max-w-4xl text-center">
        <h2 class="text-base font-semibold leading-7 text-blue-600">Về hệ thống</h2>
        <p class="mt-2 text-3xl font-bold tracking-tight text-gray-900 sm:text-4xl">
          Tại sao nên sử dụng hệ thống này?
        </p>
        <p class="mt-6 text-lg leading-8 text-gray-600">
          Hệ thống dự đoán peptide kháng khuẩn bằng AI được huấn luyện trên dữ liệu thực, kết hợp LSTM, transformer và XAI
          giúp giải thích mô hình rõ ràng – là công cụ hỗ trợ hiệu quả cho nhà nghiên cứu sinh học phân tử.
        </p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import peptideImage from '@/assets/images/peptidebg.jpg'
import { RouterLink } from 'vue-router'
</script>
