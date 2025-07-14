const express = require('express');
const cors = require('cors');
const path = require('path');
const Database = require('better-sqlite3');

const { feesInfoSmartScheduler } = require('../src/utils/FeesInfoScheduler');

// , functionGetAllFeesTest 
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

const serverStart = Date.now();
console.log(`🚀 Server started at: ${new Date(serverStart).toISOString()}`);

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

// GET a single pair's settings
app.get('/api/audi_bot/settings/:pair', (req, res) => {
  const pair = req.params.pair;

  if (!pair) {
    return res.status(400).json({ error: "'pair' parameter is required" });
  }

  try {
    const row = settings_db.prepare(`
      SELECT pair, maxTradeSize, riskLevel
      FROM audi_bot_settings
      WHERE pair = ?
    `).get(pair);

    if (row) {
      res.json(row);
    } else {
      res.json({ message: `No settings found for pair: ${pair}` });
    }

  } catch (err) {
    console.error("Database error:", err);
    res.status(500).json({ error: "Database error" });
  }
});

// Get Fees Settings working this
app.get("/api/app/settings/getfeeinfo", (req, res) => {
  try {
    const stmt = settings_db.prepare(
      "SELECT autoFetch, autoFetchTime FROM feesinfo_settings WHERE id = ?"
    );
    const row = stmt.get("singleton");

    if (row) {
      res.json({
        autoFetch: !!row.autoFetch, // convert 0/1 to boolean
        autoFetchTime: row.autoFetchTime
      });
    } else {
      res.json({
        autoFetch: false,
        autoFetchTime: "23:00"
      });
    }
  } catch (err) {
    console.error("Error fetching feesinfo_settings:", err);
    res.status(500).json({ error: err.message });
  }
});

// Set time for app
app.get("/api/server-time", (req, res) => {
  res.json({ serverTime: new Date().toISOString() });
});

app.get("/api/health", (req, res) => {
  const uptimeSeconds = Math.floor((Date.now() - serverStart) / 1000);
  res.json({
    status: "ok",
    uptime: `${uptimeSeconds} seconds`,
    serverTime: new Date().toISOString()
  });
});

// Schedulers here

const feesInfoScheduler = feesInfoSmartScheduler(settings_db);
feesInfoScheduler.start();

// Schedulers here

const PORT = 3002;
app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});
