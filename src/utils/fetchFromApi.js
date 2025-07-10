// src/utils/fetchFromApi.js
// import axios from "axios";

export const fetchFromApi = async (endpoint) => {
  const BASE_URL = "http://localhost:3002"; // your Node backend URL + port
  const response = await fetch(BASE_URL + endpoint);
  if (!response.ok) {
    throw new Error("Network response was not ok");
  }
  return response.json();
};

