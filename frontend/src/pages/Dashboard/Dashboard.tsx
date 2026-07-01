import React, { useEffect, useState } from "react";
import { Box, Typography, Divider, Chip, Stack } from "@mui/material";

type LunoStatus = {
  connected?: boolean;
  configured?: boolean;
  message?: string;
};

const Dashboard = () => {
  const [status, setStatus] = useState<LunoStatus>({});

  useEffect(() => {
    const load = async () => {
      try {
        const res = await fetch("/api/luno/status");
        const data = await res.json();
        setStatus(data);
      } catch (err) {
        setStatus({ connected: false, configured: false, message: "Status unavailable" });
      }
    };
    load();
  }, []);

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
            color={status.connected ? "success" : "default"}
            label={status.connected ? "Luno API: Connected" : "Luno API: Disconnected"}
          />
        </Stack>
      </Box>
    </Box>
  );
};

export default Dashboard;
