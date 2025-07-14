// src/utils/MarketsScheduler.js

const { functionGetAllMarketsInfo } = require('./MarketsInfoHelper');

function marketsInfoSmartScheduler(settings_db) {
  const INTERVAL_MAIN = 30 * 1000; // 30 sec
  const COUNTDOWN_SEC = 30;        // switch to per-sec countdown when close

  let mainInterval = null;
  let countdownInterval = null;

  function startMainScheduler() {
    mainInterval = setInterval(() => {
      try {
        const stmt = settings_db.prepare(
          "SELECT autoFetch, autoFetchTime FROM marketsinfo_settings WHERE id = ?"
        );
        const row = stmt.get("singleton");

        if (row && row.autoFetch) {
          const targetTime = row.autoFetchTime; // "HH:MM"
          const now = new Date();
          const currentTime = now.toTimeString().slice(0, 5);

          const [targetH, targetM] = targetTime.split(":").map(Number);
          const [currentH, currentM] = currentTime.split(":").map(Number);

          const targetDate = new Date();
          targetDate.setHours(targetH, targetM, 0, 0);

          const diffMs = targetDate - now;
          const diffSec = Math.floor(diffMs / 1000);

          // console.log(`[Markets Scheduler] Now: ${currentTime} | Target: ${targetTime} | Diff: ${diffSec}s`);

          if (diffSec > 0 && diffSec <= COUNTDOWN_SEC) {
            console.log(`[Markets Scheduler] ✅ Starting live countdown (${diffSec}s)`);
            clearInterval(mainInterval);
            startCountdown(diffSec);
          }
        } else {
          //console.log("[Markets Scheduler] AutoFetch is OFF");
        }
      } catch (err) {
        console.error("[Markets Scheduler] Error:", err);
      }
    }, INTERVAL_MAIN);
  }

  function startCountdown(secondsLeft) {
    countdownInterval = setInterval(() => {
      console.log(`[Countdown] ${secondsLeft}s remaining...`);
      secondsLeft -= 1;

      if (secondsLeft <= 0) {
        clearInterval(countdownInterval);
        console.log(`[Markets Scheduler] ✅ Running fetchAllMarketsInfo now!`);
        functionGetAllMarketsInfo();
        startMainScheduler();
      }
    }, 1000);
  }

  return {
    start: () => {
      console.log("[Markets Scheduler] 🔄 Starting smart scheduler...");
      startMainScheduler();
    },
  };
}

module.exports = { marketsInfoSmartScheduler };
