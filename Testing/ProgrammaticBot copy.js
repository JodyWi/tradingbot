import React, { useState, useEffect } from "react";
import {
  Box,
  Button,
  Typography,
  Stack,
  CircularProgress,
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

  // useEffect(() => {
  //   const fetchSettings = async () => {
  //     setLoading(true);
  //     try {
  //       const data = await fetchFromApi("/api/audi_bot/settings");
  //       setSettings(data || {});
  //     } catch (e) {
  //       console.error(e);
  //     }
  //     setLoading(false);
  //   };

  //   const fetchStatus = async () => {
  //     try {
  //       const statusRes = await fetchFromApi("/api/audi_bot/status");
  //       setBotStatus(statusRes.status || "Stopped");
  //     } catch (e) {
  //       console.error(e);
  //     }
  //   };

  //   fetchSettings();
  //   fetchStatus();
  // }, []);

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

  // if (loading) return <CircularProgress />;

  return (
    <Box 
      p={4} 
      // sx={{ maxWidth: 600 }}
    >
      <Typography variant="h4" gutterBottom>
        Programmatic Audi Bot
      </Typography>
      <Divider sx={{ mb: 3 }} />

      <Typography variant="subtitle1" gutterBottom>
        Status: <strong>{botStatus}</strong>
      </Typography>

      <Stack direction="row" spacing={2} mb={3}>
        <Button 
          variant="contained" 
          // onClick={handleStartBot} 
          disabled={botStatus === "Running"}>
          Start Bot
        </Button>
        <Button 
          variant="outlined" 
          // onClick={handleStopBot} 
          disabled={botStatus === "Stopped"}>
          Stop Bot
        </Button>
      </Stack>

      <Typography variant="h6" gutterBottom>
        Settings
      </Typography>

      <FormControl fullWidth margin="normal">
        <InputLabel>Trading Pair</InputLabel>
        <Select
          value={settings.pair || ""}
          label="Trading Pair"
          onChange={(e) => setSettings({ ...settings, pair: e.target.value })}
        >
          {pairs.map((p, i) => (
            <MenuItem key={i} value={p.pairs}>
              {p.pairs}
            </MenuItem>
          ))}
        </Select>
      </FormControl>


      <TextField
        label="Max Trade Size"
        type="number"
        fullWidth
        margin="normal"
        //value={settings.maxTradeSize || ""}
        //onChange={(e) => setSettings({ ...settings, maxTradeSize: e.target.value })}
      />

      <FormControl fullWidth margin="normal">
        <InputLabel>Risk Level</InputLabel>
        <Select
          value={settings.riskLevel || ""}
          label="Risk Level"
          //onChange={(e) => setSettings({ ...settings, riskLevel: e.target.value })}
        >
          <MenuItem value="low">Low</MenuItem>
          <MenuItem value="medium">Medium</MenuItem>
          <MenuItem value="high">High</MenuItem>
        </Select>
      </FormControl>

      <Button 
        variant="contained" 
        fullWidth sx={{ mt: 3 }} 
        // onClick={handleSaveSettings}
      >
        Save Settings
      </Button>
    </Box>
  );
};

export default ProgrammaticBot;
