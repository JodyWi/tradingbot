import React, { useState, useEffect } from "react";
import {
  Box,
  Button,
  Typography,
  Stack,
  CircularProgress,
  Divider,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
} from "@mui/material";
import { SimpleTreeView, TreeItem } from "@mui/x-tree-view";
import { fetchFromApi } from "../utils/fetchFromApi";

const TickerPage = () => {
  const [pairs, setPairs] = useState([]);
  const [tickerHistory, setTickerHistory] = useState([]);
  const [selectedPair, setSelectedPair] = useState("");
  const [loading, setLoading] = useState(false);
  const [view, setView] = useState("latest"); // "latest" or "history"

  const fetchHistory = async () => {
    setLoading(true);
    try {
      const data = await fetchFromApi("/api/1/ticker/history");
      setTickerHistory(data || []);
    } catch (err) {
      console.error(err);
      setTickerHistory([]);
    }
    setLoading(false);
  };

  useEffect(() => {
    fetchHistory();
  }, []);

  useEffect(() => {
    let isMounted = true; // Optional safety

    const fetchPairList = async () => {
      try {
        const data = await fetchFromApi("/api/1/pairs");
        if (isMounted) {
          setPairs(data || []);
        }
      } catch (err) {
        console.error(err);
        if (isMounted) setPairs([]);
      }
    };

    fetchPairList();

    return () => {
      isMounted = false; // Clean up if component unmounts
    };
  }, []);


  const handleUpdateTicker = async (pair) => {
    if (!pair) {
      alert("Please select a pair to update.");
      return;
    }
    try {
      const response = await fetch(`/api/1/ticker?pair=${pair}`, {
        method: "POST",
      });

      const result = await response.json();
      console.log(result);
      alert(result.message || `Updated tickers!`);
      // fetchAssets(view); // Refresh current view
    } catch (err) {
      console.error("Update failed:", err);
      alert("Failed to update tickers.");
    }
  };
  const handleUpdateTickers = async () => {
    try {
      const response = await fetch("/api/1/tickers", {
        method: "POST",
      });

      const result = await response.json();
      console.log(result);
      alert(result.message || `Updated ${result.count} tickers!`);
      // fetchAssets(view); // Refresh current view
    } catch (err) {
      console.error("Update failed:", err);
      alert("Failed to update tickers.");
    }
  };

  return (
    <Box p={4} sx={{ height: 600, width: "100%" }}>
      <Typography variant="h4" gutterBottom>
        Ticker Pairs - {view === "latest" ? "Latest" : "History"}
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

        <FormControl sx={{ minWidth: 200, mr: 2 }}>
          <InputLabel>Pair</InputLabel>
          <Select
            value={selectedPair}
            label="Asset"
            onChange={(e) => setSelectedPair(e.target.value)}
          >
            <MenuItem value="">All Pairs</MenuItem>
              {pairs.map((pair, index) => (
                <MenuItem key={index} value={pair.pairs}>
                  {pair.pairs}
                </MenuItem>
              ))}

          </Select>
        </FormControl>
        <Button
          variant="contained"
          color="secondary"
          onClick={() => handleUpdateTicker(selectedPair)}
          disabled={!selectedPair}
        >
          Update Selected (API)
        </Button>
        <Button
          variant="contained"
          color="secondary"
          onClick={handleUpdateTickers}
        >
          Update All (API)
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
            {tickerHistory.length === 0 ? (
              <Typography>No data found</Typography>
            ) : (
              tickerHistory.map((pair, i) => (
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
                        label={
                          `
                          pair: ${h.pair} |
                          Bid: ${h.bid} | 
                          Ask: ${h.ask} |
                          last_trade: ${h.last_trade} |
                          volume: ${h.volume} |
                          status: ${h.status} |
                          TS: ${new Date(h.timestamp).toLocaleString()} 
                          `
                        }
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
