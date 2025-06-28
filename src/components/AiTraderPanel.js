// src/components/AiTraderPanel.js
import React, { useState } from "react";
import {
  Box,
  Typography,
  TextField,
  Button,
  Drawer,
  IconButton
} from "@mui/material";
import ChatIcon from "@mui/icons-material/Chat";

const AiTraderPanel = () => {
  const [open, setOpen] = useState(false);
  const [query, setQuery] = useState("");
  const [response, setResponse] = useState("");

  const handleAskAi = async () => {
    // Placeholder for AI logic
    const mockResponse = `🤖 AI Suggests: HOLD your position on ${query.toUpperCase()}`;
    setResponse(mockResponse);
  };

  return (
    <>
      <IconButton
        sx={{
          position: "fixed",
          bottom: 20,
          right: 20,
          backgroundColor: "#1976d2",
          color: "#fff",
          zIndex: 1300,
          "&:hover": { backgroundColor: "#115293" },
        }}
        onClick={() => setOpen(true)}
      >
        <ChatIcon />
      </IconButton>

      <Drawer
        anchor="right"
        open={open}
        onClose={() => setOpen(false)}
        PaperProps={{ sx: { width: 320, p: 2 } }}
      >
        <Typography variant="h6" gutterBottom>
          AI Trader
        </Typography>

        <TextField
          label="Ask AI..."
          fullWidth
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          sx={{ mb: 2 }}
        />
        <Button fullWidth variant="contained" onClick={handleAskAi}>
          Ask
        </Button>

        {response && (
          <Box mt={3}>
            <Typography variant="subtitle2">AI Response:</Typography>
            <Typography>{response}</Typography>
          </Box>
        )}
      </Drawer>
    </>
  );
};

export default AiTraderPanel;
