// src/utils/FeesScheduler.js

const { functionGetAllFeesInfo } = require('./FeesInfoHelperServer');

function feesInfoSmartScheduler(settings_db) {
  const INTERVAL_MAIN = 30 * 1000; // 30 sec
  const COUNTDOWN_SEC = 30;        // switch to per-sec countdown when close

  let mainInterval = null;
  let countdownInterval = null;

  function startMainScheduler() {
    mainInterval = setInterval(() => {
      try {
        const stmt = settings_db.prepare(
          "SELECT autoFetch, autoFetchTime FROM feesinfo_settings WHERE id = ?"
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

          // console.log(`[Fees Scheduler] Now: ${currentTime} | Target: ${targetTime} | Diff: ${diffSec}s`);

          if (diffSec > 0 && diffSec <= COUNTDOWN_SEC) {
            console.log(`[Fees Info Scheduler] ✅ Starting live countdown (${diffSec}s)`);
            clearInterval(mainInterval);
            startCountdown(diffSec);
          }
        } else {
          console.log("[Fees Info Scheduler] AutoFetch is OFF");
        }
      } catch (err) {
        console.error("[Fees Info Scheduler] Error:", err);
      }
    }, INTERVAL_MAIN);
  }

  function startCountdown(secondsLeft) {
    countdownInterval = setInterval(() => {
      console.log(`[Countdown] ${secondsLeft}s remaining...`);
      secondsLeft -= 1;

      if (secondsLeft <= 0) {
        clearInterval(countdownInterval);
        console.log(`[Fees Info Scheduler] ✅ Running fetchAllFeesInfo now!`);
        functionGetAllFeesInfo();
        startMainScheduler();
      }
    }, 1000);
  }

  return {
    start: () => {
      console.log("[Fees Info Scheduler] 🔄 Starting smart scheduler...");
      startMainScheduler();
    },
  };
}

module.exports = { feesInfoSmartScheduler };
