// src/utils/MarketsHelper.js

import { fetchFromApi } from "./fetchFromApi.js";

export async function functionGetAllMarketsInfo() {
  try {
    console.log("⏳ Starting market info fetch...");
    // 1) Fetch all pairs dynamically
    const pairsData = await fetchFromApi("/api/1/pairs");
    if (!pairsData || !Array.isArray(pairsData)) {
      console.error("❌ No pairs found");
      return;
    }
    // console.log(`🔍 ${pairsData.length} pairs to fetch Markets for.`);
    // 2) Loop through all pairs and fetch market info
    for (const pairObj of pairsData) {
      const pair = pairObj.pair || pairObj.name || pairObj.pairs;
      if (!pair) continue;
      try {
        const response = await fetch(`/api/1/market_info?pair=${pair}`, {
          method: "POST",
        });
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
        // const result = await response.json();
        // console.log(`✅ Fetched market for ${pair}:`, result);
      } catch (err) {
        console.error(`❌ Error fetching market info for ${pair}:`, err);
      }
      // Small delay to avoid hammering the API
      await new Promise(resolve => setTimeout(resolve, 500));
    }
    console.log("🎉 All Markets fetched and stored!");
  } catch (err) {
    console.error("❌ Fatal error:", err);
  }
}


// src/utils/MarketsHelper.js is works
export async function fetchAllMarketsInfoTest() {
  try {
    const pairs = ["XBTZAR", "ETHZAR"]; // example — you'd have all 137 pairs!
    for (const pair of pairs) {
      const res = await fetch(`/api/1/market_info?pair=${pair}`, {
        method: "POST",
      });
      const data = await res.json();
      console.log(`✅ Fetched market for ${pair}:`, data);
    }
  } catch (err) {
    console.error("❌ Error fetching Markets:", err);
  }
}


// MarketsHelper.js
export async function saveMarketsInfoSettings(MarketsInfoSetting) {
  try {
    const payload = {
      autoFetch: MarketsInfoSetting.autoFetchOn, // rename key to match backend!
      autoFetchTime: MarketsInfoSetting.targetTime, // rename key to match backend!
    };

    const response = await fetch("/api/app/settings/savemarketinfo", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload), // no nested "Marketsinfo" key now
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

// MarketsHelper.js

export async function fetchMarketsInfoSettings() {
  try {
    const settingsData = await fetchFromApi("/api/app/settings/getmarketinfo");
    // console.log("settingsData", settingsData);
    if (!settingsData) {
      console.error("❌ No settings found");
      return null;
    }
    return settingsData; // no need to wrap or index
  } catch (error) {
    console.error("Failed to fetch market info settings:", error);
    return null;
  }
}
