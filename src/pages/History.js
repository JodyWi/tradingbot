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
  Drawer,
  ListItemButton,
} from "@mui/material";
import { useNavigate } from "react-router-dom";
const History = () => {
  const navigate = useNavigate();

  return (
    <Box display="flex" minHeight="100vh">
      {/* Main Content */}
      <Box flex={1} p={4}>
        <Typography variant="h4" gutterBottom>
          History
        </Typography>
        <Stack>
          <Box display="flex" gap={2} flexWrap="wrap">
            <Button variant="outlined" onClick={() => navigate("/")}>
              Dashboard
            </Button>
            <Button variant="outlined" onClick={() => navigate("/balances")}>
              Balance
            </Button>
            <Button variant="outlined" onClick={() => navigate("/trading")}>
              Trading
            </Button>
            <Button variant="outlined" onClick={() => navigate("/settings")}>
              Settings
            </Button>

          </Box>
        </Stack>
      </Box>
    </Box>
  );
};




export default History;
