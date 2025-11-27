<template>
  <div class="project-selector-container">
    <div class="header-prompt">
      <h1>Halo, <span class="greeting-name">viorano!</span></h1>
      <p class="subtitle">Pilih basis data untuk memulai percakapan</p>
    </div>

    <div class="project-cards">
      <div class="project-card" @click="selectProject('Arsip')">
        <div class="card-icon">📁</div>
        <h2 class="card-title">Arsip</h2>
        <p class="card-description">Jelajahi dan tanyakan data dari arsip digital Kompas.</p>
      </div>
      <div class="project-card" @click="selectProject('Undang-undang')">
        <div class="card-icon">📜</div>
        <h2 class="card-title">Undang-undang</h2>
        <p class="card-description">Analisis dan cari informasi dari dokumen perundang-undangan.</p>
      </div>
    </div>
  </div>
</template>

<script setup>
const emit = defineEmits(['projectSelected']);

function selectProject(projectName) {
  emit('projectSelected', projectName);
}
</script>