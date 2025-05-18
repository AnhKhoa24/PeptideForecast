// src/composables/useForecast.ts
import { ref } from 'vue'

export function useForecast() {
  const showText = ref(false)
  const revealText = () => {
    showText.value = true
  }

  return {
    showText,
    revealText
  }
}
