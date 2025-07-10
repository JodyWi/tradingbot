sudo apt install sqlitebrowser


cd database
sqlitebrowser tradingbot.db

sqlitebrowser ~/projects/tradingbot/database/tradingbot.db
sqlitebrowser ~/projects/tradingbot/database/settings.db
sqlite3 tradingbot.db

.tables

.quit

You’ve got two tables:

balances

trades

Perfect! Here's what your trades table looks like:

Column	Type
id	INTEGER
timestamp	TEXT
asset	TEXT
trade_type	TEXT
amount	REAL
price	REAL


SELECT * FROM trades LIMIT 5;
PRAGMA table_info(trades);


SELECT * FROM balances LIMIT 5;
PRAGMA table_info(balances);



all the data can be stored in the data 

lets start giving things there own databases

changing the tradingbot.db

# 📚 New Databases for Trading Bot

## ✅ Confirmed Databases

- `settings.db`  
  - Stores app settings, configs, keys, feature toggles, bank options, etc.

- `financial.db`  
  - Stores all raw market & asset data: market_info, candles, trades, balance_history, fees, assets_list.

- `conversation.db`  
  - Stores all AI agent conversations, chat history, messages, inter-agent logs.

- `logs.db`  
  - Stores logs for API calls, errors, successes, system tasks, agent activity logs.

- `research.db`  
  - Stores research data: fundamental research, technical analysis snapshots, backtests, research papers.

- `news.db`  
  - Stores market news articles, RSS feeds, AI summaries, sentiment scores.

