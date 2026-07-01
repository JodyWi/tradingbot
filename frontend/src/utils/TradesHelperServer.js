// src/utils/TradesHelperServer.js

const { fetchFromApi } = require('./fetchFromApiServer');
const fetch = (...args) => import('node-fetch').then(({default: fetch}) => fetch(...args));
const BASE_URL_PY = "http://localhost:8001"; // Python server!

async function functionGetAllTrades() {
  try {
    console.log("⏳ Starting trade info fetch...");
    // 1) Fetch all pairs dynamically
    const pairsData = await fetchFromApi("/api/1/pairs");
    if (!pairsData || !Array.isArray(pairsData)) {
      console.error("❌ No pairs found");
      return;
    }

    for (const pairObj of pairsData) {
      const pair = pairObj.pair || pairObj.name || pairObj.pairs;
      if (!pair) continue;

      try {
        const url_py = `${BASE_URL_PY}/api/1/trade?pair=${pair}`;
        const res = await fetch(url_py, { method: "POST" });
        if (!res.ok) {
          console.error(`❌ Failed for ${pair}:`, res.statusText);
          continue;
        }
        console.log(`✅ Fetched trade for ${pair}`);
      } catch (err) {
        console.error(`❌ Error fetching trade for ${pair}:`, err);
      }
      await new Promise(resolve => setTimeout(resolve, 500));
    }
    console.log("🎉 All trades fetched and stored!");
  } catch (err) {
    console.error("❌ Fatal error:", err);
  }
}

// functionGetAllTradesTest is works
// async function functionGetAllTradesTest() {
//   try {
//     const pairs = ["XBTZAR", "ETHZAR"];

//     for (const pair of pairs) {
//       const url_py = `${BASE_URL_PY}/api/1/trade?pair=${pair}`;
//       console.log(`🔗 Fetching: ${url_py}`);

//       const res = await fetch(url_py, { method: "POST" });

//       if (!res.ok) {
//         console.error(`❌ Failed for ${pair}:`, res.statusText);
//         continue;
//       }

//       const data = await res.json();
//       console.log(`✅ Fetched trade for ${pair}:`, data);

//       await new Promise(r => setTimeout(r, 300));
//     }

//     console.log("🎉 All test trades fetched!");
//   } catch (err) {
//     console.error("❌ Error fetching trades:", err);
//   }
// }

// ✅ Export both in a single statement
module.exports = {
  functionGetAllTrades,
  //functionGetAllTradesTest
};

