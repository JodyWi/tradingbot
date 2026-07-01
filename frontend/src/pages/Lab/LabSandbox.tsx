import React from "react";
import { Box, Button, Paper, Stack, TextField, Typography } from "@mui/material";

const LabSandbox = () => {
  return (
    <Paper variant="outlined" sx={{ p: 2 }}>
      <Stack spacing={2}>
        <Typography variant="subtitle1">Sandbox</Typography>
        <Typography variant="body2" color="text.secondary">
          Use this page to test layouts, spacing, and quick UI ideas.
        </Typography>
        <TextField label="Scratch input" defaultValue="Experiment here" />
        <Box>
          <Button variant="contained" sx={{ mr: 1 }}>
            Primary
          </Button>
          <Button variant="outlined">Secondary</Button>
        </Box>
      </Stack>
    </Paper>
  );
};

export default LabSandbox;
