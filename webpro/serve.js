// server.js
const WebSocket = require('ws');
const { exec } = require('child_process');

const wss = new WebSocket.Server({ port: 8080 });

wss.on('connection', (ws) => {
  ws.on('message', (message) => {
    console.log(`[SERVER] received: ${message}`)
    cmd = String(message)
    exec(cmd, (error, stdout, stderr) => {
      if (error) {
        ws.send(`Error: ${error.message}`);
      } else {
        ws.send(`Output: ${stdout}`);
      }
    });
  });
});

