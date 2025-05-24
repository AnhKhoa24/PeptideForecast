import { ref } from 'vue'

const user = ref<any>(null)

export function useAuth() {
    function saveToken(token: string) {
        localStorage.setItem('access_token', token)
    }
    function logout() {
        removeToken()
        user.value = null
        console.log('🚪 Đã đăng xuất')
    }

    function getToken() {
        return localStorage.getItem('access_token')
    }

    function removeToken() {
        localStorage.removeItem('access_token')
        user.value = null
    }

    function loginWithGoogle() {
        window.open(
            'http://localhost:8080/auth/login/google',
            '_blank',
            'width=500,height=600'
        )
    }

    async function fetchUserInfo() {
        const token = getToken()
        if (!token) return

        try {
            const res = await fetch('http://localhost:8080/user/profile', {
                headers: { token }
            })
            const data = await res.json()
            if (res.ok) {
                user.value = {
                    name: data.name,
                    email: data.email,
                    picture: data.picture || `https://api.dicebear.com/7.x/identicon/svg?seed=${encodeURIComponent(data.email)}`
                }

            } else {
                removeToken()
            }
        } catch {
            removeToken()
        }
    }

    return {
        user,
        loginWithGoogle,
        getToken,
        saveToken,
        removeToken,
        fetchUserInfo,
        logout 
    }
}
