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

const FeesInfoPage = () => {
  const [pairs, setPairs] = useState([]);
  const [feeHistory, setFeeHistory] = useState([]);
  const [selectedPair, setSelectedPair] = useState("");
  const [loading, setLoading] = useState(false);

  const fetchHistory = async () => {
    setLoading(true);
    try {
      const data = await fetchFromApi("/api/1/fee/history");
      setFeeHistory(data || []);
    } catch (err) {
      console.error(err);
      setFeeHistory([]);
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


  const handleUpdateFee = async (pair) => {
    if (!pair) {
      alert("Please select a pair to update.");
      return;
    }
    try {
      const response = await fetch(`/api/1/fee_info?pair=${pair}`, {
        method: "POST",
      });

      const result = await response.json();
      console.log(result);
      alert(result.message || `Updated Fees!`);
      // fetchAssets(view); // Refresh current view
    } catch (err) {
      console.error("Update failed:", err);
      alert("Failed to update fees.");
    }
  };

  return (
    <Box p={4} sx={{ height: 600, width: "100%" }}>
      <Typography variant="h4" gutterBottom>
        Fees History
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
          onClick={() => handleUpdateFee(selectedPair)}
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
            {feeHistory.length === 0 ? (
              <Typography>No data found</Typography>
            ) : (
              feeHistory.map((pair, i) => (
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
                          Pair: ${h.pair} |
                          Maker Fee: ${h.maker_fee} | 
                          Taker Fee: ${h.taker_fee} |
                          Thirty Day Volume: ${h.thirty_day_volume} |
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

export default FeesInfoPage;
