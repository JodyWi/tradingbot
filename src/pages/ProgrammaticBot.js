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
import { fetchFromApi } from "../utils/fetchFromApi";

const ProgrammaticBot = () => {
  const [settings, setSettings] = useState({});
  const [pairs, setPairs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [botStatus, setBotStatus] = useState("Stopped");
  const [selectedPair, setSelectedPair] = useState("");  // For selected pair

  const [currentPairSettings, setCurrentPairSettings] = useState({});


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

  const handleSaveSettings = async () => {
    try {
      const res = await fetch("/api/audi_bot/settings", {
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
onChange={async (e) => {
  const newPair = e.target.value;
  setSelectedPair(newPair);

  // Clear form fields for new pair
  setSettings({
    pair: newPair,
    maxTradeSize: "",
    riskLevel: ""
  });

  // Fetch current saved settings for this pair
  try {
    const data = await fetchFromApi(`/api/audi_bot/settings?pair=${newPair}`);
    console.log("Fetched pair settings:", data);  // 🔑 Add this
    setCurrentPairSettings(data || {});
  } catch (err) {
    console.error(err);
    setCurrentPairSettings({});
  }
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

          <TextField
            label="Max Trade Size"
            type="number"
            fullWidth
            margin="normal"
            value={settings.maxTradeSize || ""}
            onChange={(e) => setSettings({ ...settings, maxTradeSize: e.target.value })}
          />

          <FormControl fullWidth margin="normal">
            <InputLabel>Risk Level</InputLabel>
            <Select
              value={settings.riskLevel || ""}
              label="Risk Level"
              onChange={(e) => setSettings({ ...settings, riskLevel: e.target.value })}
            >
              <MenuItem value="low">Low</MenuItem>
              <MenuItem value="medium">Medium</MenuItem>
              <MenuItem value="high">High</MenuItem>
            </Select>
          </FormControl>
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
      </Stack>

      <Button variant="contained" fullWidth sx={{ mt: 3 }} onClick={handleSaveSettings}>
        Save Settings
      </Button>

      {/* displaty current settings for the pair from  */}
      {currentPairSettings && Object.keys(currentPairSettings).length > 0 && (
        <Typography variant="subtitle1" gutterBottom>
          Current Settings:
          <ul>
            {Object.entries(currentPairSettings).map(([key, value]) => (
              <li key={key}>
                <strong>{key}:</strong> {value?.toString() || "-"}
              </li>
            ))}
          </ul>
        </Typography>
      )}

    </Box>
  );
};

export default ProgrammaticBot;
