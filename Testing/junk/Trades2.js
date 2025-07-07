import React, { useEffect, useState } from "react";

function Trades() {
    const [trades, setTrades] = useState([]);

    useEffect(() => {
        fetch("http://localhost:8001/trades")
            .then(response => response.json())
            .then(data => setTrades(data.trades))
            .catch(error => console.error("Error fetching trades:", error));
    }, []);

    return (
        <div>
            <h2>Trade History</h2>
            {trades.length > 0 ? (
                <table border="1" style={{ margin: "0 auto" }}>
                    <thead>
                        <tr>
                            <th>Timestamp</th>
                            <th>Asset</th>
                            <th>Type</th>
                            <th>Amount</th>
                            <th>Price</th>
                        </tr>
                    </thead>
                    <tbody>
                        {trades.map((trade, index) => (
                            <tr key={index}>
                                <td>{trade.timestamp}</td>
                                <td>{trade.asset}</td>
                                <td>{trade.trade_type}</td>
                                <td>{trade.amount}</td>
                                <td>{trade.price}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            ) : (
                <p>No trades yet...</p>
            )}
        </div>
    );
}

export default Trades;
