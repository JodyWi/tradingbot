import React, { useEffect, useMemo, useState } from "react";
import {
  Alert,
  Box,
  Button,
  Divider,
  MenuItem,
  Paper,
  Stack,
  TextField,
  Typography,
} from "@mui/material";

type Status = {
  connected?: boolean;
  configured?: boolean;
  apiUrl?: string;
  message?: string;
};

const functions = [
  { key: "ticker", label: "Get ticker", needsPair: true, method: "POST", path: "/api/1/ticker" },
  { key: "tickers", label: "List tickers", needsPair: false, method: "POST", path: "/api/1/tickers" },
  { key: "balance", label: "Get balance", needsPair: false, method: "POST", path: "/api/1/balances" },
  { key: "trade", label: "Get trades", needsPair: true, method: "POST", path: "/api/1/trade" },
  { key: "fee", label: "Get fee info", needsPair: true, method: "POST", path: "/api/1/fee_info" },
  { key: "markets", label: "Get markets info", needsPair: true, method: "POST", path: "/api/1/markets_info" },
];

const LabApi = () => {
  const [status, setStatus] = useState<Status>({});
  const [selected, setSelected] = useState("ticker");
  const [pair, setPair] = useState("XBTZAR");
  const [response, setResponse] = useState("Run a function to inspect the result.");

  const current = useMemo(
    () => functions.find((item) => item.key === selected) ?? functions[0],
    [selected],
  );

  useEffect(() => {
    const loadStatus = async () => {
      try {
        const res = await fetch("/api/luno/status");
        const data = await res.json();
        setStatus(data);
      } catch (err) {
        setStatus({ connected: false, configured: false, message: "Status unavailable." });
      }
    };
    loadStatus();
  }, []);

  const runFunction = async () => {
    const url = current.needsPair ? `${current.path}?pair=${encodeURIComponent(pair)}` : current.path;
    try {
      const res = await fetch(url, { method: current.method });
      const data = await res.json();
      setResponse(JSON.stringify(data, null, 2));
    } catch (err) {
      setResponse("Request failed.");
    }
  };

  return (
    <Box>
      <Stack spacing={2}>
        <Alert severity={status.connected ? "success" : "warning"}>
          {status.message || "Checking Luno API status..."}
        </Alert>

        <Paper variant="outlined" sx={{ p: 2 }}>
          <Stack spacing={2}>
            <Typography variant="subtitle1">Luno Function Tester</Typography>
            <Typography variant="body2" color="text.secondary">
              Use this page to exercise the live backend functions that wrap Luno API calls.
            </Typography>

            <TextField
              select
              label="Function"
              value={selected}
              onChange={(e) => setSelected(e.target.value)}
            >
              {functions.map((item) => (
                <MenuItem key={item.key} value={item.key}>
                  {item.label}
                </MenuItem>
              ))}
            </TextField>

            {current.needsPair && (
              <TextField
                label="Pair"
                value={pair}
                onChange={(e) => setPair(e.target.value)}
              />
            )}

            <Button variant="contained" onClick={runFunction}>
              Run function
            </Button>

            <Divider />

            <Typography component="pre" variant="body2" sx={{ m: 0, whiteSpace: "pre-wrap" }}>
              {response}
            </Typography>
          </Stack>
        </Paper>
      </Stack>
    </Box>
  );
};

export default LabApi;
