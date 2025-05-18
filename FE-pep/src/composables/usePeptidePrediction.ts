// src/composables/usePeptidePrediction.ts
import { ref } from 'vue'

// @ts-ignore: 3Dmol comes from global script
declare const $3Dmol: any

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
      alert('Sequence must be between 10 and 50 amino acids.')
      return
    }

    try {
      // Call backend to get PDB + prediction
      const [pdbRes, predRes] = await Promise.all([
        fetch('http://localhost:8000/ai/generate_pdb', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ sequence: sequence.value })
        }),
        fetch('http://localhost:8000/ai/dudoan', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ sequence: sequence.value })
        })
      ])

      const pdbData = await pdbRes.json()
      const predData = await predRes.json()

      if (pdbData.pdb) render3D(pdbData.pdb)
      if (predData.label !== undefined) {
        prediction.value = predData.label === 1 ? 'AMP' : 'nAMP'
        highlightImg.value = predData.highlight_img || null
      }
    } catch (error) {
      alert('Failed to predict or generate structure.')
      console.error(error)
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
    viewer.setStyle({}, { cartoon: { color: 'spectrum' } })
    viewer.zoomTo()
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
    init3Dmol
  }
}
