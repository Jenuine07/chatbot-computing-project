// src/composables/useAuth.js
import { reactive, computed } from 'vue'

const STORAGE_USERS = 'demo_users'
const STORAGE_USER = 'current_user'
const STORAGE_TOKEN = 'current_token'

const state = reactive({
  user: JSON.parse(localStorage.getItem(STORAGE_USER)) || null,
  token: localStorage.getItem(STORAGE_TOKEN) || null,
})

export function useAuth() {
  const isAuthenticated = computed(() => !!state.token)

  function saveSession(user) {
    state.user = { id: user.id, name: user.name, email: user.email }
    state.token = 'dummy-token-' + Date.now()

    localStorage.setItem(STORAGE_USER, JSON.stringify(state.user))
    localStorage.setItem(STORAGE_TOKEN, state.token)
  }

  async function register({ name, email, password }) {
    const users = JSON.parse(localStorage.getItem(STORAGE_USERS)) || []

    const exists = users.some((u) => u.email === email)
    if (exists) {
      throw new Error('Email sudah terdaftar.')
    }

    const newUser = {
      id: Date.now(),
      name,
      email,
      password, // ⚠️ hanya demo front-end, jangan dipakai di produksi
    }

    users.push(newUser)
    localStorage.setItem(STORAGE_USERS, JSON.stringify(users))

    saveSession(newUser)
  }

  async function login({ email, password }) {
    const users = JSON.parse(localStorage.getItem(STORAGE_USERS)) || []

    const user = users.find(
      (u) => u.email === email && u.password === password,
    )

    if (!user) {
      throw new Error('Email atau password salah.')
    }

    saveSession(user)
  }

  function logout() {
    state.user = null
    state.token = null
    localStorage.removeItem(STORAGE_USER)
    localStorage.removeItem(STORAGE_TOKEN)
  }

  return {
    user: computed(() => state.user),
    token: computed(() => state.token),
    isAuthenticated,
    register,
    login,
    logout,
  }
}
