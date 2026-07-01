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
import { fetchAllMarketsInfoTest, functionGetAllMarketsInfo, saveMarketsInfoSettings, fetchMarketsInfoSettings} from "../utils/MarketsInfoHelper";
import { fetchAllTradesTest, functionGetAllTrades, saveTradesSettings, fetchTradesSettings} from "../utils/TradesHelper";
import { fetchFromApi } from "../utils/fetchFromApi";

type TabPanelProps = {
  children: React.ReactNode;
  value: number;
  index: number;
};

function TabPanel({ children, value, index, ...other }: TabPanelProps) {
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
    feesInfoSetting: {
      autoFetchOn: false,
      targetTime: "23:00"
    },
    marketsInfoSetting: {
      autoFetchOn: false,
      targetTime: "23:00"
    },
    tradesSetting: {
      autoFetchOn: false,
      targetTime: "23:00"
    },
  });

  // ✅ Fees tab state
  //const [lastUpdated, setLastUpdated] = useState(null);
  const [countdown, setCountdown] = useState<number | null>(null);
  // const [log, setLog] = useState([]);
  const [serverTime, setServerTime] = useState<Date | null>(null);
  const serverTimeRef = useRef<Date | null>(null);

  const handleTabChange = (_: React.SyntheticEvent, newValue: number) => {
    setTabIndex(newValue);
  };
  
  useEffect(() => {
    if (countdown === null) return; // skip initial mount
    if (countdown === 0) {
      functionGetAllFeesInfo();
      // functionGetAllMarketsInfo();
      // functionGetTrades();
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

      const diffSec = Math.floor((target.getTime() - now.getTime()) / 1000);
      setCountdown(diffSec);
    }, 1000);

    return () => clearInterval(interval);
  }, [settings.feesInfoSetting.targetTime]);
  
  // Load Settings 
  useEffect(() => {
    async function loadSettings() {
      const [fees, markets, trades] = await Promise.all([
        fetchFeesInfoSettings(),
        fetchMarketsInfoSettings(),
        fetchTradesSettings(),
      ]);
      if (fees || markets || trades) {
        setSettings(prev => ({
          ...prev,
          feesInfoSetting: {
            autoFetchOn: fees?.autoFetch ?? prev.feesInfoSetting.autoFetchOn,
            targetTime: fees?.autoFetchTime ?? prev.feesInfoSetting.targetTime,
          },
          marketsInfoSetting: {
            autoFetchOn: markets?.autoFetch ?? prev.marketsInfoSetting.autoFetchOn,
            targetTime: markets?.autoFetchTime ?? prev.marketsInfoSetting.targetTime,
          },
          tradesSetting: {
            autoFetchOn: trades?.autoFetch ?? prev.tradesSetting.autoFetchOn,
            targetTime: trades?.autoFetchTime ?? prev.tradesSetting.targetTime,
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
        <Tab label="Trading History" />
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
            Manual Fetch All Markets
          </Button>
          <Button variant="contained" onClick={fetchAllMarketsInfoTest}>
            Manual Test Fetch Markets
          </Button>
          <Divider />
        </Stack>
      </TabPanel>

      {/* ✅ Trades Tab */}
      <TabPanel value={tabIndex} index={3}>
        <Stack spacing={2}>
          <Box display="flex" alignItems="center" gap={2} flexWrap="wrap" sx={sxBorder}>
            {/* ✅ Toggle fetcher on/off */}
            <Typography>Auto-Fetch:</Typography>
            <Switch
              checked={settings.tradesSetting.autoFetchOn}
              onChange={(e) =>
                setSettings((prev) => ({
                  ...prev,
                  tradesSetting: {
                    ...prev.tradesSetting,
                    autoFetchOn: e.target.checked,
                  },
                }))
              }
            />
            {/* ✅ Time Picker */}
            <Typography>Auto-Fetch Time:</Typography>
            <TextField
              type="time"
              value={settings.tradesSetting.targetTime}
              onChange={(e) =>
                setSettings((prev) => ({
                  ...prev,
                  tradesSetting: {
                    ...prev.tradesSetting,
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
          <Button variant="contained" onClick={() => saveTradesSettings(settings.tradesSetting)}>
            Save Settings
          </Button>
          <Button variant="contained" onClick={functionGetAllTrades}>
            Manual Fetch All Trades
          </Button>
          <Button variant="contained" onClick={fetchAllTradesTest}>
            Manual Test Fetch Trades
          </Button>
          <Divider />
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
