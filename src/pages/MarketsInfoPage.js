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

const MarketsInfoPage = () => {
  const [pairs, setPairs] = useState([]);
  const [marketsInfoHistory, setMarketsInfoHistory] = useState([]);
  const [selectedPair, setSelectedPair] = useState("");
  const [loading, setLoading] = useState(false);

  const fetchHistory = async () => {
    setLoading(true);
    try {
      const data = await fetchFromApi("/api/1/marketsInfo/history");
      setMarketsInfoHistory(data || []);
    } catch (err) {
      console.error(err);
      setMarketsInfoHistory([]);
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


  const handleUpdateMarketsInfo = async (pair) => {
    if (!pair) {
      alert("Please select a pair to update.");
      return;
    }
    try {
      const response = await fetch(`/api/1/markets_info?pair=${pair}`, {
        method: "POST",
      });

      const result = await response.json();
      console.log(result);
      alert(result.message || `Updated Markets Info!`);
      // fetchAssets(view); // Refresh current view
    } catch (err) {
      console.error("Update failed:", err);
      alert("Failed to update Market Info.");
    }
  };

  return (
    <Box p={4} sx={{ height: 600, width: "100%" }}>
      <Typography variant="h4" gutterBottom>
        Markets Fee History
      </Typography>
      <Divider sx={{ my: 2 }} />

      <Stack direction="row" spacing={2} mb={2}>        
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
          onClick={() => handleUpdateMarketsInfo(selectedPair)}
          disabled={!selectedPair}
        >
          Update Selected (API)
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
            {marketsInfoHistory.length === 0 ? (
              <Typography>No data found</Typography>
            ) : (
              marketsInfoHistory.map((pair, i) => (
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
                          Pair: ${h.market_id} |
                          Base Currency ${h.base_currency} | 
                          Counter Currency: ${h.counter_currency} |
                          Fee Scale: ${h.fee_scale} |
                          Max Price: ${h.max_price} |                          
                          Max Volume: ${h.max_volume} |                          
                          Min Price: ${h.min_price} |                          
                          Min Volume: ${h.min_volume} |                          
                          Price Scale: ${h.price_scale} |                          
                          Trading Status: ${h.trading_status} |                          
                          Volume Scale: ${h.volume_scale} |
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

export default MarketsInfoPage;
