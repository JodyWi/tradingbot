import React, { useEffect, useState } from "react";
import {
  Box,
  Typography,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  List,
  ListItem,
  ListItemText,
  CircularProgress,
  Paper,
  Stack,
  Button,
  Divider,
} from "@mui/material";
import { useNavigate } from "react-router-dom";

const BalanceDb = () => {
  const navigate = useNavigate();
  const [balances, setBalances] = useState([]);
  const [filtered, setFiltered] = useState([]);
  const [assets, setAssets] = useState([]);
  const [selectedAsset, setSelectedAsset] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

useEffect(() => {
  const loadBalances = async () => {
    try {
      const response = await fetch("http://localhost:3001/api/balances");
      const data = await response.json();

      setBalances(data);
      setFiltered(data);
      setAssets([...new Set(data.map((b) => b.asset))]);
    } catch (err) {
      console.error("Error loading balances.json", err);
      setError("Failed to load balances");
    } finally {
      setLoading(false);
    }
  };

  loadBalances();
}, []);


  const handleFilter = (asset) => {
    setSelectedAsset(asset);
    if (asset === "") {
      setFiltered(balances);
    } else {
      setFiltered(balances.filter((b) => b.asset === asset));
    }
  };

  return (
    <Box p={4}>
      <Typography variant="h4" gutterBottom>
        Local DB Balances
      </Typography>

      {/* Navigation */}
      <Stack direction="row" spacing={2} mb={3}>
        <Button variant="outlined" onClick={() => navigate("/")}>Dashboard</Button>
        <Button variant="outlined" onClick={() => navigate("/trading")}>Trading</Button>
        <Button variant="outlined" onClick={() => navigate("/history")}>History</Button>
        <Button variant="outlined" onClick={() => navigate("/settings")}>Settings</Button>
      </Stack>

      <Divider sx={{ mb: 3 }} />

      {/* button to load data function  exportBalances */}


      <Button
        variant="contained"
        color="primary"
        onClick={async () => {
          try {
            const res = await fetch("/api/export-balances", { method: "POST" });
            const result = await res.json();
            if (result.success) {
              alert("✅ Balances exported!");
              window.location.reload(); // reload to re-fetch balances.json
            } else {
              throw new Error(result.error);
            }
          } catch (err) {
            console.error(err);
            alert("❌ Failed to export balances");
          }
        }}
      >
        Export Balances
      </Button>



      {loading ? (
        <CircularProgress />
      ) : error ? (
        <Typography color="error">{error}</Typography>
      ) : (
        <>
          {/* Filter Dropdown */}
          <Stack direction="row" spacing={2} alignItems="center" mb={2}>
            <FormControl sx={{ minWidth: 200 }}>
              <InputLabel>Asset</InputLabel>
              <Select
                value={selectedAsset}
                label="Asset"
                onChange={(e) => handleFilter(e.target.value)}
              >
                <MenuItem value="">All Assets</MenuItem>
                {assets.map((asset, idx) => (
                  <MenuItem key={idx} value={asset}>{asset}</MenuItem>
                ))}
              </Select>
            </FormControl>
          </Stack>

          {/* Balance List */}
          <Paper elevation={3} sx={{ p: 2 }}>
            <List>
              {filtered.map((balance, index) => (
                <ListItem key={index}>
                  <ListItemText
                    primary={`${balance.asset}: ${parseFloat(balance.balance).toFixed(8)}`}
                    secondary={`Timestamp: ${balance.timestamp || "N/A"}`}
                  />
                </ListItem>
              ))}
            </List>
          </Paper>
        </>
      )}
    </Box>
  );
};

export default BalanceDb;
