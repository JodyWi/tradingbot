import React from "react";
import { Alert, Box, Paper, Typography } from "@mui/material";

const LabOverview = () => {
  return (
    <Box>
      <Alert severity="info" sx={{ mb: 2 }}>
        Use this area for throwaway UI, API checks, and feature tests.
      </Alert>
      <Paper variant="outlined" sx={{ p: 2 }}>
        <Typography variant="subtitle1" gutterBottom>
          What belongs here
        </Typography>
        <Typography variant="body2" color="text.secondary">
          Temporary components, mocked data, integration checks, and test pages
          that are not part of the core workflow.
        </Typography>
      </Paper>
    </Box>
  );
};

export default LabOverview;
