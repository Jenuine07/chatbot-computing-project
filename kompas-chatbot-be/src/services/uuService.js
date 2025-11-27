const { queryPythonRagModel } = require("./pythonBridge");

async function generateUuResponse(prompt) {
  try {
    const answer = await queryPythonRagModel(prompt);
    return answer;
  } catch (error) {
    console.error("Error in UU Service:", error.message);
    return "Maaf, layanan Undang-Undang sedang tidak tersedia.";
  }
}

module.exports = {
  generateUuResponse,
};