const db = require('../db');
const arsipService = require('../services/arsipService');
const uuService = require('../services/uuService');

const handleChat = async (req, res) => {
  const { prompt, sessionId, project } = req.body;

  if (!prompt || !sessionId || !project) {
    return res.status(400).json({ error: 'Prompt, sessionId, and project are required.' });
  }

  try {
    let botResponseText;

    if (project === 'Arsip') {
      botResponseText = await arsipService.generateArsipResponse(prompt);
    } else if (project === 'Undang-undang') {
      botResponseText = await uuService.generateUuResponse(prompt);
    } else {
      return res.status(400).json({ error: 'Invalid project type specified.' });
    }

    res.status(200).json({ response: botResponseText });

  } catch (error) {
    console.error('Error in chat controller:', error);
    res.status(500).json({ error: 'Internal server error.' });
  }
};

module.exports = {
  handleChat,
};