import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

import { Box } from "@mui/material";
import { ThemeProvider, createTheme } from "@mui/material/styles";
import CssBaseline from "@mui/material/CssBaseline";

import Dashboard from "./pages/Dashboard/Dashboard";
import BalanceHistory from "./pages/History/BalanceHistory";
import TickerPage from "./pages/Info/TickerPage";
import TradeHistory from "./pages/History/TradeHistory";
import FeesInfoPage from "./pages/Info/FeesInfoPage";
import MarketsInfoPage from "./pages/Info/MarketsInfoPage";

import ProgrammaticBot from "./pages/Bot/ProgrammaticBot";
import LabLayout from "./pages/Lab/LabLayout";
import LabOverview from "./pages/Lab/LabOverview";
import LabSandbox from "./pages/Lab/LabSandbox";
import LabApi from "./pages/Lab/LabApi";
import LabCharts from "./pages/Lab/LabCharts";

import SettingPage from "./pages/Settings/SettingsPage";

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
  { label: "Programmatic Bot", path: "/ProgrammaticBot" },
  { label: "Lab", path: "/Lab" },

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
            <Route path="/Lab" element={<LabLayout />}>
              <Route index element={<LabOverview />} />
              <Route path="Sandbox" element={<LabSandbox />} />
              <Route path="Api" element={<LabApi />} />
              <Route path="Charts" element={<LabCharts />} />
            </Route>
            <Route path="/Settings" element={<SettingPage />} />
          </Routes>
          <AiTraderPanel />
        </Box>
      </Router>
    </ThemeProvider>
  );
}


export default App;
