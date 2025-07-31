// src/utils/fetchSettingsHelper.js

import { fetchFromApi } from "./fetchFromApi";

// const BASE_URL_PY = "http://localhost:8001"; // Python server!
const BASE_URL_JS = "http://localhost:3002"; // JavaScript server!
export async function fetchSettings() {


  try {
    const settingsData = `${BASE_URL_JS}/api/app/settings`;
    // const settingsData = await fetchFromApi("/api/app/settings");
    console.log("settingsData", settingsData);
    // console.log("JavaScript url",url_js);
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
