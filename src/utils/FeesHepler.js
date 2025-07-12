// src/utils/FeesHelper.js

import { fetchFromApi } from "./fetchFromApi";

export async function fetchAllFeesInfo() {
  try {
    console.log("⏳ Starting fee info fetch...");
    // 1) Fetch all pairs dynamically
    const pairsData = await fetchFromApi("/api/1/pairs");
    if (!pairsData || !Array.isArray(pairsData)) {
      console.error("❌ No pairs found");
      return;
    }
    // console.log(`🔍 ${pairsData.length} pairs to fetch fees for.`);
    // 2) Loop through all pairs and fetch fee info
    for (const pairObj of pairsData) {
      const pair = pairObj.pair || pairObj.name || pairObj.pairs;
      if (!pair) continue;
      try {
        const response = await fetch(`/api/1/fee_info?pair=${pair}`, {
          method: "POST",
        });
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
        // const result = await response.json();
        // console.log(`✅ Fetched fee for ${pair}:`, result);
      } catch (err) {
        console.error(`❌ Error fetching fee info for ${pair}:`, err);
      }
      // Small delay to avoid hammering the API
      await new Promise(resolve => setTimeout(resolve, 500));
    }
    console.log("🎉 All fees fetched and stored!");
  } catch (err) {
    console.error("❌ Fatal error:", err);
  }
}


// src/utils/FeesHelper.js is works
export async function fetchAllFeesTest() {
  try {
    const pairs = ["XBTZAR", "ETHZAR"]; // example — you'd have all 137 pairs!
    for (const pair of pairs) {
      const res = await fetch(`/api/1/fee_info?pair=${pair}`, {
        method: "POST",
      });
      const data = await res.json();
      console.log(`✅ Fetched fee for ${pair}:`, data);
    }
  } catch (err) {
    console.error("❌ Error fetching fees:", err);
  }
}


// FeesHelper.js
export async function saveFeesInfoSettings(feesSetting) {
  try {
    const payload = {
      autoFetch: feesSetting.autoFetchOn, // rename key to match backend!
      autoFetchTime: feesSetting.targetTime, // rename key to match backend!
    };

    const response = await fetch("/api/app/settings/savefeeinfo", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload), // no nested "feesinfo" key now
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

// FeesHelper.js

export async function fetchFeesInfoSettings() {
  try {
    const settingsData = await fetchFromApi("/api/app/settings/getfeeinfo");
    // console.log("settingsData", settingsData);
    if (!settingsData) {
      console.error("❌ No settings found");
      return null;
    }
    return settingsData; // no need to wrap or index
  } catch (error) {
    console.error("Failed to fetch fee info settings:", error);
    return null;
  }
}
