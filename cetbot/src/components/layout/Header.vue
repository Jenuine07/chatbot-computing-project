<template>
  <header class="topbar">
    <div class="left">
      <h1 class="app-title">Kompas AI</h1>
      <span class="breadcrumb">
        / {{ projectTitle || 'Dashboard' }}
      </span>
    </div>

    <div class="right">
      <!-- SUDAH LOGIN -->
      <div
        v-if="isAuthenticated"
        class="user-menu"
        @click="toggleMenu"
      >
        <img
          class="avatar"
          src="https://i.pravatar.cc/40?img=5"
          alt="profile"
        />
        <span class="user-name">{{ user?.name || 'Pengguna' }}</span>

        <div
          v-if="showMenu"
          class="menu-dropdown"
        >
          <div class="menu-item email">
            {{ user?.email }}
          </div>
          <button
            class="menu-item danger"
            @click.stop="handleLogout"
          >
            Keluar
          </button>
        </div>
      </div>

      <!-- BELUM LOGIN -->
      <button
        v-else
        class="login-btn"
        @click="showAuthModal = true"
      >
        Masuk / Daftar
      </button>
    </div>

    <!-- Modal Login / Register -->
    <AuthModal v-model="showAuthModal" />
  </header>
</template>

<script setup>
import { ref } from 'vue'
import AuthModal from './AuthModal.vue'
import { useAuth } from '../../composables/useAuth'

// dipakai hanya untuk render, jadi nggak perlu disimpan ke variabel
defineProps({
  projectTitle: {
    type: String,
    default: '',
  },
})

const showAuthModal = ref(false)
const showMenu = ref(false)

const { user, isAuthenticated, logout } = useAuth()

function toggleMenu() {
  showMenu.value = !showMenu.value
}

function handleLogout() {
  logout()
  showMenu.value = false
}
</script>

<style scoped>
.topbar {
  height: 72px;
  padding: 0 32px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: #02163c;
  color: #e5e7eb;
  border-bottom: 1px solid rgba(148, 163, 184, 0.2);
}

.left {
  display: flex;
  align-items: baseline;
  gap: 8px;
}

.app-title {
  font-size: 20px;
  font-weight: 700;
}

.breadcrumb {
  font-size: 14px;
  color: #9ca3af;
}

.right {
  display: flex;
  align-items: center;
  position: relative;
}

.login-btn {
  border-radius: 999px;
  border: 1px solid #38bdf8;
  background: transparent;
  color: #e0f2fe;
  padding: 6px 14px;
  cursor: pointer;
  font-size: 14px;
}

.login-btn:hover {
  background: rgba(56, 189, 248, 0.15);
}

.user-menu {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  position: relative;
}

.avatar {
  width: 36px;
  height: 36px;
  border-radius: 999px;
  object-fit: cover;
}

.user-name {
  font-size: 14px;
}

.menu-dropdown {
  position: absolute;
  right: 0;
  top: 52px;
  background: #020617;
  border-radius: 12px;
  padding: 8px;
  min-width: 180px;
  box-shadow: 0 12px 30px rgba(0, 0, 0, 0.4);
  z-index: 50;
}

.menu-item {
  font-size: 14px;
  padding: 6px 10px;
  border-radius: 8px;
  color: #e5e7eb;
  text-align: left;
  width: 100%;
  background: transparent;
  border: none;
}

.menu-item:hover {
  background: #111827;
}

.menu-item.danger {
  color: #fecaca;
}
</style>
