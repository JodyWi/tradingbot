// src/utils/TradesHelper.js

import { fetchFromApi } from "./fetchFromApi.js";

export async function functionGetAllTrades() {
  try {
    console.log("⏳ Starting trade info fetch...");
    // 1) Fetch all pairs dynamically
    const pairsData = await fetchFromApi("/api/1/pairs");
    if (!pairsData || !Array.isArray(pairsData)) {
      console.error("❌ No pairs found");
      return;
    }
    // console.log(`🔍 ${pairsData.length} pairs to fetch Trades for.`);
    // 2) Loop through all pairs and fetch trade info
    for (const pairObj of pairsData) {
      const pair = pairObj.pair || pairObj.name || pairObj.pairs;
      if (!pair) continue;
      try {
        const response = await fetch(`/api/1/trade?pair=${pair}`, {
          method: "POST",
        });
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
        // const result = await response.json();
        // console.log(`✅ Fetched trade for ${pair}:`, result);
      } catch (err) {
        console.error(`❌ Error fetching trade info for ${pair}:`, err);
      }
      // Small delay to avoid hammering the API
      await new Promise(resolve => setTimeout(resolve, 500));
    }
    console.log("🎉 All Trades fetched and stored!");
  } catch (err) {
    console.error("❌ Fatal error:", err);
  }
}


// src/utils/TradesHelper.js is works
export async function fetchAllTradesTest() {
  try {
    const pairs = ["XBTZAR", "ETHZAR"]; // example — you'd have all 137 pairs!
    for (const pair of pairs) {
      const res = await fetch(`/api/1/trade?pair=${pair}`, {
        method: "POST",
      });
      const data = await res.json();
      console.log(`✅ Fetched trade for ${pair}:`, data);
    }
  } catch (err) {
    console.error("❌ Error fetching Trades:", err);
  }
}


// TradesHelper.js
export async function saveTradesSettings(TradesSetting) {
  try {
    const payload = {
      autoFetch: TradesSetting.autoFetchOn, // rename key to match backend!
      autoFetchTime: TradesSetting.targetTime, // rename key to match backend!
    };

    const response = await fetch("/api/app/settings/savetradeinfo", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload), // no nested "Tradesinfo" key now
    });

    const result = await response.json();
    if (result.error) {
      console.error("Save error:", result.error);
      return false;
    } else {
      alert("Settings saved!");
      return true;
    }
  } catch (err) {
    console.error("Save settings failed:", err);
    return false;
  }
}

// TradesHelper.js

export async function fetchTradesSettings() {
  try {
    const settingsData = await fetchFromApi("/api/app/settings/gettradeinfo");
    // console.log("settingsData", settingsData);
    if (!settingsData) {
      console.error("❌ No settings found");
      return null;
    }
    return settingsData; // no need to wrap or index
  } catch (error) {
    console.error("Failed to fetch trade info settings:", error);
    return null;
  }
}
