<!-- src/components/auth/AuthModal.vue -->
<template>
  <div class="backdrop" @click.self="close">
    <div class="auth-card">
      <div class="auth-header">
        <button
          class="tab"
          :class="{ active: mode === 'login' }"
          @click="mode = 'login'"
        >
          Masuk
        </button>
        <button
          class="tab"
          :class="{ active: mode === 'register' }"
          @click="mode = 'register'"
        >
          Daftar
        </button>
      </div>

      <form class="auth-form" @submit.prevent="handleSubmit">
        <div v-if="mode === 'register'" class="field">
          <label>Nama</label>
          <input v-model="form.name" type="text" required />
        </div>

        <div class="field">
          <label>Email</label>
          <input v-model="form.email" type="email" required />
        </div>

        <div class="field">
          <label>Password</label>
          <input v-model="form.password" type="password" required />
        </div>

        <p v-if="error" class="error">{{ error }}</p>

        <button type="submit" class="submit-btn" :disabled="loading">
          {{ loading ? 'Memproses...' : (mode === 'login' ? 'Masuk' : 'Daftar') }}
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useAuth } from '@/composables/useAuth'

const props = defineProps({
  modelValue: { type: Boolean, default: false },
})

const emit = defineEmits(['update:modelValue'])

const mode = ref('login')
const form = ref({
  name: '',
  email: '',
  password: '',
})
const error = ref('')
const loading = ref(false)

const { login, register } = useAuth()

function resetForm() {
  form.value = { name: '', email: '', password: '' }
  error.value = ''
  loading.value = false
  mode.value = 'login'
}

function close() {
  emit('update:modelValue', false)
  resetForm()
}

watch(
  () => props.modelValue,
  (val) => {
    if (!val) resetForm()
  },
)

async function handleSubmit() {
  loading.value = true
  error.value = ''

  try {
    if (mode.value === 'login') {
      await login({
        email: form.value.email,
        password: form.value.password,
      })
    } else {
      await register({
        name: form.value.name,
        email: form.value.email,
        password: form.value.password,
      })
    }

    // ✅ login/register sukses → tutup modal → blur hilang
    close()
  } catch (err) {
    error.value = err?.message || 'Terjadi kesalahan, silakan coba lagi.'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.backdrop {
  position: fixed;
  inset: 0;
  /* warna gelap transparan di atas background */
  background: rgba(0, 0, 0, 0.35);

  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 999;

  /* ✨ KUNCI UTAMA: blur background di belakang overlay */
  backdrop-filter: blur(6px);
  -webkit-backdrop-filter: blur(6px); /* untuk Safari */
}

.auth-card {
  background: #0c2a5b;
  border-radius: 16px;
  padding: 24px 28px;
  width: 360px;
  max-width: 90vw;
  box-shadow: 0 12px 30px rgba(0, 0, 0, 0.35);
  color: #fff;
}
.auth-header {
  display: flex;
  margin-bottom: 20px;
  border-radius: 999px;
  background: #092044;
  padding: 4px;
}

.tab {
  flex: 1;
  border: none;
  background: transparent;
  color: #9db4ff;
  padding: 8px 0;
  border-radius: 999px;
  cursor: pointer;
  font-weight: 500;
}

.tab.active {
  background: linear-gradient(135deg, #7c3aed, #38bdf8);
  color: #fff;
}

.auth-form {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.field label {
  font-size: 13px;
  margin-bottom: 4px;
  display: block;
  color: #c7d2fe;
}

.field input {
  width: 100%;
  border-radius: 8px;
  border: 1px solid #1d4ed8;
  background: #020617;
  padding: 8px 10px;
  color: #e5e7eb;
  outline: none;
}

.field input:focus {
  border-color: #38bdf8;
}

.error {
  color: #fecaca;
  font-size: 13px;
}

.submit-btn {
  margin-top: 8px;
  width: 100%;
  border: none;
  border-radius: 999px;
  padding: 10px 0;
  font-weight: 600;
  cursor: pointer;
  background: linear-gradient(135deg, #22c55e, #14b8a6);
  color: #020617;
}
</style>
