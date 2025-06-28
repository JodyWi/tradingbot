// src/styles/globalStyles.js
import { createGlobalStyle } from "styled-components";

const GlobalStyle = createGlobalStyle`
  /* Global Reset */
  * {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
  }

  body {
    font-family: Arial, sans-serif;
    background: #000;  /* Full black */
    color: #fff;
    height: 100vh;
  }

  a {
    text-decoration: none;
    color: inherit;
  }

  /* Sidebar */
  .sidebar {
    width: 250px;
    background: #1f1f1f;
    padding: 20px;
    display: flex;
    flex-direction: column;
    gap: 15px;
    box-shadow: 2px 0 5px rgba(255, 255, 255, 0.1);
    position: fixed;
    left: 0;
    top: 0;
    bottom: 0;
  }

  .sidebar h1 {
    font-size: 1.5rem;
    font-weight: bold;
    text-align: center;
    color: #4caf50;
    margin-bottom: 15px;
  }

  .sidebar a {
    display: block;
    padding: 12px 18px;
    border-radius: 5px;
    transition: all 0.3s ease;
    font-size: 1rem;
  }

  .sidebar a:hover {
    background: #333;
    transform: scale(1.05);
  }

  /* Main Content */
  .content {
    margin-left: 250px;
    padding: 50px;
  }

  .stat-container {
    display: flex;
    gap: 20px;
  }

  .stat-box {
    background: #1f1f1f;
    padding: 25px;
    border-radius: 10px;
    text-align: center;
    min-width: 160px;
    box-shadow: 0px 0px 12px rgba(255, 255, 255, 0.1);
  }

  .stat-label {
    font-size: 1rem;
    opacity: 0.8;
  }

  .stat-value {
    font-size: 2rem;
    font-weight: bold;
    color: #4caf50;
  }
`;

export default GlobalStyle;
