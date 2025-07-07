import React, { useEffect, useState } from 'react';

const BalanceHistory = () => {
  const [balances, setBalances] = useState([]);

  useEffect(() => {
    fetch('http://localhost:8001/api/balances')
      .then(res => res.json())
      .then(data => {
        if (data.status === 'success') {
          setBalances(data.balances);
        }
      })
      .catch(err => console.error('Error fetching balances:', err));
  }, []);

  return (
    <div className="p-6">
      <h2 className="text-xl font-bold mb-4">💼 Wallet Balances</h2>
      <table className="w-full table-auto border-collapse">
        <thead>
          <tr className="bg-gray-200">
            <th className="border px-4 py-2">Asset</th>
            <th className="border px-4 py-2">Balance</th>
            <th className="border px-4 py-2">Timestamp</th>
          </tr>
        </thead>
        <tbody>
          {balances.map(item => (
            <tr key={item.id} className="text-center">
              <td className="border px-4 py-2">{item.asset}</td>
              <td className="border px-4 py-2">{item.balance}</td>
              <td className="border px-4 py-2">{item.timestamp}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default BalanceHistory;
