import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";

const links = [
  { path: "/", label: "Home" },
  { path: "/dashboard", label: "Dashboard" },
];

const Balances = () => {
    const [balances, setBalances] = useState([]);
    const [assets, setAssets] = useState([]); // List of assets
    const [selectedAsset, setSelectedAsset] = useState(""); 
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    useEffect(() => {
        fetchBalances();
    }, []);

    const fetchBalances = async (asset = "") => {
        setLoading(true);
        setError(null);
        try {
        const response = await fetch(
            `http://localhost:8001/balance${asset ? `?assets=${asset}` : ""}`
        );
        const data = await response.json();
        if (data.balances) {
            setBalances(data.balances);

            // Extract asset list
            const assetList = data.balances.map((b) => b.Asset);
            setAssets([...new Set(assetList)]); // Remove duplicates
        } else {
            setError("Failed to retrieve balances");
        }
        } catch (err) {
        setError("Error fetching balances");
        }
        setLoading(false);
    };
  return (
    <div className="container">
      {/* Sidebar */}
      <nav className="sidebar">
        <h1 className="sidebar-title">Trading Bot</h1>
        <ul className="sidebar-links">
          {links.map((link, index) => (
            <li key={index}>
              <Link to={link.path} className="sidebar-link">
                {link.label}
              </Link>
            </li>
          ))}
        </ul>
      </nav>

      {/* Main Content */}
      <div className="content">
        <h1 className="page-title">Account Balances</h1>

        {/* Dropdown for asset selection */}
        <select
          value={selectedAsset}
          onChange={(e) => setSelectedAsset(e.target.value)}
        >
          <option value="">All Assets</option>
          {assets.map((asset, index) => (
            <option key={index} value={asset}>
              {asset}
            </option>
          ))}
        </select>

        {/* Fetch balances button */}
        <button onClick={() => fetchBalances(selectedAsset)}>Check Balances</button>

        {loading && <p>Loading...</p>}
        {error && <p className="error-message">{error}</p>}

        <ul>
          {balances.map((balance, index) => (
            <li key={index} className="balance-item">
              <span>
                {balance.Asset}: {balance.Balance}
              </span>
              <button onClick={() => fetchBalances(balance.Asset)}>Check</button>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default Balances;
