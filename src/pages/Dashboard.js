import React from "react";
import { Box, Typography, Divider } from "@mui/material";

const Dashboard = () => {
  return (
    <Box display="flex" minHeight="100vh">
            <Box flex={1} p={4}>
        <Typography variant="h4" gutterBottom>
          Dashboard
        </Typography>
        <Divider sx={{ my: 2 }} />
        <Typography variant="body1">
          Welcome to your Trading Bot Dashboard!
        </Typography>

        {/* Add widgets, charts, or stats here later */}
        </Box>
    </Box>
  );
};

export default Dashboard;
