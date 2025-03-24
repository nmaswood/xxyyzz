const express = require("express");
const path = require("path");
const { spawn } = require("child_process");

const app = express();
const PORT = process.env.PORT || 3000;

// Serve up files in "public" as static
app.use(express.static(path.join(__dirname, "public")));

// Also serve "static" folder (for graph.png)
app.use("/static", express.static(path.join(__dirname, "static")));

app.get("/generate-graph", (req, res) => {
  const bookId = req.query.book_id || "12345";

  const pythonProcess = spawn("python", [
    path.join(__dirname, "python", "main.py"),
    bookId,
  ]);

  // Capture Python's output
  let stdoutData = "";
  pythonProcess.stdout.on("data", (chunk) => {
    stdoutData += chunk.toString();
  });

  let stderrData = "";
  pythonProcess.stderr.on("data", (chunk) => {
    stderrData += chunk.toString();
  });

  pythonProcess.on("close", (code) => {
    console.log(`Python script exited with code ${code}`);
    if (stderrData) {
      console.error("Python stderr:", stderrData);
    }
    // When done, we can send back a message
    // The front-end can then reload /static/graph.png
    res.send("Graph generation complete");
  });
});

// Start the server
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
