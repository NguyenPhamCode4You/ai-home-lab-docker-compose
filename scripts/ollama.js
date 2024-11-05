const express = require("express");
const axios = require("axios");
const fs = require("fs"); // Import File System module
const app = express();
const PORT = 3000;
const OLLAMA_BASE_URL = "http://localhost:11434/api/generate";

const { cleanJsonResponse } = require("./helpers");
// Load the prompt from prompt.txt
const parseEmail = fs.readFileSync("./parseEmail.txt", "utf8");
const portCorrect = fs.readFileSync("./portCorrect.txt", "utf8");

// Middleware to parse JSON request bodies
app.use(express.json());

// POST endpoint to send prompt to Ollama
app.post("/api/parse-email/gemma", async (req, res) => {
  try {
    const { data } = req.body;
    // Send the prompt to Ollama's API
    const response = await axios.post(OLLAMA_BASE_URL, {
      // model: 'qwen2.5:14b-instruct-q8_0',
      // model: "llama3.1:8b-instruct-q8_0",
      model: "gemma2:9b-instruct-q8_0",
      prompt: parseEmail + data,
      stream: false,
    });
    var formattedJson = cleanJsonResponse(response);
    res.json(JSON.parse(formattedJson));
  } catch (error) {
    console.error("Error communicating with Ollama:", error.message);
    res.status(500).json({ error: "Failed to communicate with Ollama" });
  }
});

app.post("/api/parse-email", async (req, res) => {
  try {
    const { data } = req.body;
    // Send the prompt to Ollama's API
    const response = await axios.post(OLLAMA_BASE_URL, {
      model: "nichealpham/email-extract",
      prompt: parseEmail + data,
      stream: false,
    });
    var formattedJson = cleanJsonResponse(response);
    res.json(JSON.parse(formattedJson));
  } catch (error) {
    console.error("Error communicating with Ollama:", error.message);
    res.status(500).json({ error: "Failed to communicate with Ollama" });
  }
});

app.post("/api/port-correct", async (req, res) => {
  try {
    const { data } = req.body;
    // Send the prompt to Ollama's API
    const response = await axios.post(OLLAMA_BASE_URL, {
      model: "nichealpham/port-name-correction",
      prompt: portCorrect + data,
      stream: false,
    });
    res.json({ result: response.data.response });
  } catch (error) {
    console.error("Error communicating with Ollama:", error.message);
    res.status(500).json({ error: "Failed to communicate with Ollama" });
  }
});

// Start the Express server
app.listen(PORT, () => {
  console.log(`Express server running on http://localhost:${PORT}`);
});
