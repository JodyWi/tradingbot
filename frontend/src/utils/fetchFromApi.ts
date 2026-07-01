export const fetchFromApi = async (endpoint: string) => {
  const BASE_URL = import.meta.env.VITE_API_BASE || "";
  const response = await fetch(BASE_URL + endpoint);
  if (!response.ok) {
    throw new Error("Network response was not ok");
  }
  return response.json();
};
