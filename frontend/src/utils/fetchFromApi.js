// src/utils/fetchFromApi.js

export const fetchFromApi = async (endpoint) => {
  const BASE_URL = process.env.REACT_APP_API_BASE || "http://localhost:8001";
  const response = await fetch(BASE_URL + endpoint);
  if (!response.ok) {
    throw new Error("Network response was not ok");
  }
  return response.json();
};
