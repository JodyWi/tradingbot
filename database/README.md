cd database

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



all the data can be stored in the data folder