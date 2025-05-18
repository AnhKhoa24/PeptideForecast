<template>
  <div class="w-full px-4 max-w-6xl mx-auto py-10 space-y-10">
    <!-- Title -->
    <div class="text-center">
      <h1 class="text-4xl font-bold text-indigo-700">Peptide 3D Structure & Activity Prediction</h1>
      <p class="text-gray-600 mt-3 text-base">
        Enter a peptide sequence (10–50 amino acids) to visualize its 3D structure and predict antimicrobial activity.
      </p>
    </div>

    <!-- Input Box -->
    <div class="relative">
      <textarea v-model="sequence"
        class="w-full min-h-[60px] rounded-xl border border-gray-300 focus:ring-2 focus:ring-indigo-400 px-4 py-3 text-sm font-mono resize-none shadow-md"
        maxlength="50"
        placeholder="E.g. ACDEFGHIKLMNPQRSTVWY..."
      ></textarea>

      <!-- Tools -->
      <div class="absolute top-2 right-3 flex space-x-2">
        <button @click="copyText" class="p-1.5 text-gray-500 hover:text-indigo-600 rounded hover:bg-gray-100" title="Copy">
          <ClipboardDocumentIcon class="w-5 h-5" />
        </button>
        <button @click="pasteText" class="p-1.5 text-gray-500 hover:text-indigo-600 rounded hover:bg-gray-100" title="Paste">
          <DocumentArrowDownIcon class="w-5 h-5" />
        </button>
      </div>
    </div>

    <!-- Predict Button -->
    <div class="text-center">
      <button @click="submitSequence"
        class="bg-indigo-600 hover:bg-indigo-700 text-white font-semibold px-6 py-2 rounded-xl shadow">
        Predict & Generate 3D
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
    <div id="viewer" class="relative w-full h-[250px] border rounded shadow overflow-hidden"></div>
    <!-- IG Visualization -->
    <div v-if="highlightImg" class="text-center">
      <h2 class="text-lg font-semibold text-gray-700 mb-2">Model Explanation (XAI)</h2>
      <img :src="highlightImg" alt="IG XAI Visualization" class="mx-auto rounded shadow border max-w-full" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ClipboardDocumentIcon, DocumentArrowDownIcon } from '@heroicons/vue/24/outline'
import { usePeptidePrediction } from '@/composables/usePeptidePrediction'
import { onMounted } from 'vue'

const {
  sequence,
  prediction,
  highlightImg,
  copyText,
  pasteText,
  submitSequence,
  init3Dmol
} = usePeptidePrediction()

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
</script>

<style scoped>
textarea::placeholder {
  color: #94a3b8;
}
</style>
