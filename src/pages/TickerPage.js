import React, { useState, useEffect } from "react";
import {
  Box,
  Button,
  Typography,
  Stack,
  CircularProgress,
  Divider,
} from "@mui/material";
import { SimpleTreeView, TreeItem } from "@mui/x-tree-view";
import { fetchFromApi } from "../utils/fetchFromApi";

const TickerPage = () => {
  const [pairs, setPairs] = useState([]);
  const [assets, setAssets] = useState([]);
  const [loading, setLoading] = useState(false);
  const [view, setView] = useState("latest"); // "latest" or "history"

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
        <Box
          sx={{
            maxHeight: 500,
            overflowY: "auto",
            border: "1px solid #ddd",
            p: 2, 
          }}
        >
          <SimpleTreeView>
            {pairs.length === 0 ? (
              <Typography>No data found</Typography>
            ) : (
              pairs.map((pair, i) => (
                <TreeItem
                  key={pair.pair || i}
                  itemId={pair.pair || `${i}`}
                  label={pair.pair || `No Pair ${i}`}
                >
                  {pair.history && pair.history.length > 0 ? (
                    pair.history.map((h, j) => (
                      <TreeItem
                        key={`${pair.pair}-${j}`}
                        itemId={`${pair.pair}-${j}`}
                        label={`TS: ${new Date(h.timestamp).toLocaleString()} | Bid: ${h.bid} | Ask: ${h.ask}`}
                      />
                    ))
                  ) : (
                    <TreeItem
                      key={`${pair.pair}-empty`}
                      itemId={`${pair.pair}-empty`}
                      label="No history"
                    />
                  )}
                </TreeItem>
              ))
            )}
          </SimpleTreeView>
        </Box>
      )}
    </Box>
  );
};

export default TickerPage;
