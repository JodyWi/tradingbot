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

const BalancePage = () => {
  const [balances, setBalances] = useState([]);
  const [assets, setAssets] = useState([]);
  const [selectedAsset, setSelectedAsset] = useState("");
  const [view, setView] = useState("latest");
  const [loading, setLoading] = useState(false);

  const fetchBalances = async () => {
    setLoading(true);
    try {
      const data = await fetchFromApi("/api/1/balance/history");
      setBalances(data || []);
    } catch (err) {
      console.error(err);
      setBalances([]);
    }
    setLoading(false);
  };

  useEffect(() => {
    fetchBalances();
  }, []);


useEffect(() => {
  let isMounted = true;

  const fetchAssetsList = async () => {
    try {
      const data = await fetchFromApi("/api/1/assets");
      if (isMounted) {
        setAssets(data || []);
      }
    } catch (err) {
      console.error(err);
      if (isMounted) setAssets([]);
    }
  };

  fetchAssetsList();

  return () => {
    isMounted = false;
  };
}, []);

  // handleUpdatebalance
  const handleUpdatebalance = async (asset) => {
    if (!asset) {
      alert("Please select an asset to update.");
      return;
    }
    try {
      const response = await fetch(`/api/1/balance?assets=${asset}`, {
        method: "POST",
      });
      const result = await response.json();
      console.log(result);
      alert(result.message || `Updated ${result.count} balance!`);
    } catch (err) {
      console.error("Update failed:", err);
      alert("Failed to update balance.");
    }
  };

  // handleUpdatebalances
  const handleUpdatebalances = async () => {
    try {
      const response = await fetch("/api/1/balances", {
        method: "POST",
      });

      const result = await response.json();
      console.log(result);
      alert(result.message || `Updated ${result.count} balance!`);
      // fetchAssets(view); // Refresh current view
    } catch (err) {
      console.error("Update failed:", err);
      alert("Failed to update balance.");
    }
  };

  return (
    <Box p={4} sx={{ height: 600, width: "100%" }}>
      <Typography variant="h4" gutterBottom>
        Balance History - {view === "latest" ? "Latest" : "History"}
      </Typography>
      <Divider sx={{ my: 2 }} />

      <Stack direction="row" spacing={2} mb={2}>

        <Button
          variant={view === "latest" ? "contained" : "outlined"}
          onClick={() => setView("latest")}
        >
          Latest Balance
        </Button>
        
        <Button
          variant={view === "history" ? "contained" : "outlined"}
          onClick={() => setView("history")}
        >
          Balance History
        </Button>
        
        <FormControl sx={{ minWidth: 200, mr: 2 }}>
          <InputLabel>Asset</InputLabel>
          <Select
            value={selectedAsset}
            label="Asset"
            onChange={(e) => setSelectedAsset(e.target.value)}
          >
            <MenuItem value="">All Assets</MenuItem>
            {assets.map((asset, index) => (
              <MenuItem key={index} value={asset.assets}>
                {asset.assets}
              </MenuItem>
            ))}
          </Select>
        </FormControl>

        <Button
          variant="contained"
          color="secondary"
          onClick={() => handleUpdatebalance(selectedAsset)}
          disabled={!selectedAsset}
        >
          Update Selected (API)
        </Button>

        <Button
          variant="contained"
          color="secondary"
          onClick={handleUpdatebalances}
        >
          Update All (API)
        </Button>

      </Stack>
      <Box
        sx={{
          maxHeight: 500, 
          overflowY: "auto", 
          border: "1px solid #ddd", 
          p: 2, 
        }}
      >
        {loading ? (
          <CircularProgress />
        ) : balances.length === 0 ? (
          <Typography>No data found</Typography>
        ) : (
          <SimpleTreeView>
            {balances
              .filter((asset) => asset.asset) // Skip rows with empty asset
              .map((asset, i) => (
                <TreeItem
                  key={asset.asset || i}
                  itemId={asset.asset || `${i}`}
                  label={asset.asset}
                >
                  {asset.history && asset.history.length > 0 ? (
                    asset.history.map((h, j) => (
                      <TreeItem
                        key={`${asset.asset}-${j}`}
                        itemId={`${asset.asset}-${j}`}
                        label={
                          `
                          Balance: ${h.balance} | 
                          Reserved: ${h.reserved} | 
                          Unconfirmed: ${h.unconfirmed} | 
                          TS: ${new Date(h.timestamp).toLocaleString()}
                          `
                        }
                        sx={{
                        border: "1px solid #ddd", 
                        }}
                      />
                    ))
                  ) : (
                    <TreeItem
                      key={`${asset.asset}-empty`}
                      itemId={`${asset.asset}-empty`}
                      label="No history"
                    />
                  )}
                </TreeItem>
              ))}
          </SimpleTreeView>
        )}
      </Box>
    </Box>
  );
};

export default BalancePage;
