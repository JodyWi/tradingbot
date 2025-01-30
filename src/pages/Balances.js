import React, { useEffect, useState } from "react";

function Balances() {
    const [balance, setBalance] = useState(null);

    useEffect(() => {
        fetch("http://localhost:8001/balance")
            .then(response => response.json())
            .then(data => setBalance(data.balance))
            .catch(error => console.error("Error fetching balance:", error));
    }, []);

    return (
        <div>
            <h2>Balance Page</h2>
            <p>Current Balance: {balance !== null ? `${balance} USD` : "Loading..."}</p>
        </div>
    );
}

export default Balances;
