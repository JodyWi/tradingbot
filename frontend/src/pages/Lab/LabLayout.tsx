import React from "react";
import { NavLink, Outlet } from "react-router-dom";
import { Box, Stack, Tab, Tabs, Typography } from "@mui/material";

const labTabs = [
  { label: "Overview", path: "/Lab" },
  { label: "Sandbox", path: "/Lab/Sandbox" },
  { label: "API", path: "/Lab/Api" },
  { label: "Charts", path: "/Lab/Charts" },
];

const LabLayout = () => {
  return (
    <Box p={4}>
      <Typography variant="h4" gutterBottom>
        Lab
      </Typography>
      <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
        Workspace for tests, prototypes, and temporary pages.
      </Typography>

      <Tabs value={false} sx={{ mb: 3 }}>
        {labTabs.map((tab) => (
          <Tab
            key={tab.path}
            component={NavLink}
            to={tab.path}
            value={tab.path}
            label={tab.label}
          />
        ))}
      </Tabs>

      <Stack spacing={2}>
        <Outlet />
      </Stack>
    </Box>
  );
};

export default LabLayout;
