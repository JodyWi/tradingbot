import React, { useState, useEffect } from "react";
import {
  Box,
  Typography,
  Button,
  Select,
  Stack,
  MenuItem,
  FormControl,
  InputLabel,
  CircularProgress,
  List,
  ListItem,
  ListItemText,
  Divider,
} from "@mui/material";
import { useNavigate } from "react-router-dom";

const Balances = () => {
  const navigate = useNavigate();
  const [balances, setBalances] = useState([]);
  const [assets, setAssets] = useState([]);
  const [selectedAsset, setSelectedAsset] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchBalances();
  }, []);

  const fetchBalances = async (asset = "") => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch(`http://localhost:8001/balance${asset ? `?assets=${asset}` : ""}`);
      const data = await response.json();

      if (data.balances && data.balances.balances && Array.isArray(data.balances.balances)) {
        const fetchedBalances = data.balances.balances.map((b) => ({
          asset: b.asset,
          balance: parseFloat(b.balance),
        }));

        setBalances(fetchedBalances);
        setAssets([...new Set(fetchedBalances.map((b) => b.asset))]);
      } else {
        setBalances([]);
        setError("No balances found.");
      }
    } catch (err) {
      setError("Error fetching balances");
      setBalances([]);
    }
    setLoading(false);
  };

  return (
    <Box display="flex" minHeight="100vh">
      <Box flex={1} p={4}>
        <Typography variant="h4" gutterBottom>
          Account Balances
        </Typography>

        <Stack direction="row" spacing={2} mb={2}>
          <Button variant="outlined" onClick={() => navigate("/")}>
            Dashboard
          </Button>
        </Stack>

        <Divider sx={{ my: 2 }} />

        <FormControl sx={{ minWidth: 200, mr: 2 }}>
          <InputLabel>Asset</InputLabel>
          <Select
            value={selectedAsset}
            label="Asset"
            onChange={(e) => setSelectedAsset(e.target.value)}
          >
            <MenuItem value="">All Assets</MenuItem>
            {assets.map((asset, index) => (
              <MenuItem key={index} value={asset}>
                {asset}
              </MenuItem>
            ))}
          </Select>
        </FormControl>

        <Button variant="contained" onClick={() => fetchBalances(selectedAsset)}>
          Check Balances
        </Button>

        <Box mt={2}>
          {loading && <CircularProgress />}
          {error && <Typography color="error">{error}</Typography>}
        </Box>

        <List sx={{ mt: 2 }}>
          {balances.map((balance, index) => (
            <ListItem
              key={index}
              secondaryAction={
                <Button
                  variant="outlined"
                  size="small"
                  onClick={() => fetchBalances(balance.asset)}
                >
                  Check
                </Button>
              }
            >
              <ListItemText
                primary={`${balance.asset}: ${balance.balance.toFixed(8)}`}
              />
            </ListItem>
          ))}
        </List>
      </Box>
    </Box>
  );
};

export default Balances;
