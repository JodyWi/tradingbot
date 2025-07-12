import React from "react";
import { NavLink } from "react-router-dom";
import {
  Drawer,
  List,
  ListItemButton,
  ListItemText,
  Typography,
  Box,
  Divider
} from "@mui/material";

const Sidebar = ({ links }) => {
  return (
    <Drawer
      variant="permanent"
      sx={{
        width: 240,
        flexShrink: 0,
        [`& .MuiDrawer-paper`]: {
          width: 240,
          boxSizing: "border-box",
          display: "flex",
          flexDirection: "column",
          justifyContent: "space-between",
        },
      }}
    >
      <Box>
        <Box sx={{ p: 3, borderBottom: "1px solid #555" }}>
          <Typography variant="h5" color="primary">
            Trading Bot
          </Typography>
        </Box>

        <List>
          {links.map((link, i) => (
            <React.Fragment key={i}>
              <NavLink
                to={link.path}
                style={{ textDecoration: "none", color: "inherit" }}
              >
                {({ isActive }) => (
                  <ListItemButton
                    selected={isActive}
                    sx={{
                      "&.Mui-selected": {
                        bgcolor: "primary.main",
                        color: "#fff",
                      },
                      "&:hover": { bgcolor: "#333" },
                    }}
                  >
                    <ListItemText primary={link.label} />
                  </ListItemButton>
                )}
              </NavLink>

              {link.label === "Markets Info" && (
                <Divider
                  sx={{
                    my: 1,               
                    borderColor: "#666", 
                    borderWidth: "0.5px",
                    mx: 2,               
                    borderRadius: "2px", 
                  }}
                />
              )}
            </React.Fragment>
          ))}
        </List>
      </Box>

      <Box>
        <Divider sx={{ bgcolor: "#555" }} />
        <NavLink
          to="/Settings"
          style={{ textDecoration: "none", color: "inherit" }}
        >
          {({ isActive }) => (
            <ListItemButton
              selected={isActive}
              sx={{
                "&.Mui-selected": {
                  bgcolor: "primary.main",
                  color: "#fff",
                },
                "&:hover": { bgcolor: "#333" },
              }}
            >
              <ListItemText primary="Settings" />
            </ListItemButton>
          )}
        </NavLink>

        <Divider sx={{ bgcolor: "#555" }} />

        <Box sx={{ p: 2, fontSize: "0.75rem", color: "#aaa" }}>
          JodyWi © 2025 — All Rights Reserved
        </Box>
      </Box>
    </Drawer>
  );
};

export default Sidebar;
