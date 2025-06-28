import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

import GlobalStyle from "./globalStyles"; // ✅ Import Global Styles
import { ThemeProvider, createTheme } from "@mui/material/styles";
import CssBaseline from "@mui/material/CssBaseline";


import AiTraderPanel from "./components/AiTraderPanel";

import Dashboard from "./pages/Dashboard";
import Balances from "./pages/Balances";
import TickerPage from "./pages/TickerPage"
import TradeHistory from "./pages/TradeHistory";


const darkTheme = createTheme({
  palette: {
    mode: "dark",
  },
});

// is there a way to get like darkmode at the start at my App.js
function App() {
    return (
        <>
        <ThemeProvider theme={darkTheme}>
            <CssBaseline /> {/* Makes sure the background is correct */}
            {/* <GlobalStyle />  ✅ Apply Global Styles */}
            <Router>
                    {/* <div style={{ display: "flex", height: "100vh" }}> */}
                    {/* Routes */}
                    <Routes>
                        <Route path="/" element={<Dashboard />} />
                        <Route path="/balances" element={<Balances />} />
                        <Route path="/TickerPage" element={<TickerPage />} />
                        <Route path="/TradeHistory" element={<TradeHistory />} />
                    </Routes>
                    {/* </div> */}
                    <AiTraderPanel /> {/* 👈 This makes it visible everywhere */}
            </Router>
        </ThemeProvider>
        </>
    );
}

export default App;
