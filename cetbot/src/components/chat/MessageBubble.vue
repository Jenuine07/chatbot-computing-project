<template>
  <div :class="['message-bubble', message.sender]">
    <div class="sizer" v-html="formattedText"></div>
    <p v-if="isAnimating" ref="textEl" class="text-overlay"></p>
    <div v-if="!isAnimating" v-html="formattedText" class="text-overlay"></div>
  </div>
</template>

<script setup>
import { computed, ref, onMounted } from 'vue';
import { gsap } from 'gsap';
import { TextPlugin } from 'gsap/TextPlugin'; 

gsap.registerPlugin(TextPlugin);

const props = defineProps({
  message: {
    type: Object,
    required: true,
  },
});

const isAnimating = ref(
  props.message.shouldAnimate === true && props.message.sender === 'ai'
);
const textEl = ref(null);

const formattedText = computed(() => {
  let text = props.message.text;

  const boldRegex = /\*\*(.*?)\*\*/g;
  text = text.replace(boldRegex, '<strong>$1</strong>');

  const markdownLinkRegex = /\[(.*?)\]\((https?:\/\/[^\s)]+)\)/g;
  text = text.replace(markdownLinkRegex, '<a href="$2" target="_blank" rel="noopener noreferrer">$1</a>');

  const rawUrlRegex = /(?<!href=")(httpsS?:\/\/[^\s]+)/g;
  text = text.replace(rawUrlRegex, (url) => {
    if (text.includes(`href="${url}"`)) {
      return url;
    }
    return `<a href="${url}" target="_blank" rel="noopener noreferrer">${url}</a>`;
  });

  return text;
});

onMounted(() => {
  if (isAnimating.value && textEl.value) {
    const animatedText = props.message.text.replace(/\n/g, "<br>");
    
    const charsPerSecond = 75; 
    const calculatedDuration = props.message.text.length / charsPerSecond;

    gsap.to(textEl.value, {
      duration: calculatedDuration,
      text: animatedText, 
      type: "innerHTML", 
      ease: 'none',
      onComplete: () => {
        isAnimating.value = false;
      }
    });
  }
});
</script>

<style scoped>
  .message-bubble {
    position: relative;
  }

  .sizer {
    visibility: hidden;
    white-space: pre-wrap;
  }

  .text-overlay {
    position: absolute;
    top: 0;
    left: 0;
    padding: 0.8rem 1.2rem;
    white-space: pre-wrap; 
    margin: 0; 
    width: 100%;
    box-sizing: border-box; 
  }

  .message-bubble.ai :deep(a) {
    color: #76c8ff;
    text-decoration: underline;
  }

  .message-bubble.ai :deep(a:hover) {
    color: #a9dbff;
  }

  .message-bubble :deep(strong) {
    font-weight: 700;
  }
</style>