import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import GlobalStyle from "./globalStyles"; // ✅ Import Global Styles
import Home from "./pages/Home";  
import Dashboard from "./pages/Dashboard";
import Balances from "./pages/Balances";
import Trades from "./pages/Trades";


function App() {
    return (
        <>
            <GlobalStyle />  {/* ✅ Apply Global Styles */}
            <Router>
                <div style={{ display: "flex", height: "100vh" }}>
                    {/* Routes */}
                    <Routes>
                        <Route path="/" element={<Home />} />  
                        <Route path="/dashboard" element={<Dashboard />} />
                        <Route path="/balances" element={<Balances />} />
                        <Route path="/trades" element={<Trades />} />
                    </Routes>
                </div>
            </Router>
        </>
    );
}

export default App;
