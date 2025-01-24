const { MongoClient, ServerApiVersion } = require('mongodb');
const fs = require('fs');
const path = require('path');

const uri = "mongodb+srv://minersimon:z9KaSRAinZtuE2zS@cluster0.avuvgqu.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0";

// Create a MongoClient with a MongoClientOptions object to set the Stable API version
const client = new MongoClient(uri, {
  serverApi: {
    version: ServerApiVersion.v1,
    strict: true,
    deprecationErrors: true,
  }
});

async function run() {
  try {
    // Connect the client to the server
    await client.connect();

    // Reference the database and collection
    const database = client.db("test");
    const collection = database.collection("entries");

    // Calculate the last 365 days
    const now = new Date();
    const fourteenDaysAgo = new Date();
    fourteenDaysAgo.setDate(now.getDate() - 365);

    // Find all entries for the last 365 days
    const entries = await collection
      .find({ date: { $gte: fourteenDaysAgo.getTime() } }) // Query for entries from the last 14 days
      .sort({ date: -1 })
      .toArray();

    // Group entries by day
    const groupedEntries = entries.reduce((groups, entry) => {
      const date = new Date(entry.date);
      const dayKey = date.toISOString().split('T')[0]; // Get YYYY-MM-DD format
      if (!groups[dayKey]) {
        groups[dayKey] = [];
      }
      groups[dayKey].push(entry);
      return groups;
    }, {});

    // Directory to save files
    const outputDir = "C:\\Users\\simon\\Desktop\\CGM+\\dataCollection";
    if (!fs.existsSync(outputDir)) {
      fs.mkdirSync(outputDir, { recursive: true });
    }

    // Write each day's entries to a file
    for (const [day, dayEntries] of Object.entries(groupedEntries)) {
      const filePath = path.join(outputDir, `${day}.txt`);
      const fileContent = JSON.stringify(dayEntries, null, 2);
      fs.writeFileSync(filePath, fileContent, 'utf8');
      console.log(`Saved ${dayEntries.length} entries to ${filePath}`);
    }

    console.log("All files have been created!");

  } catch (err) {
    console.error("An error occurred:", err);
  } finally {
    // Ensures that the client will close when you finish/error
    await client.close();
  }
}

run().catch(console.dir);