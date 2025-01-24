const express = require("express");
const { MongoClient } = require("mongodb");
require('dotenv').config();

const app = express();
const PORT = 3000;
const MONGO_URI = process.env.MONGO_URI;
console.log("MongoDB URI:", MONGO_URI);
const client = new MongoClient(MONGO_URI);

let db;

// connect to mongodb
async function connectDB() {
  await client.connect();
  db = client.db("test");
  console.log("MongoDB verbunden");
}

connectDB();

// api endpoint: fetch new data with a time filter
app.get("/data", async (req, res) => {
  const { period, unit } = req.query; // "days" or "hours"

  if (!period || !unit || isNaN(period)) {
    return res.status(400).json({ error: "Bitte gib einen gültigen Zeitraum (Zahl und Einheit) an." });
  }

  // calc date
  let timeFilter;
  const currentTime = new Date();

  if (unit === "days") {
    timeFilter = new Date(currentTime.setDate(currentTime.getDate() - period)); // X Tage zurück
  } else if (unit === "hours") {
    timeFilter = new Date(currentTime.setHours(currentTime.getHours() - period)); // X Stunden zurück
  } else {
    return res.status(400).json({ error: "Die Einheit muss entweder 'days' oder 'hours' sein." });
  }

  try {
    const data = await db
      .collection("entries")
      .find({
        dateString: { $gte: timeFilter.toISOString() } // Filter nach dem ISO-Format von dateString
      })
      .sort({ dateString: -1 })
      .toArray();


    res.json(data);
  } catch (err) {
    console.error("Fehler bei der Datenabfrage:", err);
    res.status(500).json({ error: "Fehler bei der Datenabfrage" });
  }
});

// start server on port 3000
app.listen(PORT, () => {
  console.log(`Server läuft auf http://localhost:${PORT}`);
});
