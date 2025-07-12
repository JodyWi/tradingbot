import React, { useState, useEffect, useRef } from "react";
import {
  Box,
  Typography,
  Tabs,
  Tab,
  Divider,
  TextField,
  Stack,
  Button,
  Switch,
} from "@mui/material";
import { fetchAllFeesTest, fetchAllFeesInfo, saveFeesInfoSettings, fetchFeesInfoSettings } from "../utils/FeesHepler";
import { fetchFromApi } from "../utils/fetchFromApi";
function TabPanel({ children, value, index, ...other }) {
  return (
    <div
      hidden={value !== index}
      {...other}
    >
      {value === index && (
        <Box sx={{ py: 2 }}>
          {children}
        </Box>
      )}
    </div>
  );
}


const SettingsPage = () => {
  const [tabIndex, setTabIndex] = useState(0);
  const [settings, setSettings] = useState({
    generalSetting: "",
    tradingSetting: "",
    feesSetting: {
      autoFetchOn: false,
      targetTime: "23:00",
      cronJobOn: false
    },
  });

  // ✅ Fees tab state
  //const [lastUpdated, setLastUpdated] = useState(null);
  const [countdown, setCountdown] = useState(null);
  // const [log, setLog] = useState([]);
  const [serverTime, setServerTime] = useState(null);
  const serverTimeRef = useRef(null);

  const handleTabChange = (_, newValue) => {
    setTabIndex(newValue);
  };
  
  useEffect(() => {
    if (countdown === null) return; // skip initial mount
    if (countdown === 0) {
      fetchAllFeesInfo();
    }
  }, [countdown]);

  // Fetch server time initially and every minute to resync
  useEffect(() => {
    async function fetchServerTime() {
      try {
        const data = await fetchFromApi("/api/server-time");
        const newTime = new Date(data.serverTime);
        setServerTime(newTime);
        serverTimeRef.current = newTime;
      } catch (err) {
        console.error("Error fetching server time:", err);
      }
    }

    fetchServerTime();
    const intervalFetch = setInterval(fetchServerTime, 60 * 1000);
    const intervalTick = setInterval(() => {
      if (serverTimeRef.current) {
        serverTimeRef.current = new Date(serverTimeRef.current.getTime() + 1000);
        setServerTime(new Date(serverTimeRef.current));
      }
    }, 1000);

    return () => {
      clearInterval(intervalFetch);
      clearInterval(intervalTick);
    };
  }, []);

  useEffect(() => {
    const interval = setInterval(() => {
      const now = new Date();
      const [hours, minutes] = settings.feesSetting.targetTime.split(":").map(Number);

      const target = new Date();
      target.setHours(hours, minutes, 0, 0);

      if (target < now) {
        target.setDate(target.getDate() + 1);
      }

      const diffSec = Math.floor((target - now) / 1000);
      setCountdown(diffSec);
    }, 1000);

    return () => clearInterval(interval);
  }, [settings.feesSetting.targetTime]);
  
  // Load Fees Settings 
  useEffect(() => {
    async function loadSettings() {
      const fetched = await fetchFeesInfoSettings();
      if (fetched) {
        setSettings(prev => ({
          ...prev,
          feesSetting: {
            autoFetchOn: fetched.autoFetch,
            targetTime: fetched.autoFetchTime,
          },
        }));
      }
    }
    loadSettings();
  }, []);

  const sxBorder = {
    border: "1px solid #ccc",
    borderRadius: 2,
    p: 2,
  };

  return (
    <Box p={4}>
      <Typography variant="h4" gutterBottom>
        Settings
      </Typography>
      <Divider sx={{ mb: 3 }} />

      <Tabs
        value={tabIndex}
        onChange={handleTabChange}
        textColor="primary"
        indicatorColor="primary"
      >
        <Tab label="General" />
        <Tab label="Fees" />
        <Tab label="Trading" />
        <Tab label="Notifications" />
      </Tabs>

      <TabPanel value={tabIndex} index={0}>
        <Stack spacing={2}>
          <TextField
            label="General Setting"
            fullWidth
            value={settings.generalSetting}
            onChange={(e) =>
              setSettings({ ...settings, generalSetting: e.target.value })
            }
          />
        </Stack>
      </TabPanel>

      {/* ✅ Fees Tab */}
      <TabPanel value={tabIndex} index={1}>
        <Stack spacing={2}>
          <Box display="flex" alignItems="center" gap={2} flexWrap="wrap" sx={sxBorder}>
            {/* ✅ Toggle fetcher on/off */}
            <Typography>Auto-Fetch:</Typography>
            <Switch
              checked={settings.feesSetting.autoFetchOn}
              onChange={(e) =>
                setSettings((prev) => ({
                  ...prev,
                  feesSetting: {
                    ...prev.feesSetting,
                    autoFetchOn: e.target.checked,
                  },
                }))
              }
            />
                        {/* ✅ Toggle fetcher on/off */}
            <Typography>Auto-Fetch: Cron</Typography>
            <Switch
              checked={settings.feesSetting.cronJobOn}
              onChange={(e) =>
                setSettings((prev) => ({
                  ...prev,
                  feesSetting: {
                    ...prev.feesSetting,
                    cronJobOn: e.target.checked,
                  },
                }))
              }
            />
            {/* ✅ Time Picker */}
            <Typography>Auto-Fetch Time:</Typography>
            <TextField
              type="time"
              value={settings.feesSetting.targetTime}
              onChange={(e) =>
                setSettings((prev) => ({
                  ...prev,
                  feesSetting: {
                    ...prev.feesSetting,
                    targetTime: e.target.value,
                  },
                }))
              }
              sx={{ width: 120 }}
              inputProps={{ step: 60 }}
            />
            {/* ✅ Countdown */}
            <Typography>
              Auto-Fetch in: {Math.floor(countdown / 3600)}h{" "}
              {Math.floor((countdown % 3600) / 60)}m {countdown % 60}s
            </Typography>
            {/* ✅ Server Time */}
            <Typography sx={{ color: "gray" }}>
              Server Time: {serverTime ? new Date(serverTime).toLocaleString() : "Loading..."}
            </Typography>
          </Box>
          {/* ✅ Save Settings */}
          <Button variant="contained" onClick={() => saveFeesInfoSettings(settings.feesSetting)}>
            Save Settings
          </Button>
          <Button variant="contained" onClick={fetchAllFeesInfo}>
            Manual Fetch All Fees
          </Button>
          <Button variant="contained" onClick={fetchAllFeesTest}>
            Manual Test Fetch All Fees
          </Button>
          <Divider />
          {/* and when i manual update can we have a live visals showing the data coming in? make sure we do a slow data get please please */}
          {/* <Box sx={{ maxHeight: 200, overflowY: "auto", bgcolor: "#111", p: 2 }}>
            {log.map((entry, idx) => (
              <Typography key={idx} sx={{ fontSize: "0.8rem" }}>
                {entry}
              </Typography>
            ))}
          </Box> */}
        </Stack>
      </TabPanel>

      <TabPanel value={tabIndex} index={2}>
        <Stack spacing={2}>
          <TextField
            label="Trading Pair"
            fullWidth
            value={settings.tradingSetting}
            onChange={(e) =>
              setSettings({ ...settings, tradingSetting: e.target.value })
            }
          />
        </Stack>
      </TabPanel>

      <TabPanel value={tabIndex} index={3}>
        <Stack spacing={2}>
          <Typography variant="body1">
            Notification settings will go here.
          </Typography>
        </Stack>
      </TabPanel>

      <Divider sx={{ my: 3 }} />
    </Box>
  );
};

export default SettingsPage;
