import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

import { Box, Divider } from "@mui/material";
import { ThemeProvider, createTheme } from "@mui/material/styles";
import CssBaseline from "@mui/material/CssBaseline";

import Dashboard from "./pages/Dashboard";
import BalanceHistory from "./pages/BalanceHistory";
import TickerPage from "./pages/TickerPage"
import TradeHistory from "./pages/TradeHistory";
import FeesInfoPage from "./pages/FeesInfoPage";
import MarketsInfoPage from "./pages/MarketsInfoPage";

import ProgrammaticBot from "./pages/ProgrammaticBot";

import Sidebar from "./components/Sidebar";
import AiTraderPanel from "./components/AiTraderPanel";

const darkTheme = createTheme({
  palette: {
    mode: "dark",
  },
});

const links = [
  { label: "Dashboard", path: "/" },
  { label: "Balance History", path: "/BalanceHistory" },
  { label: "Trade History", path: "/TradeHistory" },
  { label: "Ticker", path: "/TickerPage" },
  { label: "Fees Info", path: "/FeesInfoPage" },
  { label: "Markets Info", path: "/MarketsInfoPage" },
  <Divider />,
  { label: "Programmatic Bot", path: "/ProgrammaticBot" },


];

function App() {
  return (
    <ThemeProvider theme={darkTheme}>
      <CssBaseline />
      <Router>
        <Sidebar links={links} />
        <Box sx={{ ml: 30}}>
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/BalanceHistory" element={<BalanceHistory />} />
            <Route path="/TradeHistory" element={<TradeHistory />} />
            <Route path="/TickerPage" element={<TickerPage />} />
            <Route path="/FeesInfoPage" element={<FeesInfoPage />} />
            <Route path="/MarketsInfoPage" element={<MarketsInfoPage />} />
            <Route path="/ProgrammaticBot" element={<ProgrammaticBot />} />
          </Routes>
          <AiTraderPanel />
        </Box>
      </Router>
    </ThemeProvider>
  );
}


export default App;
