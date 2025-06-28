import React, { useState, useEffect } from "react";
import {
  Box,
  Button,
  Typography,
  Stack,
  CircularProgress,
  Divider,
} from "@mui/material";

const TradeHistory = () => {

  return (
    <Box p={4}>
      <Typography variant="h4" gutterBottom>
        Trade History
      </Typography>
        <Divider sx={{ my: 2 }} />
    </Box>
  );
};

export default TradeHistory;
