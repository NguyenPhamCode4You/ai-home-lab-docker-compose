const express = require("express");
const axios = require("axios");
const fs = require("fs"); // Import File System module
const app = express();
const PORT = 3000;
const OLLAMA_BASE_URL = "http://localhost:11434/api/generate";

// Load the prompt from prompt.txt
const prompt = fs.readFileSync("./prompt.txt", "utf8"); // Read file content as a string

// Middleware to parse JSON request bodies
app.use(express.json());

// POST endpoint to send prompt to Ollama
app.post("/api/sendPrompt", async (req, res) => {
  try {
    const { data } = req.body;

    // Send the prompt to Ollama's API
    const response = await axios.post(OLLAMA_BASE_URL, {
      // model: 'qwen2.5:14b-instruct-q8_0',
      model: "gemma2:9b-instruct-q8_0",
      prompt: prompt + data,
      stream: false,
    });

    var jsonText = response.data.response;
    // Step 1: Remove <json> tags and newline escape characters
    jsonText = jsonText
      .replace("<json>", "")
      .replace("</json>", "")
      .replace("\\n", "");
    // Step 2: Parse the cleaned JSON text
    const jsonObject = JSON.parse(jsonText);
    // Step 3: Format the JSON with indentation
    const formattedJson = JSON.stringify(jsonObject, null, 2);
    // Output the formatted JSON
    console.log(formattedJson);
    res.json(JSON.parse(formattedJson));
  } catch (error) {
    console.error("Error communicating with Ollama:", error.message);
    res.status(500).json({ error: "Failed to communicate with Ollama" });
  }
});

// Start the Express server
app.listen(PORT, () => {
  console.log(`Express server running on http://localhost:${PORT}`);
});
