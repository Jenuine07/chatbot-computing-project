<template>
  <div :class="['chat-page-container', { 'sidebar-closed': !isSidebarOpen }]">
    <Sidebar 
      @toggleSidebar="toggleSidebar" 
      @startNewChat="handleNewChat"
      @loadChat="handleLoadChat"
      :chats="recentChats"
      :isOpen="isSidebarOpen" 
    />
    <main class="main-content" :class="{ 'project-selector-active': !selectedProject }">

      <Header :projectTitle="selectedProject" />

      <ProjectSelector v-if="!selectedProject" @projectSelected="handleProjectSelection" />

      <template v-else>
        <ChatWindow 
          :messages="messages" 
          :isLoading="isLoading" />
        <ChatInput @sendMessage="handleNewMessage" />
      </template>
    </main>
  </div>
</template>

<script setup>
import { ref, reactive, computed } from 'vue';
import axios from 'axios';
import Sidebar from './layout/Sidebar.vue';
import Header from './layout/Header.vue';
import ProjectSelector from './chat/ProjectSelector.vue';
import ChatWindow from './chat/ChatWindow.vue';
import ChatInput from './chat/ChatInput.vue';
import '@/assets/styles/ChatPage.css';

const selectedProject = ref(null);
const chatHistory = reactive({ /* ... data history ... */ });
const isSidebarOpen = ref(true);
const messages = ref([]);
const currentChatId = ref(null);
const isLoading = ref(false);

const recentChats = computed(() => {
  const groupedChats = { Arsip: [], 'Undang-undang': [] };
  Object.keys(chatHistory).forEach(id => {
    const chat = chatHistory[id];
    const project = chat.project || 'Arsip';
    if (groupedChats[project]) {
      groupedChats[project].push({ id, title: chat.title });
    }
  });
  groupedChats.Arsip.reverse();
  groupedChats['Undang-undang'].reverse();
  return groupedChats;
});

function handleProjectSelection(projectName) {
  selectedProject.value = projectName;
}

function toggleSidebar() { isSidebarOpen.value = !isSidebarOpen.value; }

function handleNewChat() {
  if (messages.value.length > 0) {
    if (currentChatId.value && chatHistory[currentChatId.value]) {
      chatHistory[currentChatId.value].messages = [...messages.value];
    } else {
      const newChatId = `chat-${Date.now()}`;
      const firstUserMessage = messages.value.find(m => m.sender === 'user');
      let newTitle = "Percakapan Baru";
      if (firstUserMessage) {
        newTitle = firstUserMessage.text.substring(0, 30);
        if (firstUserMessage.text.length > 30) { newTitle += '...'; }
      }
      chatHistory[newChatId] = {
        title: newTitle,
        messages: [...messages.value],
        project: selectedProject.value 
      };
    }
  }
  messages.value = [];
  currentChatId.value = null;
  selectedProject.value = null;
}

function handleLoadChat(chatId) {
  if (chatHistory[chatId]) {
    selectedProject.value = chatHistory[chatId].project;
    
    messages.value = [
      ...chatHistory[chatId].messages.map(msg => ({ ...msg, shouldAnimate: false }))
    ];
    
    currentChatId.value = chatId; 
    if (!isSidebarOpen.value) { isSidebarOpen.value = true; }
  }
}

async function handleNewMessage(text) {
  messages.value.push({ id: Date.now(), text: text, sender: 'user' });

  if (!currentChatId.value) { 
    currentChatId.value = `chat-${Date.now()}`; 
  }

  isLoading.value = true;

  try {
    const response = await axios.post('http://localhost:3000/api/chat', {
      prompt: text,
      sessionId: currentChatId.value,
      project: selectedProject.value
    });

    const botReply = response.data?.response || "Tidak ada respons dari model.";

    messages.value.push({
      id: Date.now() + 1,
      text: botReply,
      sender: 'ai',
      shouldAnimate: true 
    });

    if (chatHistory[currentChatId.value]) {
      chatHistory[currentChatId.value].messages.push({
        id: Date.now() + 1,
        text: botReply,
        sender: 'ai'
      });
    } else {
      chatHistory[currentChatId.value] = {
        title: text.substring(0, 30),
        messages: [...messages.value],
        project: selectedProject.value
      };
    }

  } catch (error) {
    console.error("Error memanggil backend:", error);
    messages.value.push({
      id: Date.now() + 1,
      text: "Maaf, terjadi kesalahan saat menghubungi server.",
      sender: 'ai',
      shouldAnimate: true 
    });
  } finally {
    isLoading.value = false;
  }
}

</script>