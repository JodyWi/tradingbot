// server/index.js or server.js
const express = require("express");
const path = require("path");
const fs = require("fs");

const app = express();
const PORT = 3001;

// Serve balances.json at /api/balances
app.get("/api/balances", (req, res) => {
  const filePath = path.resolve(__dirname, "../database/data/balances.json");
  fs.readFile(filePath, "utf8", (err, data) => {
    if (err) {
      console.error("Error reading balances.json:", err);
      return res.status(500).json({ error: "Failed to read balances file" });
    }

    try {
      const json = JSON.parse(data);
      res.json(json);
    } catch (parseErr) {
      console.error("Invalid JSON in balances.json:", parseErr);
      res.status(500).json({ error: "Invalid JSON format" });
    }
  });
});

app.listen(PORT, () => {
  console.log(`✅ Backend running at http://localhost:${PORT}`);
});
