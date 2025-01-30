import React from "react";
import { Link } from "react-router-dom";
import styled from "styled-components";

// Styled Components
const Container = styled.div`
  display: flex;
  height: 100vh;
  background: #121212;
  color: #ffffff;
`;

const Sidebar = styled.nav`
  width: 250px;
  background: #1f1f1f;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 15px;
  box-shadow: 2px 0 5px rgba(255, 255, 255, 0.1);
`;

const SidebarTitle = styled.h1`
  font-size: 1.5rem;
  font-weight: bold;
  text-align: center;
  color: #4caf50;
`;

const SidebarLink = styled(Link)`
  color: #ffffff;
  text-decoration: none;
  padding: 10px 15px;
  border-radius: 5px;
  transition: background 0.3s;

  &:hover {
    background: #333;
  }
`;

const Content = styled.div`
  flex: 1;
  padding: 40px;
`;

const Heading = styled.h2`
  font-size: 2rem;
  font-weight: bold;
  margin-bottom: 20px;
`;

const Description = styled.p`
  font-size: 1.2rem;
  opacity: 0.8;
`;

const links = [
  { path: "/dashboard", label: "Dashboard" },
  { path: "/trading", label: "Trading" },
  { path: "/settings", label: "Settings" },
  { path: "/history", label: "History" },
];

const Home = () => {
  return (
    <Container>
      {/* Sidebar */}
      <Sidebar>
        <SidebarTitle>Trading Bot</SidebarTitle>
        {links.map((link, index) => (
          <SidebarLink key={index} to={link.path}>
            {link.label}
          </SidebarLink>
        ))}
      </Sidebar>

      {/* Main Content */}
      <Content>
        <Heading>Welcome to the Trading Bot</Heading>
        <Description>
          Monitor trades, check history, and adjust settings in real-time.
        </Description>
      </Content>
    </Container>
  );
};

export default Home;
