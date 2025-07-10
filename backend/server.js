const express = require('express');
const cors = require('cors');
const path = require('path');
const Database = require('better-sqlite3');

// Good: Use path.resolve to get the absolute file path
const tradingbotPath = path.resolve(__dirname, '../database/tradingbot.db');
const financials = path.resolve(__dirname, '../database/financial.db');
const settings = path.resolve(__dirname, '../database/settings.db');
const portfolio = path.resolve(__dirname, '../database/portfolio.db');
const conversation = path.resolve(__dirname, '../database/conversation.db');
const logs = path.resolve(__dirname, '../database/logs.db');
const news = path.resolve(__dirname, '../database/news.db');
const research = path.resolve(__dirname, '../database/research.db');

console.log('Resolved paths:', tradingbotPath, financials);

const tradingbot_db = new Database(tradingbotPath, { readonly: true }); // ✅ CORRECT
const financial_db = new Database(financials, { readonly: true }); // ✅ CORRECT
const settings_db = new Database(settings, {}); // ✅ read/write
// const portfolio_db = new Database(portfolio, { readonly: true }); // ✅ CORRECT
// const conversation_db = new Database(conversation, { readonly: true }); // ✅ CORRECT
// const logs_db = new Database(logs, { readonly: true }); // ✅ CORRECT
// const news_db = new Database(news, { readonly: true }); // ✅ CORRECT
// const research_db = new Database(research, { readonly: true }); // ✅ CORRECT

const app = express();
app.use(cors());


// Fetch ticker_history (limit 1000 latest records)
app.get('/api/1/ticker/history', (req, res) => {
  try {
    const rows = financial_db.prepare('SELECT * FROM ticker_history').all();

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
    const rows = financial_db.prepare('SELECT * FROM balance_history').all();

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

// Fetch trade_history
app.get('/api/1/trade/history', (req, res) => {
  try {
    const rows = financial_db.prepare('SELECT * FROM trade_history').all();
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

// Fetch fee_history
app.get('/api/1/fee/history', (req, res) => {
  try {
    const rows = financial_db.prepare('SELECT * FROM fee_history').all();
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

// Fetch market_history
app.get('/api/1/marketsInfo/history', (req, res) => {
  try {
    const rows = financial_db.prepare('SELECT * FROM market_history').all();
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

// Fetch pairs_list
app.get('/api/1/pairs', (req, res) => {
  try {
    const rows = financial_db.prepare('SELECT * FROM pairs_list').all();
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
    const rows = financial_db.prepare('SELECT * FROM assets_list').all();
    // its inside assets field

    res.json(rows);
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: "Database error" });
  }
});

// Audi_Bot stuff goes here
// ✅ Audi Bot Settings API
app.get('/api/audi_bot/settings', (req, res) => {
  try {
    const rows = settings_db.prepare(`
      SELECT pair, maxTradeSize, riskLevel
      FROM audi_bot_settings
    `).all();

    res.json(rows);
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: "Database error" });
  }
});

app.post('/api/audi_bot/settings', express.json(), (req, res) => {
  const { pair, maxTradeSize, riskLevel } = req.body;

  if (!pair) {
    return res.status(400).json({ error: "'pair' field is required" });
  }

  try {
    settings_db.prepare(`
      CREATE TABLE IF NOT EXISTS audi_bot_settings (
        pair TEXT PRIMARY KEY,
        maxTradeSize REAL,
        riskLevel TEXT
      );
    `).run();

    settings_db.prepare(`
      INSERT OR REPLACE INTO audi_bot_settings (pair, maxTradeSize, riskLevel)
      VALUES (?, ?, ?);
    `).run(pair, maxTradeSize, riskLevel);

    res.json({ message: `Settings saved for pair: ${pair}` });
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: "Database error" });
  }
});

// server.js example
app.get('/api/audi_bot/settings', (req, res) => {
  const pair = req.query.pair;
  if (!pair) return res.status(400).json({ error: "Pair is required" });

  try {
    const row = settings_db.prepare(`
      SELECT * FROM audi_bot_settings WHERE pair = ?
    `).get(pair);

    res.json(row || {});
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: "Database error" });
  }
});




const PORT = 3002;
app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});
