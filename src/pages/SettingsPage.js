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
import { fetchAllFeesInfoTest, functionGetAllFeesInfo, saveFeesInfoSettings, fetchFeesInfoSettings } from "../utils/FeesInfoHelper";
import { fetchAllMarketsInfoTest, functionGetAllMarketsInfo, saveMarketsInfoSettings, fetchMarketsInfoSettings } from "../utils/MarketsInfoHelper";
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
    feesInfoSetting: {
      autoFetchOn: false,
      targetTime: "23:00"
    },
    marketsInfoSetting: {
      autoFetchOn: false,
      targetTime: "23:00"
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
      functionGetAllFeesInfo();
      // functionGetAllMarketsInfo();
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
      const [hours, minutes] = settings.feesInfoSetting.targetTime.split(":").map(Number);

      const target = new Date();
      target.setHours(hours, minutes, 0, 0);

      if (target < now) {
        target.setDate(target.getDate() + 1);
      }

      const diffSec = Math.floor((target - now) / 1000);
      setCountdown(diffSec);
    }, 1000);

    return () => clearInterval(interval);
  }, [settings.feesInfoSetting.targetTime]);
  
  // Load Settings 
  useEffect(() => {
    async function loadSettings() {
      const fetched = await fetchFeesInfoSettings();
      if (fetched) {
        setSettings(prev => ({
          ...prev,
          feesInfoSetting: {
            autoFetchOn: fetched.autoFetch,
            targetTime: fetched.autoFetchTime,
          },
          marketsInfoSetting: {
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
        <Tab label="Fees Info" />
        <Tab label="Markets Info" />
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

      {/* ✅ Fees info Tab */}
      <TabPanel value={tabIndex} index={1}>
        <Stack spacing={2}>
          <Box display="flex" alignItems="center" gap={2} flexWrap="wrap" sx={sxBorder}>
            {/* ✅ Toggle fetcher on/off */}
            <Typography>Auto-Fetch:</Typography>
            <Switch
              checked={settings.feesInfoSetting.autoFetchOn}
              onChange={(e) =>
                setSettings((prev) => ({
                  ...prev,
                  feesInfoSetting: {
                    ...prev.feesInfoSetting,
                    autoFetchOn: e.target.checked,
                  },
                }))
              }
            />
            {/* ✅ Time Picker */}
            <Typography>Auto-Fetch Time:</Typography>
            <TextField
              type="time"
              value={settings.feesInfoSetting.targetTime}
              onChange={(e) =>
                setSettings((prev) => ({
                  ...prev,
                  feesInfoSetting: {
                    ...prev.feesInfoSetting,
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
          <Button variant="contained" onClick={() => saveFeesInfoSettings(settings.feesInfoSetting)}>
            Save Settings
          </Button>
          <Button variant="contained" onClick={functionGetAllFeesInfo}>
            Manual Fetch All Fees
          </Button>
          <Button variant="contained" onClick={fetchAllFeesInfoTest}>
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

      {/* ✅ Market info Tab */}
      <TabPanel value={tabIndex} index={2}>
        <Stack spacing={2}>
          <Box display="flex" alignItems="center" gap={2} flexWrap="wrap" sx={sxBorder}>
            {/* ✅ Toggle fetcher on/off */}
            <Typography>Auto-Fetch:</Typography>
            <Switch
              checked={settings.marketsInfoSetting.autoFetchOn}
              onChange={(e) =>
                setSettings((prev) => ({
                  ...prev,
                  marketsInfoSetting: {
                    ...prev.marketsInfoSetting,
                    autoFetchOn: e.target.checked,
                  },
                }))
              }
            />
            {/* ✅ Time Picker */}
            <Typography>Auto-Fetch Time:</Typography>
            <TextField
              type="time"
              value={settings.marketsInfoSetting.targetTime}
              onChange={(e) =>
                setSettings((prev) => ({
                  ...prev,
                  marketsInfoSetting: {
                    ...prev.marketsInfoSetting,
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
          <Button variant="contained" onClick={() => saveMarketsInfoSettings(settings.marketsInfoSetting)}>
            Save Settings
          </Button>
          <Button variant="contained" onClick={functionGetAllMarketsInfo}>
            Manual Fetch All Fees
          </Button>
          <Button variant="contained" onClick={fetchAllMarketsInfoTest}>
            Manual Test Fetch All Fees
          </Button>
          <Divider />
        </Stack>
      </TabPanel>

      <TabPanel value={tabIndex} index={3}>
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

      <TabPanel value={tabIndex} index={4}>
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
