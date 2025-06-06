import React from "react";
import { Button, Box, Typography } from "@mui/material";
import { useNavigate } from "react-router-dom";

const Dashboard = () => {
  const navigate = useNavigate();

  return (
    <Box display="flex" minHeight="100vh">
      <Box flex={1} p={4}>
        <Typography variant="h4" gutterBottom>
          Dashboard
        </Typography>
      <Box display="flex" gap={2} flexWrap="wrap">
        <Button variant="outlined" onClick={() => navigate("/balances")}>
          Balance
        </Button>
        <Button variant="outlined" onClick={() => navigate("/balanceDb")}>
          Balance in DB
        </Button>
        <Button variant="outlined" onClick={() => navigate("/trading")}>
          Trading
        </Button>
        <Button variant="outlined" onClick={() => navigate("/history")}>
          History
        </Button>
        <Button variant="outlined" onClick={() => navigate("/settings")}>
          Settings
        </Button>
      </Box>
      </Box>
    </Box>
  );
};

export default Dashboard;
