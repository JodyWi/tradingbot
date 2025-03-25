import React from "react";
import { Link } from "react-router-dom";

const links = [
  { path: "/", label: "Home" },
  { path:"/balances", label: "Balance"},
  { path: "/trading", label: "Trading" },
  { path: "/settings", label: "Settings" },
  { path: "/history", label: "History" },
];

const Dashboard = () => {
  return (
    <div className="container">
      {/* Sidebar */}
      <nav className="sidebar">
        <h1>Trading Bot</h1>
        {links.map((link, index) => (
          <Link key={index} to={link.path}>
            {link.label}
          </Link>
        ))}
      </nav>

      {/* Main Content */}
      <div className="content">
        <h2>Dashboard Overview</h2>
        <div className="stat-container">
          <div className="stat-box">
            <p className="stat-label">Balance</p>
            <h3 className="stat-value">$?</h3>
          </div>
          <div className="stat-box">
            <p className="stat-label">Open Trades</p>
            <h3 className="stat-value">?</h3>
          </div>
          <div className="stat-box">
            <p className="stat-label">Profit/Loss</p>
            <h3 className="stat-value">+?%</h3>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
