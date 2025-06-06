import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import GlobalStyle from "./globalStyles"; // ✅ Import Global Styles

import Dashboard from "./pages/Dashboard";
import Balances from "./pages/Balances";
import BalanceDb from "./pages/BalanceDb"
import Trading from "./pages/Trades";
import History from "./pages/History";


function App() {
    return (
        <>
            <GlobalStyle />  {/* ✅ Apply Global Styles */}
            <Router>
                <div style={{ display: "flex", height: "100vh" }}>
                    {/* Routes */}
                    <Routes>

                        <Route path="/" element={<Dashboard />} />
                        <Route path="/balances" element={<Balances />} />
                        <Route path="/balanceDb" element={<BalanceDb />} />
                        <Route path="/trading" element={<Trading />} />
                        <Route path="/history" element={<History />} />

                    </Routes>
                </div>
            </Router>
        </>
    );
}

export default App;
