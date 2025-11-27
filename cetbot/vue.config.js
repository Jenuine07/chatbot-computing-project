const { defineConfig } = require('@vue/cli-service')

module.exports = defineConfig({
  transpileDependencies: true,
  pages: {
    index: {
      entry: 'src/main.js', // atau 'src/main.js' sesuai punya kamu
      title: 'Kompas AI - Chatbot', // <- ini yang muncul di tab
    },
  },
})
