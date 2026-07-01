import React, { useState } from "react";
import { Alert, Button, Paper, Stack, Typography } from "@mui/material";

const LabApi = () => {
  const [result, setResult] = useState<string>("No request yet.");

  const checkHealth = async () => {
    try {
      const res = await fetch("/api/server-time");
      const data = await res.json();
      setResult(JSON.stringify(data, null, 2));
    } catch (err) {
      setResult("Request failed.");
    }
  };

  return (
    <Paper variant="outlined" sx={{ p: 2 }}>
      <Stack spacing={2}>
        <Typography variant="subtitle1">API</Typography>
        <Alert severity="info">Use this page for temporary backend checks.</Alert>
        <Button variant="contained" onClick={checkHealth}>
          Run request
        </Button>
        <Typography component="pre" variant="body2" sx={{ whiteSpace: "pre-wrap", m: 0 }}>
          {result}
        </Typography>
      </Stack>
    </Paper>
  );
};

export default LabApi;
