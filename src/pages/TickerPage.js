import React, { useState, useEffect } from "react";
import {
  Box,
  Button,
  Typography,
  Stack,
  CircularProgress,
} from "@mui/material";
import { DataGrid } from "@mui/x-data-grid";
import { useNavigate } from "react-router-dom";

const TickerPage = () => {
  const navigate = useNavigate();
  const [assets, setAssets] = useState([]);
  const [columns, setColumns] = useState([]);
  const [loading, setLoading] = useState(false);

  const fetchAssets = async () => {
    setLoading(true);
    try {
      const res = await fetch("http://localhost:8001/assets"); // <-- your backend API
      const data = await res.json();

      if (Array.isArray(data) && data.length > 0) {
        const rowsWithId = data.map((item, index) => ({
          id: index,
          ...item,
        }));

        // Dynamically generate columns from object keys
        const dynamicColumns = Object.keys(data[0]).map((key) => ({
          field: key,
          headerName: key.replace(/_/g, " ").replace(/\b\w/g, l => l.toUpperCase()), // Pretty formatting
          flex: 1,
        }));

        setAssets(rowsWithId);
        setColumns(dynamicColumns);
      } else {
        setAssets([]);
        setColumns([]);
      }
    } catch (error) {
      console.error("Failed to fetch assets:", error);
    }
    setLoading(false);
  };

  useEffect(() => {
    fetchAssets();
  }, []);

  return (
    <Box p={4}>
      <Typography variant="h4" gutterBottom>
        Trading Assets
      </Typography>

      <Stack direction="row" spacing={2} mb={2}>
        <Button variant="outlined" onClick={() => navigate("/")}>
          Dashboard
        </Button>
      </Stack>

      {loading ? (
        <CircularProgress />
      ) : (
        <DataGrid
          rows={assets}
          columns={columns}
          autoHeight
          disableRowSelectionOnClick
        />
      )}

        <Stack direction="row" spacing={2} mb={2}>
        <Button variant="contained" onClick={fetchAssets}>
          Refresh Assets
        </Button>
      </Stack>
    </Box>
  );
};

export default TickerPage;
