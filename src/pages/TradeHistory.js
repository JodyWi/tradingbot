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

const TradeHistory = () => {
  const [pairs, setPairs] = useState([]);
  const [tradeHistory, setTradeHistory] = useState([]);
  const [selectedPair, setSelectedPair] = useState("");
  const [loading, setLoading] = useState(true);
  // const [view, setView] = useState("latest");

  const fetchHistory = async () => {
    setLoading(true);
    try {
      const data = await fetchFromApi("/api/1/trade/history");
      setTradeHistory(data || []);
    } catch (err) {
      console.error(err);
      setTradeHistory([]);
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

    const handleUpdateTrade = async (pair) => {
    if (!pair) {
      alert("Please select a pair to update.");
      return;
    }
    try {
      const response = await fetch(`/api/1/trade?pair=${pair}`, {
        method: "POST",
      });

      const result = await response.json();
      console.log(result);
      alert(result.message || `Updated Trade Hisrory!`);
    } catch (err) {
      console.error("Update failed:", err);
      alert("Failed to update Trades.");
    }
  };
  return (
    <Box p={4} sx={{ height: 600, width: "100%" }}>
      <Typography variant="h4" gutterBottom>
        Trade History
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
          onClick={() => handleUpdateTrade(selectedPair)}
          disabled={!selectedPair}
        >
          Update Selected (API)
        </Button>
        <Button
          variant="contained"
          color="secondary"
          // onClick={handleUpdateTickers}
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
            {tradeHistory.length === 0 ? (
              <Typography>No data found</Typography>
            ) : (
              tradeHistory.map((pair, i) => (
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
                          Pairs: ${h.pair} |
                          Sequence: ${h.sequence} | 
                          Order id: ${h.order_id} |
                          Type: ${h.type} |
                          Price: ${h.price} |
                          Volume: ${h.volume} |
                          Base: ${h.base} |
                          Counter: ${h.counter} |
                          Fee Base: ${h.fee_base} |
                          Fee Counter: ${h.fee_counter} |
                          Is Buy: ${h.is_buy} |
                          Client Order id: ${h.client_order_id} |
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



export default TradeHistory;
