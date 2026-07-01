(venv) (base) ubuntu@Echo:~/projects/tradingbot/backend$ python server.py
 * Serving Flask app 'server'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:8001
 * Running on http://172.31.211.27:8001
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 260-692-493
 * Detected change in '/home/ubuntu/projects/tradingbot/backend/luno_api_functions/luno_tickers.py', reloading
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 260-692-493


Compiled successfully!

You can now view pro in the browser.

  Local:            http://localhost:3001
  On Your Network:  http://172.31.211.27:3001

Note that the development build is not optimized.
To create a production build, use npm run build.

webpack compiled successfully



(base) ubuntu@Echo:~/projects/tradingbot/backend$ node server.js
node:events:502
      throw er; // Unhandled 'error' event
      ^

Error: listen EADDRINUSE: address already in use :::3001
    at Server.setupListenHandle [as _listen2] (node:net:1937:16)
    at listenInCluster (node:net:1994:12)
    at Server.listen (node:net:2099:7)
    at Function.listen (/home/ubuntu/projects/tradingbot/node_modules/express/lib/application.js:635:24)
    at Object.<anonymous> (/home/ubuntu/projects/tradingbot/backend/server.js:23:5)
    at Module._compile (node:internal/modules/cjs/loader:1562:14)
    at Object..js (node:internal/modules/cjs/loader:1699:10)
    at Module.load (node:internal/modules/cjs/loader:1313:32)
    at Function._load (node:internal/modules/cjs/loader:1123:12)
    at TracingChannel.traceSync (node:diagnostics_channel:322:14)
Emitted 'error' event on Server instance at:
    at emitErrorNT (node:net:1973:8)
    at process.processTicksAndRejections (node:internal/process/task_queues:90:21) {
  code: 'EADDRINUSE',
  errno: -98,
  syscall: 'listen',
  address: '::',
  port: 3001
}

Node.js v22.13.1
(base) ubuntu@Echo:~/projects/tradingbot/backend$ 