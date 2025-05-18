<template>
 <!-- <header class="fixed top-0 left-0 right-0 z-[99] bg-gray-200 shadow-md border-b border-gray-200"> -->
<header :class="[
  'fixed top-0 left-0 right-0 z-[99] border-b border-gray-200 shadow-md transition-all duration-300',
  isScrolled ? 'bg-gray-300' : 'bg-white'
]">

    <nav class="mx-auto flex max-w-7xl items-center justify-between p-4 lg:px-8" aria-label="Global">
      <div class="flex lg:flex-1 items-center">
        <!-- Logo desktop -->
        <RouterLink to="/" class="-m-1.5 p-1.5 hidden lg:block">
          <img class="h-8 w-auto" :src="peptideImage" alt="logo-full" />
        </RouterLink>

        <!-- Logo mobile -->
        <RouterLink to="/" class="-m-1.5 p-1.5 block lg:hidden">
          <img class="h-8 w-auto" :src="miniLogo" alt="logo-mini" />
        </RouterLink>
      </div>
      <div class="flex lg:hidden">
        <button type="button" class="-m-2.5 inline-flex items-center justify-center rounded-md p-2.5 text-gray-700"
          @click="mobileMenuOpen = true">
          <span class="sr-only">Open main menu</span>
          <Bars3Icon class="size-6" aria-hidden="true" />
        </button>
      </div>
      <PopoverGroup class="hidden lg:flex lg:gap-x-12">
        <RouterLink to="/" class="hover:text-blue-700 text-slate-900 text-[15px] font-medium">Home</RouterLink>
        <Popover class="relative">
          <PopoverButton class="flex items-center gap-x-1 text-[15px] font-medium hover:text-blue-700 text-slate-900">
            Product
            <ChevronDownIcon class="size-5 flex-none text-gray-400" aria-hidden="true" />
          </PopoverButton>
          <transition enter-active-class="transition ease-out duration-200" enter-from-class="opacity-0 translate-y-1"
            enter-to-class="opacity-100 translate-y-0" leave-active-class="transition ease-in duration-150"
            leave-from-class="opacity-100 translate-y-0" leave-to-class="opacity-0 translate-y-1">
            <PopoverPanel
              class="absolute top-full -left-8 z-10 mt-3 w-screen max-w-md overflow-hidden rounded-3xl bg-white shadow-lg ring-1 ring-gray-900/5">
              <div class="p-4">
                <div v-for="item in products" :key="item.name"
                  class="group relative flex items-center gap-x-6 rounded-lg p-4 text-sm/6 hover:bg-gray-50">
                  <div
                    class="flex size-11 flex-none items-center justify-center rounded-lg bg-gray-50 group-hover:bg-white">
                    <component :is="item.icon" class="size-6 text-gray-600 group-hover:text-indigo-600"
                      aria-hidden="true" />
                  </div>
                  <div class="flex-auto">
                    <RouterLink :to="item.href" class="block font-semibold text-gray-900">
                      {{ item.name }}
                      <span class="absolute inset-0" />
                    </RouterLink>
                    <p class="mt-1 text-gray-600">{{ item.description }}</p>
                  </div>
                </div>
              </div>
              <div class="grid grid-cols-2 divide-x divide-gray-900/5 bg-gray-50">
                <a v-for="item in callsToAction" :key="item.name" :href="item.href"
                  class="flex items-center justify-center gap-x-2.5 p-3 text-sm/6 font-semibold text-gray-900 hover:bg-gray-100">
                  <component :is="item.icon" class="size-5 flex-none text-gray-400" aria-hidden="true" />
                  {{ item.name }}
                </a>
              </div>
            </PopoverPanel>
          </transition>
        </Popover>
        <RouterLink to="/history" class="text-[15px] font-medium hover:text-blue-700 text-slate-900">Lịch sử
        </RouterLink>
      </PopoverGroup>

      <div class="hidden lg:flex lg:flex-1 lg:justify-end space-x-4">
        <!-- Nút login / Avatar -->
        <template v-if="!user">
          <button @click="loginWithGoogle"
            class="px-4 py-2 text-sm rounded-full font-medium cursor-pointer tracking-wide text-slate-900 border border-gray-400 bg-transparent hover:bg-gray-50 transition-all">
            Login
          </button>
        </template>
        <template v-if="user">
          <div class="relative" ref="dropdownRef">
            <button @click="toggleMenu" class="focus:outline-none">
              <img :src="user.picture" class="w-9 h-9 rounded-full border-2 border-blue-600 shadow" :alt="user.name"
                referrerpolicy="no-referrer" />
            </button>

            <transition name="fade">
              <div v-if="showMenu"
                class="absolute right-0 mt-2 w-72 bg-white rounded-xl shadow-2xl border border-gray-200 z-50">
                <div class="p-4 border-b text-center">
                  <img :src="user.picture" class="w-16 h-16 rounded-full border mx-auto" />
                  <div class="mt-2 font-semibold text-gray-900 text-sm">{{ user.name }}</div>
                  <div class="text-xs text-gray-500">{{ user.email }}</div>
                </div>
                <button @click="logout"
                  class="w-full flex items-center justify-center gap-2 px-4 py-3 text-red-600 hover:bg-red-50 font-semibold text-sm">
                  <ArrowRightOnRectangleIcon class="w-5 h-5" />
                  Đăng xuất
                </button>

              </div>
            </transition>
          </div>
        </template>
        <button id="toggleOpen" class="lg:hidden cursor-pointer">
          <svg class="w-7 h-7" fill="#000" viewBox="0 0 20 20">
            <path fill-rule="evenodd"
              d="M3 5a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zM3 10a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zM3 15a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1z"
              clip-rule="evenodd"></path>
          </svg>
        </button>
      </div>
    </nav>
    <Dialog class="lg:hidden" @close="mobileMenuOpen = false" :open="mobileMenuOpen">
      <div class="fixed inset-0 z-10" />
      <DialogPanel
        class="fixed inset-y-0 right-0 z-10 w-full overflow-y-auto bg-white px-6 py-6 sm:max-w-sm sm:ring-1 sm:ring-gray-900/10">
        <div class="flex items-center justify-between">
          <a href="#" class="-m-1.5 p-1.5">
            <span class="sr-only">Your Company</span>
            <img class="h-8 w-auto" :src="miniLogo" alt="" />
          </a>
          <button type="button" class="-m-2.5 rounded-md p-2.5 text-gray-700" @click="mobileMenuOpen = false">
            <span class="sr-only">Close menu</span>
            <XMarkIcon class="size-6" aria-hidden="true" />
          </button>
        </div>
        <div class="mt-6 flow-root">
          <div class="-my-6 divide-y divide-gray-500/10">
            <div class="space-y-2 py-6">
              <Disclosure as="div" class="-mx-3" v-slot="{ open }">
                <DisclosureButton
                  class="flex w-full items-center justify-between rounded-lg py-2 pr-3.5 pl-3 text-base/7 font-semibold text-gray-900 hover:bg-gray-50">
                  Product
                  <ChevronDownIcon :class="[open ? 'rotate-180' : '', 'size-5 flex-none']" aria-hidden="true" />
                </DisclosureButton>
                <DisclosurePanel class="mt-2 space-y-2">
                  <DisclosureButton v-for="item in [...products, ...callsToAction]" :key="item.name" as="a"
                    :href="item.href"
                    class="block rounded-lg py-2 pr-3 pl-6 text-sm/7 font-semibold text-gray-900 hover:bg-gray-50">{{
                      item.name }}</DisclosureButton>
                </DisclosurePanel>
              </Disclosure>
              <a href="#"
                class="-mx-3 block rounded-lg px-3 py-2 text-base/7 font-semibold text-gray-900 hover:bg-gray-50">Features</a>
              <a href="#"
                class="-mx-3 block rounded-lg px-3 py-2 text-base/7 font-semibold text-gray-900 hover:bg-gray-50">Marketplace</a>
              <a href="#"
                class="-mx-3 block rounded-lg px-3 py-2 text-base/7 font-semibold text-gray-900 hover:bg-gray-50">Company</a>
            </div>
            <div class="py-6">
              <a href="#"
                class="-mx-3 block rounded-lg px-3 py-2.5 text-base/7 font-semibold text-gray-900 hover:bg-gray-50">Log
                in</a>
            </div>
          </div>
        </div>
      </DialogPanel>
    </Dialog>
  </header>
  <!-- <main class="pt-2 px-6">
    <router-view />
  </main> -->
  <main class="pt-20 px-6">
    <router-view />
  </main>
  <footer class="tracking-wide bg-gray-50 px-10 pt-12 pb-6 border-t border-gray-200">
      <div class="flex flex-wrap justify-between gap-10">
        <div class="max-w-md">
          <a href='javascript:void(0)'>
            <img :src="peptideImage" alt="logo" class="w-36" />
          </a>
          <div class="mt-6">
            <p class="text-slate-600 leading-relaxed text-sm">This product is designed and built by AnhKhoa, any feedback please contact gmail: anhkhoa.24052003@gmail.com</p>
          </div>
          <ul class="mt-10 flex space-x-5">
            <li>
              <a href='javascript:void(0)'>
                <svg xmlns="http://www.w3.org/2000/svg" class="fill-blue-600 w-8 h-8" viewBox="0 0 49.652 49.652">
                  <path d="M24.826 0C11.137 0 0 11.137 0 24.826c0 13.688 11.137 24.826 24.826 24.826 13.688 0 24.826-11.138 24.826-24.826C49.652 11.137 38.516 0 24.826 0zM31 25.7h-4.039v14.396h-5.985V25.7h-2.845v-5.088h2.845v-3.291c0-2.357 1.12-6.04 6.04-6.04l4.435.017v4.939h-3.219c-.524 0-1.269.262-1.269 1.386v2.99h4.56z" data-original="#000000" />
                </svg>
              </a>
            </li>
            <li>
              <a href='javascript:void(0)'>
                <svg xmlns="http://www.w3.org/2000/svg" class="w-8 h-8" viewBox="0 0 112.196 112.196">
                  <circle cx="56.098" cy="56.097" r="56.098" fill="#007ab9" data-original="#007ab9" />
                  <path fill="#fff" d="M89.616 60.611v23.128H76.207V62.161c0-5.418-1.936-9.118-6.791-9.118-3.705 0-5.906 2.491-6.878 4.903-.353.862-.444 2.059-.444 3.268v22.524h-13.41s.18-36.546 0-40.329h13.411v5.715c-.027.045-.065.089-.089.132h.089v-.132c1.782-2.742 4.96-6.662 12.085-6.662 8.822 0 15.436 5.764 15.436 18.149zm-54.96-36.642c-4.587 0-7.588 3.011-7.588 6.967 0 3.872 2.914 6.97 7.412 6.97h.087c4.677 0 7.585-3.098 7.585-6.97-.089-3.956-2.908-6.967-7.496-6.967zm-6.791 59.77H41.27v-40.33H27.865v40.33z" data-original="#f1f2f2" />
                </svg>
              </a>
            </li>
            <li>
              <a href='javascript:void(0)'>
                <svg xmlns="http://www.w3.org/2000/svg" class="w-8 h-8" viewBox="0 0 152 152">
                  <linearGradient id="a" x1="22.26" x2="129.74" y1="22.26" y2="129.74" gradientUnits="userSpaceOnUse">
                    <stop offset="0" stop-color="#fae100" />
                    <stop offset=".15" stop-color="#fcb720" />
                    <stop offset=".3" stop-color="#ff7950" />
                    <stop offset=".5" stop-color="#ff1c74" />
                    <stop offset="1" stop-color="#6c1cd1" />
                  </linearGradient>
                  <g data-name="Layer 2">
                    <g data-name="03.Instagram">
                      <rect width="152" height="152" fill="url(#a)" data-original="url(#a)" rx="76" />
                      <g fill="#fff">
                        <path fill="#ffffff10" d="M133.2 26c-11.08 20.34-26.75 41.32-46.33 60.9S46.31 122.12 26 133.2q-1.91-1.66-3.71-3.46A76 76 0 1 1 129.74 22.26q1.8 1.8 3.46 3.74z" data-original="#ffffff10" />
                        <path d="M94 36H58a22 22 0 0 0-22 22v36a22 22 0 0 0 22 22h36a22 22 0 0 0 22-22V58a22 22 0 0 0-22-22zm15 54.84A18.16 18.16 0 0 1 90.84 109H61.16A18.16 18.16 0 0 1 43 90.84V61.16A18.16 18.16 0 0 1 61.16 43h29.68A18.16 18.16 0 0 1 109 61.16z" data-original="#ffffff" />
                        <path d="m90.59 61.56-.19-.19-.16-.16A20.16 20.16 0 0 0 76 55.33 20.52 20.52 0 0 0 55.62 76a20.75 20.75 0 0 0 6 14.61 20.19 20.19 0 0 0 14.42 6 20.73 20.73 0 0 0 14.55-35.05zM76 89.56A13.56 13.56 0 1 1 89.37 76 13.46 13.46 0 0 1 76 89.56zm26.43-35.18a4.88 4.88 0 0 1-4.85 4.92 4.81 4.81 0 0 1-3.42-1.43 4.93 4.93 0 0 1 3.43-8.39 4.82 4.82 0 0 1 3.09 1.12l.1.1a3.05 3.05 0 0 1 .44.44l.11.12a4.92 4.92 0 0 1 1.1 3.12z" data-original="#ffffff" />
                      </g>
                    </g>
                  </g>
                </svg>
              </a>
            </li>
            <li>
              <a href='javascript:void(0)'>
                <svg xmlns="http://www.w3.org/2000/svg" class="w-8 h-8" viewBox="0 0 1227 1227">
                  <path d="M613.5 0C274.685 0 0 274.685 0 613.5S274.685 1227 613.5 1227 1227 952.315 1227 613.5 952.315 0 613.5 0z" data-original="#000000" />
                  <path fill="#fff" d="m680.617 557.98 262.632-305.288h-62.235L652.97 517.77 470.833 252.692H260.759l275.427 400.844-275.427 320.142h62.239l240.82-279.931 192.35 279.931h210.074L680.601 557.98zM345.423 299.545h95.595l440.024 629.411h-95.595z" data-original="#ffffff" />
                </svg>
              </a>
            </li>
          </ul>
        </div>

        <div class="max-lg:min-w-[140px]">
          <h4 class="text-slate-900 font-semibold text-sm relative max-sm:cursor-pointer">Services</h4>

          <ul class="mt-6 space-y-4">
            <li>
              <a href='javascript:void(0)' class="hover:text-slate-900 text-slate-600 text-sm font-normal">Web Development</a>
            </li>
            <li>
              <a href='javascript:void(0)' class="hover:text-slate-900 text-slate-600 text-sm font-normal">Pricing</a>
            </li>
            <li>
              <a href='javascript:void(0)' class="hover:text-slate-900 text-slate-600 text-sm font-normal">Support</a>
            </li>
            <li>
              <a href='javascript:void(0)' class="hover:text-slate-900 text-slate-600 text-sm font-normal">Client Portal</a>
            </li>
            <li>
              <a href='javascript:void(0)' class="hover:text-slate-900 text-slate-600 text-sm font-normal">Resources</a>
            </li>
          </ul>
        </div>

        <div class="max-lg:min-w-[140px]">
          <h4 class="text-slate-900 font-semibold text-sm relative max-sm:cursor-pointer">Platforms</h4>
          <ul class="space-y-4 mt-6">
            <li>
              <a href='javascript:void(0)' class="hover:text-slate-900 text-slate-600 text-sm font-normal">Hubspot</a>
            </li>
            <li>
              <a href='javascript:void(0)' class="hover:text-slate-900 text-slate-600 text-sm font-normal">Integration Services</a>
            </li>
            <li>
              <a href='javascript:void(0)' class="hover:text-slate-900 text-slate-600 text-sm font-normal">Marketing Glossar</a>
            </li>
            <li>
              <a href='javascript:void(0)' class="hover:text-slate-900 text-slate-600 text-sm font-normal">UIPath</a>
            </li>
          </ul>
        </div>

        <div class="max-lg:min-w-[140px]">
          <h4 class="text-slate-900 font-semibold text-sm relative max-sm:cursor-pointer">Company</h4>

          <ul class="space-y-4 mt-6">
            <li>
              <a href='javascript:void(0)' class="hover:text-slate-900 text-slate-600 text-sm font-normal">About us</a>
            </li>
            <li>
              <a href='javascript:void(0)' class="hover:text-slate-900 text-slate-600 text-sm font-normal">Careers</a>
            </li>
            <li>
              <a href='javascript:void(0)' class="hover:text-slate-900 text-slate-600 text-sm font-normal">Blog</a>
            </li>
            <li>
              <a href='javascript:void(0)' class="hover:text-slate-900 text-slate-600 text-sm font-normal">Portfolio</a>
            </li>
            <li>
              <a href='javascript:void(0)' class="hover:text-slate-900 text-slate-600 text-sm font-normal">Events</a>
            </li>
          </ul>
        </div>

        <div class="max-lg:min-w-[140px]">
          <h4 class="text-slate-900 font-semibold text-sm relative max-sm:cursor-pointer">Additional</h4>

          <ul class="space-y-4 mt-6">
            <li>
              <a href='javascript:void(0)' class="hover:text-slate-900 text-slate-600 text-sm font-normal">FAQ</a>
            </li>
            <li>
              <a href='javascript:void(0)' class="hover:text-slate-900 text-slate-600 text-sm font-normal">Partners</a>
            </li>
            <li>
              <a href='javascript:void(0)' class="hover:text-slate-900 text-slate-600 text-sm font-normal">Sitemap</a>
            </li>
            <li>
              <a href='javascript:void(0)' class="hover:text-slate-900 text-slate-600 text-sm font-normal">Contact</a>
            </li>
            <li>
              <a href='javascript:void(0)' class="hover:text-slate-900 text-slate-600 text-sm font-normal">News</a>
            </li>
          </ul>
        </div>
      </div>

      <hr class="mt-10 mb-6 border-gray-300" />

      <div class="flex flex-wrap max-md:flex-col gap-4">
        <ul class="md:flex md:space-x-6 max-md:space-y-2">
          <li>
            <a href='javascript:void(0)' class="hover:text-slate-900 text-slate-600 text-sm font-normal">Terms of Service</a>
          </li>
          <li>
            <a href='javascript:void(0)' class="hover:text-slate-900 text-slate-600 text-sm font-normal">Privacy Policy</a>
          </li>
          <li>
            <a href='javascript:void(0)' class="hover:text-slate-900 text-slate-600 text-sm font-normal">Security</a>
          </li>
        </ul>

        <p class="text-slate-600 text-sm md:ml-auto">© AnhKhoa. All rights reserved.</p>
      </div>
    </footer>
</template>

<script setup>
import peptideImage from '@/assets/images/anhkhoalogo.png'
import miniLogo from '@/assets/images/minilogo_anhkhoa.png'
import { ref, onMounted, onBeforeUnmount, nextTick } from 'vue'
import {
  Dialog,
  DialogPanel,
  Disclosure,
  DisclosureButton,
  DisclosurePanel,
  Popover,
  PopoverButton,
  PopoverGroup,
  PopoverPanel,
} from '@headlessui/vue'
import {
  ArrowPathIcon,
  Bars3Icon,
  ChartPieIcon,
  CursorArrowRaysIcon,
  FingerPrintIcon,
  SquaresPlusIcon,
  XMarkIcon,
  ArrowRightOnRectangleIcon
} from '@heroicons/vue/24/outline'
import { ChevronDownIcon, PhoneIcon, PlayCircleIcon } from '@heroicons/vue/20/solid'
import { useAuth } from '@/composables/useAuth'

const products = [
  { name: 'Dự đoán', description: 'Dự đoán chuỗi peptide với mô hình LSTM', href: '/forecast', icon: ChartPieIcon },
  { name: 'Dự đoán fasta', description: 'Speak directly to your customers', href: '/fileforecast', icon: CursorArrowRaysIcon },
  { name: 'Security', description: 'Your customers’ data will be safe and secure', href: '#', icon: FingerPrintIcon },
  { name: 'Integrations', description: 'Connect with third-party tools', href: '#', icon: SquaresPlusIcon },
  { name: 'Automations', description: 'Build strategic funnels that will convert', href: '#', icon: ArrowPathIcon },
]
const callsToAction = [
  { name: 'Watch demo', href: '#', icon: PlayCircleIcon },
  { name: 'Contact sales', href: '#', icon: PhoneIcon },
]

const mobileMenuOpen = ref(false)

const { user, loginWithGoogle, saveToken, fetchUserInfo, getToken, logout } = useAuth()
const showMenu = ref(false)
const dropdownRef = ref(null)

function toggleMenu() {
  showMenu.value = !showMenu.value
}

function handleClickOutside(event) {
  if (dropdownRef.value && !dropdownRef.value.contains(event.target)) {
    showMenu.value = false
  }
}

onMounted(() => {
  // 1. Lắng nghe message từ popup Google
  window.addEventListener('message', (event) => {
    const { access_token, user: receivedUser } = event.data
    if (!access_token) return
    saveToken(access_token)
    user.value = receivedUser
  })

  // 2. Gọi lại user nếu đã login
  if (getToken()) {
    fetchUserInfo()
  }

  // 3. Lắng nghe click ngoài dropdown để đóng
  nextTick(() => {
    window.addEventListener('click', handleClickOutside)
  })
})

onBeforeUnmount(() => {
  window.removeEventListener('click', handleClickOutside)
})


//hiệu ứng header
const isScrolled = ref(false)

function handleScroll() {
  isScrolled.value = window.scrollY > 10
}

onMounted(() => {
  window.addEventListener('scroll', handleScroll)
})

onBeforeUnmount(() => {
  window.removeEventListener('scroll', handleScroll)
})

</script>
