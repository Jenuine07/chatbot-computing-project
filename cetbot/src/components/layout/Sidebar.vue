<template>
  <aside class="sidebar">
    <div class="sidebar-item logo" @click="emit('toggleSidebar')">
      <img v-if="!isOpen" :src="kompasLogo" alt="Kompas Logo" class="kompas-logo-collapsed">
      <template v-if="isOpen">
        <img :src="kompasLogo" alt="Kompas AI Logo" class="kompas-logo-full">
        <span class="text-and-arrow">
          <span class="text">Kompas AI</span>
          <span class="arrow-icon">◀</span>
        </span>
      </template>
    </div>
    
    <button class="sidebar-item new-chat-btn" @click="emit('startNewChat')">
      <span class="icon">✎</span>
      <span v-show="isOpen" class="text">New Chat</span>
    </button>
    
    <div class="history-groups-container">
      <div v-if="isOpen" class="chat-group">
        <div class="recent-title clickable" @click="toggleDropdown('Arsip')">
          <span>Arsip</span>
          <span class="dropdown-arrow" :class="{ 'is-open': dropdownStates.Arsip }">▶</span>
        </div>
        <ul v-show="dropdownStates.Arsip" v-if="chats.Arsip.length > 0" class="recent-list">
          <li 
            class="sidebar-item"
            v-for="chat in chats.Arsip" 
            :key="chat.id" 
            @click="emit('loadChat', chat.id)"
          >
            <span class="text">{{ chat.title }}</span>
          </li>
        </ul>
      </div>

      <div v-if="isOpen" class="chat-group">
        <div class="recent-title clickable" @click="toggleDropdown('Undang-undang')">
          <span>Undang-undang</span>
          <span class="dropdown-arrow" :class="{ 'is-open': dropdownStates['Undang-undang'] }">▶</span>
        </div>
        <ul v-show="dropdownStates['Undang-undang']" v-if="chats['Undang-undang'].length > 0" class="recent-list">
          <li 
            class="sidebar-item"
            v-for="chat in chats['Undang-undang']" 
            :key="chat.id" 
            @click="emit('loadChat', chat.id)"
          >
            <span class="text">{{ chat.title }}</span>
          </li>
        </ul>
      </div>
    </div>

    <div class="sidebar-footer">
       <div class="sidebar-item settings">
         <span class="icon">⚙️</span>
         <span v-show="isOpen" class="text">Setelan & Bantuan</span>
       </div>
    </div>
  </aside>
</template>

<script setup>
import { reactive, defineProps, defineEmits } from 'vue';
import kompasLogo from '@/assets/kompas-logo.png';

const dropdownStates = reactive({
  Arsip: false,
  'Undang-undang': false,
});

function toggleDropdown(project) {
  dropdownStates[project] = !dropdownStates[project];
}

defineProps({
  chats: { type: Object, required: true },
  isOpen: { type: Boolean, required: true },
});

const emit = defineEmits(['toggleSidebar', 'startNewChat', 'loadChat']);
</script>