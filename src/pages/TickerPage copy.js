import React, { useState, useEffect } from "react";
import {
  Box,
  Button,
  Typography,
  Stack,
  CircularProgress,
  Divider,
} from "@mui/material";
import { DataGrid } from "@mui/x-data-grid";
import { fetchFromApi } from "../utils/fetchFromApi";

const TickerPage = () => {
    const [pairs, setPairs] = useState([]);
  const [assets, setAssets] = useState([]);
  const [loading, setLoading] = useState(false);
  const [view, setView] = useState("latest"); // "latest" or "history"

  const columns = [
    { field: "pair", headerName: "Pair", flex: 1 },
    { field: "timestamp", headerName: "Timestamp", flex: 1 },
    { field: "bid", headerName: "Bid", flex: 1 },
    { field: "ask", headerName: "Ask", flex: 1 },
    { field: "last_trade", headerName: "Last Trade", flex: 1 },
    { field: "volume", headerName: "Volume", flex: 1 },
    { field: "status", headerName: "Status", flex: 1 },
  ];

  const fetchAssets = async (type = "latest") => {
    setLoading(true);
    try {
      const data = await fetchFromApi(`/api/1/tickers/${type}`);
      setAssets(data || []);
    } catch (error) {
      console.error("Failed to fetch assets:", error);
      setAssets([]);
    }
    setLoading(false);
  };

  useEffect(() => {
    fetchAssets(view);
  }, [view]);

  const handleUpdateTickers = async () => {
    try {
      const response = await fetch("/api/1/tickers/update", {
        method: "POST",
      });

      const result = await response.json();
      console.log(result);
      alert(result.message || `Updated ${result.count} tickers!`);
      fetchAssets(view); // Refresh current view
    } catch (err) {
      console.error("Update failed:", err);
      alert("Failed to update tickers.");
    }
  };
  const fetchPairs = async () => {
    setLoading(true);
    try {
      const data = await fetchFromApi("/api/1/tickers/history");
      setPairs(data || []);
    } catch (err) {
      console.error(err);
      setPairs([]);
    }
    setLoading(false);
  };

  useEffect(() => {
    fetchPairs();
  }, []);
  return (
    <Box p={4} sx={{ height: 600, width: "100%" }}>
      <Typography variant="h4" gutterBottom>
        Trading Assets - {view === "latest" ? "Latest" : "History"}
      </Typography>
      <Divider sx={{ my: 2 }} />

      <Stack direction="row" spacing={2} mb={2}>
        <Button
          variant={view === "latest" ? "contained" : "outlined"}
          onClick={() => setView("latest")}
        >
          Latest Tickers
        </Button>
        <Button
          variant={view === "history" ? "contained" : "outlined"}
          onClick={() => setView("history")}
        >
          Ticker History
        </Button>
        <Button
          variant="contained"
          color="secondary"
          onClick={handleUpdateTickers}
        >
          Update Tickers (API)
        </Button>
      </Stack>

      {loading ? (
        <CircularProgress />
      ) : (
<DataGrid
  rows={(view === "latest" ? assets : pairs).map((row, i) => ({
    id: row.id || row.pair || i,
    pair: row.pair,
    timestamp: row.timestamp,
    bid: row.bid,
    ask: row.ask,
    last_trade: row.last_trade,
    volume: row.volume,
    status: row.status,
  }))}
  columns={columns}
/>

      )}
    </Box>
  );
};

export default TickerPage;
