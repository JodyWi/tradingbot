import React, { useState, useEffect } from "react";
import {
  Box,
  Button,
  Typography,
  Stack,
  Divider,
  TextField,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
} from "@mui/material";
import CircularProgress from "@mui/material/CircularProgress";

import { Card, CardContent } from "@mui/material";
import { fetchFromApi } from "../utils/fetchFromApi";
import Chart from "../components/Chart";
const ProgrammaticBot = () => {
  const [settings, setSettings] = useState({});
  const [botStatus, setBotStatus] = useState("Stopped");
  
  const [pairs, setPairs] = useState([]);
  const [selectedPair, setSelectedPair] = useState("");  // For selected pair

  // const [currentPairSettings, setCurrentPairSettings] = useState({});
  const [tickerHistory, setTickerHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [chartData, setChartData] = useState([]);

  
  // Fetch pair list
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

  // Fetch settings for that pair whenever selectedPair changes
  useEffect(() => {
    if (!selectedPair) return;

    const fetchCurrentPairSettings = async () => {
      try {
        const data = await fetchFromApi(`/api/audi_bot/settings/${selectedPair}`);
        setSettings({
          pair: selectedPair,
          maxTradeSize: data?.maxTradeSize || "",
          riskLevel: data?.riskLevel || ""
        });
      } catch (err) {
        console.error(err);
        setSettings({
          pair: selectedPair,
          maxTradeSize: "",
          riskLevel: ""
        });
      }
    };

    fetchCurrentPairSettings();
  }, [selectedPair]);


  // you can use this with the chart data 
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
    if (!tickerHistory || tickerHistory.length === 0 || !selectedPair) return;

    // 1️⃣ Find the selected pair's data
    const pairData = tickerHistory.find(item => item.pair === selectedPair);

    if (!pairData || !pairData.history || pairData.history.length === 0) {
      console.warn("No history for selected pair");
      return;
    }
    // 2️⃣ Labels: timestamp -> HH:MM:SS
    const labels = pairData.history.map(item => {
      return item.timestamp ? item.timestamp.slice(11, 19) : "N/A";
    });

    // 3️⃣ Data points: last_trade -> number
    const prices = pairData.history.map(item => {
      const value = parseFloat(item.last_trade);
      return isNaN(value) ? null : value;
    });

    // 4️⃣ Set chart data
    setChartData({
      labels: labels,
      datasets: [
        {
          label: `${selectedPair} Last Trade`,
          data: prices,
          borderColor: "rgb(75, 192, 192)",
          backgroundColor: "rgba(75, 192, 192, 0.2)",
          tension: 0.1
        }
      ]
    });
  }, [tickerHistory, selectedPair]);

  useEffect(() => {
    if (!selectedPair) return;

  setLoading(true);
  // mimic async chart data prep
  setTimeout(() => setLoading(false), 500);
}, [selectedPair]);

  const handleUpdateTickers = async () => {
    try {
      const response = await fetch("/api/1/tickers", {
        method: "POST",
      });

      const result = await response.json();
      console.log(result);
      // alert(result.message || `Updated ${result.count} tickers!`);
      // fetchAssets(view); 
      // Refresh the chart too
      fetchHistory();

    } catch (err) {
      console.error("Update failed:", err);
      alert("Failed to update tickers.");
    }
  };

  const handleSaveSettings = async () => {
    try {
      const res = await fetch("/api/audi_bot/settings/save", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(settings),
      });
      const result = await res.json();
      alert(result.message || "Settings saved");
    } catch (e) {
      alert("Failed to save settings");
      console.error(e);
    }
  };

  const handleClearSettings = async () => {
    try {
      const res = await fetch("/api/audi_bot/settings/clear", {
        method: "DELETE",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(settings),
      });
      const result = await res.json();
      alert(result.message || "Settings cleared");
      // update the settings state
      setSettings({});
    } catch (e) {
      alert("Failed to clear settings");
      console.error(e);
    }
  };

  const handleStartBot = async () => {
    try {
      await fetch("/api/audi_bot/start", { method: "POST" });
      setBotStatus("Running");
    } catch (e) {
      alert("Failed to start bot");
    }
  };

  const handleStopBot = async () => {
    try {
      await fetch("/api/audi_bot/stop", { method: "POST" });
      setBotStatus("Stopped");
    } catch (e) {
      alert("Failed to stop bot");
    }
  };

  return (
    <Box p={4}>
      <Typography variant="h4" gutterBottom>
        Programmatic Audi Bot
      </Typography>
      <Divider sx={{ mb: 3 }} />

      <FormControl fullWidth margin="normal">
        <InputLabel>Trading Pair</InputLabel>
        <Select
          value={selectedPair}
          label="Trading Pair"
          onChange={(e) => {
            const newPair = e.target.value;
            setSelectedPair(newPair);
          }}
        >
          {pairs.map((p, i) => (
            <MenuItem key={i} value={p.pairs}>
              {p.pairs}
            </MenuItem>
          ))}
        </Select>
      </FormControl>
      {selectedPair && (
        <>
          {/* Dynamic Settings Based on Selected Pair */}
          <Typography variant="subtitle1" gutterBottom>
            Selected Pair: <strong>{selectedPair}</strong>
          </Typography>

          <Stack direction="row" spacing={2} mb={3}>
            <TextField
              label="Max Trade Size"
              type="number"
              fullWidth
              value={settings.maxTradeSize || ""}
              onChange={(e) =>
                setSettings({ ...settings, maxTradeSize: e.target.value })
              }
            />

            <FormControl fullWidth>
              <InputLabel>Risk Level</InputLabel>
              <Select
                value={settings.riskLevel || ""}
                label="Risk Level"
                onChange={(e) =>
                  setSettings({ ...settings, riskLevel: e.target.value })
                }
              >
                <MenuItem value="low">Low</MenuItem>
                <MenuItem value="medium">Medium</MenuItem>
                <MenuItem value="high">High</MenuItem>
              </Select>
            </FormControl>
          </Stack>
        </>
      )}

      {/* Bot Control Buttons */}
      <Stack direction="row" spacing={2} mb={3}>
        <Button variant="contained" disabled={botStatus === "Running"} onClick={handleStartBot}>
          Start Bot
        </Button>
        <Button variant="outlined" disabled={botStatus === "Stopped"} onClick={handleStopBot}>
          Stop Bot
        </Button>
        <Button variant="contained" onClick={handleSaveSettings}>
          Save Settings
        </Button>
        <Button variant="contained" onClick={handleClearSettings}>
          Clear Settings
        </Button>
      </Stack>
      {/* display current settings for the pair from  */}
      <Stack direction={{ xs: "column", md: "row" }} spacing={4}>
        {/* Left Side: Form */}
        <Box flex={1}>
          {/* Your Form Fields Here */}
          {settings && Object.keys(settings).length > 0 && (
            <Card variant="outlined" sx={{ mt: 2 }}>
              <CardContent>
                <Typography variant="subtitle1" gutterBottom>
                  Current Settings:
                </Typography>
                <Stack spacing={1}>
                  <Typography variant="body2">
                    <strong>Pair:</strong> {settings.pair || "N/A"}
                  </Typography>
                  <Typography variant="body2">
                    <strong>Max Trade Size:</strong> {settings.maxTradeSize || "N/A"}
                  </Typography>
                  <Typography variant="body2">
                    <strong>Risk Level:</strong> {settings.riskLevel || "N/A"}
                  </Typography>
                </Stack>
              </CardContent>
            </Card>
          )}
        </Box>

        {/* Right Side: Graphs / Info */}
        <Box flex={1}>
          {/* Add your charts, logs, metrics */}
          {loading ? (
            <Box display="flex" justifyContent="center" alignItems="center" height={300}>
              <CircularProgress />
            </Box>
          ) : (
            <Chart pair={selectedPair} data={chartData} />
          )}
          <Button variant="outlined" onClick={handleUpdateTickers}>
            Refresh History
          </Button>

        </Box>
      </Stack>
    </Box>
  );
};

export default ProgrammaticBot;
