// scripts/exportBalances.js

const fs = require("fs");
const path = require("path");
const sqlite3 = require("sqlite3").verbose();

const dbPath = path.resolve(__dirname, "../database/tradingbot.db");
const outputPath = path.resolve(__dirname, '../database/data/balances.json');

function exportBalances() {
  return new Promise((resolve, reject) => {
    const db = new sqlite3.Database(dbPath, sqlite3.OPEN_READONLY, (err) => {
      if (err) return reject(err);
    });

    db.all("SELECT * FROM balances", [], (err, rows) => {
      if (err) {
        db.close();
        return reject(err);
      }

      fs.writeFileSync(outputPath, JSON.stringify(rows, null, 2));
      console.log(`✅ Exported ${rows.length} balances to balances.json`);
      db.close();
      resolve();
    });
  });
}

module.exports = exportBalances;
