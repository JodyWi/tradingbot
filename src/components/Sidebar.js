import React from "react";
import { Link } from "react-router-dom";

const Sidebar = ({ links }) => {
  return (
    <aside className="w-64 bg-gray-800 h-screen p-6 flex flex-col fixed left-0 top-0 shadow-xl">
      <h1 className="text-2xl font-bold text-blue-400 mb-6">Trading Bot</h1>

      {/* Navigation Links */}
      <nav className="flex flex-col space-y-3">
        {links.map((link, index) => (
          <Link
            key={index}
            to={link.path}
            className="flex items-center space-x-3 py-2 px-3 rounded-lg bg-gray-700 hover:bg-blue-500 transition hover:shadow-md"
          >
            <i className={`${link.icon} text-xl text-blue-400`}></i>
            <span className="text-white">{link.label}</span>
          </Link>
        ))}
      </nav>

      {/* Footer */}
      <div className="mt-auto text-gray-500 text-sm">
        JodyWi © 2025 <br />
        All Rights Reserved
      </div>
    </aside>
  );
};

export default Sidebar;
