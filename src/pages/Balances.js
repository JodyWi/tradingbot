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
  Drawer,
  ListItemButton,
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


      {/* Main Content */}
      <Box flex={1} p={4}>
        <Typography variant="h4" gutterBottom>
          Account Balances
        </Typography>
        
        <Stack>

        <Box display="flex" gap={2} flexWrap="wrap">
          <Button variant="outlined" onClick={() => navigate("/")}>
            Dashboard
          </Button>
          <Button variant="outlined" onClick={() => navigate("/trading")}>
            Trading
          </Button>
          <Button variant="outlined" onClick={() => navigate("/history")}>
            History
          </Button>
          <Button variant="outlined" onClick={() => navigate("/settings")}>
            Settings
          </Button>
        </Box>
</Stack>

<Divider sx={{ my: 2, color: "white" }} />

<Stack>
{/* iwant the db todisplay here */}
{/* can you improve the spacing too */}

{/* lets just render what in the db */}
<Stack>
        {/* Dropdown */}
        <FormControl >
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

        <Button variant="contained" onClick={() => fetchBalances(selectedAsset)} sx={{ ml: 2 }}>
          Check Balances
        </Button>

        {/* Feedback */}
        <Box mt={2}>
          {loading && <CircularProgress />}
          {error && <Typography color="error">{error}</Typography>}
        </Box>

        {/* Balance List */}
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
      </Stack>
      </Stack>
      </Box>
    </Box>
  );
};

export default Balances;
