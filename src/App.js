import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

import { Box } from "@mui/material";
import { ThemeProvider, createTheme } from "@mui/material/styles";
import CssBaseline from "@mui/material/CssBaseline";

import Dashboard from "./pages/Dashboard";
import BalancePage from "./pages/BalancePage";
import TickerPage from "./pages/TickerPage"
import TradeHistory from "./pages/TradeHistory";

import Sidebar from "./components/Sidebar";
import AiTraderPanel from "./components/AiTraderPanel";

const darkTheme = createTheme({
  palette: {
    mode: "dark",
  },
});

const links = [
  { label: "Dashboard", path: "/" },
  { label: "Balance History", path: "/BalancePage" },
  { label: "Ticker", path: "/TickerPage" },
  { label: "Trade History", path: "/TradeHistory" },
];

function App() {
  return (
    <ThemeProvider theme={darkTheme}>
      <CssBaseline />
      <Router>
        <Sidebar links={links} />   {/* ✅ pass it here */}
        <Box sx={{ ml: 30}}>
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/BalancePage" element={<BalancePage />} />
            <Route path="/TickerPage" element={<TickerPage />} />
            <Route path="/TradeHistory" element={<TradeHistory />} />
          </Routes>
          <AiTraderPanel />
        </Box>
      </Router>
    </ThemeProvider>
  );
}


export default App;
