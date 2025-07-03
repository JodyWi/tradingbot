const express = require('express');
const Database = require('better-sqlite3');
const cors = require('cors');
const path = '/home/ubuntu/projects/tradingbot/database/tradingbot.db';

const app = express();
app.use(cors());

const db = new Database(path, { readonly: true }); // Open DB read-only

// 1) Latest tickers snapshot
app.get('/api/1/tickers/latest', (req, res) => {
  try {
    const rows = db.prepare(`
      SELECT pair, timestamp, bid, ask, last_trade, volume, status 
      FROM tickers
    `).all();
    res.json(rows);
  } catch (err) {
    console.error('DB error (latest):', err);
    res.status(500).json({ error: 'Database error' });
  }
});

// 2) Full ticker history (limit 1000 latest records)
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

// 3) Trigger update tickers (POST)
app.post('/api/1/tickers/update', (req, res) => {
  try {
    // You can call your Python API or the update_tickers function here.
    // For example, if you want to call the Python API you could use child_process or an HTTP request.
    // Here we'll just respond with a placeholder:
    res.json({ status: 'success', message: 'Ticker update triggered' });
  } catch (err) {
    console.error('Update error:', err);
    res.status(500).json({ error: 'Update failed' });
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





const PORT = 3002;
app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});
