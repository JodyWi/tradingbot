// src/utils/fetchSettingsHelper.js

import { fetchFromApi } from "./fetchFromApi";

export async function fetchSettings() {
  try {
    const settingsData = await fetchFromApi("/api/app/settings");
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
