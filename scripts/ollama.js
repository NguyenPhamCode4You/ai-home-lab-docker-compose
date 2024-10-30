const express = require("express");
const axios = require("axios");
const fs = require("fs"); // Import File System module
const app = express();
const PORT = 3000;
const OLLAMA_BASE_URL = "http://localhost:11434/api/generate";

// Load the prompt from prompt.txt
const prompt = fs.readFileSync("prompt.txt", "utf8"); // Read file content as a string

// Middleware to parse JSON request bodies
app.use(express.json());

// POST endpoint to send prompt to Ollama
app.post("/api/sendPrompt", async (req, res) => {
  try {
    const { data } = req.body;

    // Send the prompt to Ollama's API
    const response = await axios.post(OLLAMA_BASE_URL, {
      model: "llama3.2:3b-instruct-fp16", // Replace with the correct model name for your use case
      prompt: prompt + data, // Use the loaded prompt here
      stream: false,
    });

    var jsonText = response.data.response;
    // Step 1: Remove <json> tags and newline escape characters
    const cleanedText = jsonText
      .replace("<json>", "")
      .replace("</json>", "")
      .replace("\\n", "");
    console.log(cleanedText);

    // Step 2: Parse the cleaned JSON text
    const jsonObject = JSON.parse(cleanedText);

    // Step 3: Format the JSON with indentation
    const formattedJson = JSON.stringify(jsonObject, null, 2);

    // Output the formatted JSON
    console.log(formattedJson);

    console.log(formattedJson);
    res.json(jsonObject);
  } catch (error) {
    console.error("Error communicating with Ollama:", error.message);
    res.status(500).json({ error: "Failed to communicate with Ollama" });
  }
});

// Start the Express server
app.listen(PORT, () => {
  console.log(`Express server running on http://localhost:${PORT}`);
});
