import { ref } from 'vue'

export function useFileForecast() {
  const loading = ref(false)
  const error = ref('')
  const pdfUrl = ref('')
  const excelUrl = ref('')

  const uploadFastaFilePDF = async (file: File) => {
    loading.value = true
    error.value = ''
    pdfUrl.value = ''

    const formData = new FormData()
    formData.append('file', file)

    try {
      const res = await fetch('http://localhost:8080/ai/dudoan_fasta_pdf', {
        method: 'POST',
        body: formData,
      })

      if (!res.ok) throw new Error(`Lỗi server: ${res.status}`)

      const blob = await res.blob()
      pdfUrl.value = URL.createObjectURL(blob)
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Lỗi không xác định'
    } finally {
      loading.value = false
    }
  }

  const uploadFastaFileExcel = async (file: File) => {
    loading.value = true
    error.value = ''
    excelUrl.value = ''

    const formData = new FormData()
    formData.append('file', file)

    try {
      const res = await fetch('http://localhost:8080/ai/dudoan_fasta', {
        method: 'POST',
        body: formData,
      })

      if (!res.ok) throw new Error(`Lỗi server: ${res.status}`)

      const blob = await res.blob()
      excelUrl.value = URL.createObjectURL(blob)
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Lỗi không xác định'
    } finally {
      loading.value = false
    }
  }

  return {
    uploadFastaFilePDF,
    uploadFastaFileExcel,
    loading,
    error,
    pdfUrl,
    excelUrl,
  }
}
