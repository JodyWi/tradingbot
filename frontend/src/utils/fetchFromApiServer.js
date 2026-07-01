// src/utils/fetchFromApiServer.js

const fetch = (...args) =>
  import('node-fetch').then(({default: fetch}) => fetch(...args));

const BASE_URL = process.env.AUTOLUNO_API_BASE || "http://localhost:8001";

const fetchFromApi = async (endpoint) => {
  const response = await fetch(BASE_URL + endpoint);
  if (!response.ok) {
    throw new Error("Network response was not ok");
  }
  return response.json();
};

module.exports = { fetchFromApi };
