<template>
  <div class="chat-window" ref="chatWindowRef">
    <div class="message-container">
      <MessageBubble
        v-for="msg in messages"
        :key="msg.id"
        :message="msg"
      />
      <MessageBubble
        v-if="isLoading"
        :message="{ id: 'loading', text: '...', sender: 'ai' }"
        class="typing-indicator"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, watch, nextTick } from 'vue';
import MessageBubble from './MessageBubble.vue';

const props = defineProps({
  messages: {
    type: Array,
    required: true,
  },
  isLoading: {
    type: Boolean,
    default: false,
  }
});

const chatWindowRef = ref(null);

const scrollToBottom = async () => {
  await nextTick();
  if (chatWindowRef.value) {
    chatWindowRef.value.scrollTop = chatWindowRef.value.scrollHeight;
  }
};

watch(
  () => [props.messages, props.isLoading],
  () => {
    scrollToBottom();
  },
  { deep: true }
);
</script>

<style scoped>
:deep(.message-bubble.ai.typing-indicator) {
  width: fit-content;
  animation: typing-pulse 1.5s infinite ease-in-out;
}

@keyframes typing-pulse {
  0% {
    transform: scale(1);
    opacity: 0.6;
  }
  50% {
    transform: scale(1.05);
    opacity: 1;
  }
  100% {
    transform: scale(1);
    opacity: 0.6;
  }
}
</style>