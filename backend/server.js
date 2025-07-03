const express = require('express');
const Database = require('better-sqlite3');
const cors = require('cors');
const path = '/home/ubuntu/projects/tradingbot/database/tradingbot.db';

const app = express();
app.use(cors());

const db = new Database(path, { readonly: true }); // Open DB read-only

// Fetch ticker_history (limit 1000 latest records)
app.get('/api/1/tickers/history', (req, res) => {
  try {
    const rows = db.prepare('SELECT * FROM ticker_history').all();

    // Group by pair
    const grouped = rows.reduce((acc, row) => {
      if (!acc[row.pair]) {
        acc[row.pair] = { pair: row.pair, history: [] };
      }
      acc[row.pair].history.push(row);
      return acc;
    }, {});

    res.json(Object.values(grouped));
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: "Database error" });
  }
});

// Fetch balance_history
app.get('/api/1/balance/history', (req, res) => {
  try {
    const rows = db.prepare('SELECT * FROM balance_history').all();

    // Group by asset
    const grouped = rows.reduce((acc, row) => {
      if (!acc[row.asset]) {
        acc[row.asset] = { asset: row.asset, history: [] };
      }
      acc[row.asset].history.push(row);
      return acc;
    })
    res.json(Object.values(grouped));
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: "Database error" });
  }
});


// Fetch pairs_list
app.get('/api/1/pairs', (req, res) => {
  try {
    const rows = db.prepare('SELECT * FROM pairs_list').all();
    // its inside pairs field
    res.json(rows);
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: "Database error" });
  }
});

// Fetch assets_list
app.get('/api/1/assets', (req, res) => {
  try {
    const rows = db.prepare('SELECT * FROM assets_list').all();
    // its inside assets field

    res.json(rows);
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: "Database error" });
  }
});


const PORT = 3002;
app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});
