// src/index.js
// src/index.js
require('dotenv').config()
const express = require('express')
const cors = require('cors')
const chatRoutes = require('./routes/chat')
const authRoutes = require('./routes/auth')  // <- TAMBAH BARIS INI

const app = express()
const PORT = process.env.PORT || 3000

// Middleware
app.use(cors())           // Enable Cross-Origin Resource Sharing
app.use(express.json())   // Enable parsing of JSON request bodies

// API Routes
app.use('/api/auth', authRoutes)  // <- TAMBAH BARIS INI
app.use('/api/chat', chatRoutes)

app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`)
})


const app = express()
const PORT = process.env.PORT || 3000

// Middleware
app.use(cors())               // Enable Cross-Origin Resource Sharing
app.use(express.json())       // Enable parsing of JSON request bodies

// API Routes
app.use('/api/chat', chatRoutes)
app.use('/api/auth', authRoutes)   // ✅ dan tambahkan ini

app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`)
})
