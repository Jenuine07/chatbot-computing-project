<template>
  <form class="chat-input-area" @submit.prevent="handleSend">
    <input
      v-model="newMessage"
      type="text"
      placeholder="Ketik pesan Anda di sini..."
    />
    <button type="submit">Kirim</button>
  </form>
  
  <div class="ai-warning-footer">
    <p>Kompas AI dapat membuat kesalahan. Pertimbangkan untuk memverifikasi informasi penting.</p>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const newMessage = ref('');

const emit = defineEmits(['sendMessage']);

function handleSend() {
  if (newMessage.value.trim() !== '') {
    emit('sendMessage', newMessage.value);
    newMessage.value = '';
  }
}
</script>