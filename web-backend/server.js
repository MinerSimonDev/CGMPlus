const express = require("express");
const { MongoClient } = require("mongodb");
require('dotenv').config()

const app = express();
const PORT = 3000;
const MONGO_URI = process.env.MONGO_URI;
const client = new MongoClient(MONGO_URI);

let db;

// connect to mongodb
async function connectDB() {
  await client.connect();
  db = client.db("test");
  console.log("MongoDB verbunden");
}

connectDB();

// api endpoint: fetch new data
app.get("/data", async (req, res) => {
  const data = await db.collection("entries").find().sort({ timestamp: -1 }).limit(100).toArray();
  res.json(data);
});

// api endpoint: add new data
app.post("/add", express.json(), async (req, res) => {
  const newEntry = req.body;
  await db.collection("entries").insertOne(newEntry);
  res.json({ message: "Eintrag hinzugefügt" });
});

// start server on port 3000
app.listen(PORT, () => {
  console.log(`Server läuft auf http://localhost:${PORT}`);
});
