// src/composables/usePeptidePrediction.ts
import { ref } from 'vue'
import Swal from 'sweetalert2'
// @ts-ignore: 3Dmol comes from global script
declare const $3Dmol: any
const showContent = ref(false)
const isLoading = ref(false)
const pdbReady = ref(false)

export function usePeptidePrediction() {
  const sequence = ref('')
  const prediction = ref<string | null>(null)
  const highlightImg = ref<string | null>(null)
  let viewer: any = null

  function copyText() {
    navigator.clipboard.writeText(sequence.value)
  }

  async function pasteText() {
    const text = await navigator.clipboard.readText()
    sequence.value = text
  }

  async function submitSequence() {

    if (sequence.value.length < 10 || sequence.value.length > 50) {
      await Swal.fire({
        icon: 'warning',
        title: 'Chuỗi không hợp lệ',
        text: 'Độ dài peptide phải từ 10 đến 50 amino acids.',
        confirmButtonText: 'OK'
      })
      return
    }
    isLoading.value = true
    try {
      // Call backend to get PDB + prediction
      const [pdbRes, predRes] = await Promise.all([
        fetch('http://localhost:8080/ai/generate_pdb', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ sequence: sequence.value })
        }),
        fetch('http://localhost:8080/ai/dudoan', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ sequence: sequence.value })
        })
      ])

      const pdbData = await pdbRes.json()
      const predData = await predRes.json()

      if (pdbData.pdb) {
        pdbReady.value = true
        render3D(pdbData.pdb)
      }

      if (predData.label !== undefined) {
        prediction.value = predData.label === 1 ? 'AMP' : 'nAMP'
        highlightImg.value = predData.highlight_img || null
      }
      showContent.value = true
    } catch (error) {
      alert('Failed to predict or generate structure.')
      console.error(error)
    }
    finally {
      isLoading.value = false
    }
  }

  function render3D(pdbData: string) {
    if (!viewer && typeof $3Dmol !== 'undefined') {
      const el = document.getElementById('viewer')
      if (el) viewer = $3Dmol.createViewer(el, { backgroundColor: 'white' })
    }
    if (!viewer) return
    viewer.clear()
    viewer.addModel(pdbData, 'pdb')
    // viewer.setStyle({}, { cartoon: { color: 'spectrum' } })
    viewer.setStyle({}, {
      cartoon: { color: 'spectrum', arrows: true },   // có mũi tên biểu thị hướng
      stick: { radius: 0.2 },                         // hiện liên kết
      sphere: { scale: 0.3 },                         // hiện nguyên tử
    })
    viewer.addSurface($3Dmol.SurfaceType.SES, {
      opacity: 0.3,
      color: 'white'
    })

    viewer.zoomTo()
    viewer.zoom(3)
    viewer.render()
  }

  function init3Dmol() {
    const el = document.getElementById('viewer')
    if (el && typeof $3Dmol !== 'undefined') {
      viewer = $3Dmol.createViewer(el, { backgroundColor: 'white' })
    }
  }

  return {
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
  }
}
