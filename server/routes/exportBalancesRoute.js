// server/routes/exportBalancesRoute.js

const express = require("express");
const router = express.Router();
const exportBalances = require("../../scripts/exportBalances");

router.post("/export-balances", (req, res) => {
  exportBalances()
    .then(() => res.json({ success: true }))
    .catch((err) => res.status(500).json({ error: err.message }));
});

module.exports = router;
