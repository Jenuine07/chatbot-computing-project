const axios = require("axios");

async function queryPythonRagModel(prompt) {
  try {
    const response = await axios.post("http://localhost:8000/chat", { query: prompt });
    return response.data.answer;
  } catch (error) {
    console.error("Error connecting to Python RAG model:", error.message);
    throw new Error("Python RAG model unavailable");
  }
}

module.exports = { queryPythonRagModel };
