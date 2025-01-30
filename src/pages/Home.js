import React from "react";
import { Link } from "react-router-dom";

const links = [
  { path: "/dashboard", label: "Dashboard" },
//   { path: "/trading", label: "Trading" },
//   { path: "/settings", label: "Settings" },
//   { path: "/history", label: "History" },
];

const Home = () => {
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
            <h2>Home</h2>
        </div>    
    </div>
  );
};

export default Home;
