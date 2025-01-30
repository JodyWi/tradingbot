import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";

const links = [
  { path: "/", label: "Home" },
  { path: "/dashboard", label: "Dashboard" },
];

const Balances = () => {
  const [balances, setBalances] = useState([]);
  const [assets, setAssets] = useState([]);
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
      const response = await fetch(`http://localhost:8001/balance${asset ? `?assets=${asset}` : ""}`);
      const data = await response.json();

      if (data.balances && data.balances.balances && Array.isArray(data.balances.balances)) {
        const fetchedBalances = data.balances.balances.map((b) => ({
          asset: b.asset,
          balance: parseFloat(b.balance), // Ensure balance is a number
        }));

        setBalances(fetchedBalances);
        setAssets([...new Set(fetchedBalances.map((b) => b.asset))]); // Unique asset list
      } else {
        setBalances([]);
        setError("No balances found.");
      }
    } catch (err) {
      setError("Error fetching balances");
      setBalances([]);
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
        <select value={selectedAsset} onChange={(e) => setSelectedAsset(e.target.value)}>
          <option value="">All Assets</option>
          {assets.map((asset, index) => (
            <option key={index} value={asset}>
              {asset}
            </option>
          ))}
        </select>

        {/* Fetch Balances Button */}
        <button onClick={() => fetchBalances(selectedAsset)}>Check Balances</button>

        {loading && <p>Loading...</p>}
        {error && <p className="error-message">{error}</p>}

        {balances.length > 0 ? (
          <ul>
            {balances.map((balance, index) => (
              <li key={index} className="balance-item">
                <span>
                  {balance.asset}: {balance.balance.toFixed(8)}
                </span>
                <button onClick={() => fetchBalances(balance.asset)}>Check</button>
              </li>
            ))}
          </ul>
        ) : (
          <p>No balances available.</p>
        )}
      </div>
    </div>
  );
};

export default Balances;
