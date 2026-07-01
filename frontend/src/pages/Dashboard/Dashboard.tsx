import React, { useEffect, useState } from "react";
import { Box, Typography, Divider, Chip, Stack, Paper } from "@mui/material";
import { fetchFromApi } from "../../utils/fetchFromApi";

type LunoStatus = {
  connected?: boolean;
  configured?: boolean;
  message?: string;
};

type LiveTicker = {
  pair?: string;
  bid?: string;
  ask?: string;
  last_trade?: string;
  status?: string;
  timestamp?: string;
};

const STATUS_REFRESH_MS = 30_000;
const LIVE_PAIR = "XBTZAR";

const Dashboard = () => {
  const [status, setStatus] = useState<LunoStatus | null>(null);
  const [ticker, setTicker] = useState<LiveTicker | null>(null);

  useEffect(() => {
    let active = true;

    const loadStatus = async () => {
      try {
        const statusData = await fetchFromApi("/api/luno/status");
        if (active) {
          setStatus(statusData);
        }
      } catch (err) {
        if (active) {
          setStatus({ connected: false, configured: false, message: "Status unavailable" });
        }
      }
    };

    const loadTicker = async () => {
      try {
        const tickerData = await fetchFromApi(`/api/luno/live/ticker?pair=${LIVE_PAIR}`);
        if (active) {
          setTicker(tickerData);
        }
      } catch (err) {
        if (active) {
          setTicker(null);
        }
      }
    };

    loadStatus();
    loadTicker();
    const interval = window.setInterval(() => {
      loadStatus();
      loadTicker();
    }, STATUS_REFRESH_MS);

    return () => {
      active = false;
      window.clearInterval(interval);
    };
  }, []);

  const chipLabel = status === null ? "Luno API: Checking..." : status.connected ? "Luno API: Connected" : "Luno API: Disconnected";
  const chipColor = status === null ? "default" : status.connected ? "success" : "default";

  return (
    <Box display="flex" minHeight="100vh">
      <Box flex={1} p={4}>
        <Typography variant="h4" gutterBottom>
          Dashboard
        </Typography>
        <Divider sx={{ my: 2 }} />
        <Stack direction="row" spacing={2} alignItems="center">
          <Typography variant="body1">
            Welcome to your Trading Bot Dashboard!
          </Typography>
          <Chip
            size="small"
            color={chipColor}
            label={chipLabel}
          />
        </Stack>
        <Paper variant="outlined" sx={{ mt: 3, p: 2 }}>
          <Typography variant="subtitle2" gutterBottom>
            Live Ticker
          </Typography>
          <Typography variant="body2" color="text.secondary">
            {ticker ? `${ticker.pair} bid ${ticker.bid} ask ${ticker.ask} last ${ticker.last_trade}` : "Checking live market data..."}
          </Typography>
        </Paper>
      </Box>
    </Box>
  );
};

export default Dashboard;
