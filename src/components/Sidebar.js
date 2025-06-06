import React from 'react';
import { NavLink } from 'react-router-dom';

const Sidebar = ({ links }) => {
  return (
    <div className="w-64 h-screen bg-[#1e1e2f] text-white fixed top-0 left-0 shadow-lg z-50 flex flex-col">
      <nav className="sidebar">
      <div className="p-6 border-b border-gray-700">
        <h1 className="text-2xl font-bold text-blue-400">Trading Bot</h1>
      </div>

        {links.map((link, i) => (
          <NavLink
            key={i}
            to={link.path}
            className={({ isActive }) =>
              `px-4 py-2 rounded transition-colors ${
                isActive ? 'bg-blue-600' : 'hover:bg-gray-700'
              }`
            }
          >
            {link.label}
          </NavLink>
        ))}

        <div className="mt-auto p-4 text-xs text-gray-400 border-t border-gray-700">
        JodyWi © 2025 — All Rights Reserved
        </div>
      </nav>
    </div>
  );
};

export default Sidebar;
