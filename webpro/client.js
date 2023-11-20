// client.js
const ws = new WebSocket('ws://localhost:8080');
const outputElement = document.getElementById('output');
const executeBtn = document.getElementById('executeBtn');
const createdataBtn=document.getElementById('createdataBtn');
const monitordataBtn=document.getElementById('monitordataBtn');
const top10dataBtn=document.getElementById('top10dataBtn');

executeBtn.addEventListener('click', () => {
  const command = 'ls';
    ws.send(command);
});

ws.onmessage = (event) => {
  outputElement.innerHTML += event.data + '<br>';
};

createdataBtn.addEventListener('click', () => {
  const command = 'sudo python3 datapacket.py';
  if (command) {
    ws.send(command);
  }
});

ws.onmessage = (event) => {
  outputElement.innerHTML += event.data + '<br>';
};

monitordataBtn.addEventListener('click', () => {
  const command = 'sudo python3 CountMinSketch.py';
  if (command) {
    ws.send(command);
  }
});

ws.onmessage = (event) => {
  outputElement.innerHTML += event.data + '<br>';
};

top10dataBtn.addEventListener('click', () => {
  const command = 'sudo python3 heavyhitter.py';
  if (command) {
    ws.send(command);
  }
});

ws.onmessage = (event) => {
  outputElement.innerHTML += event.data + '<br>';
};

function createTopology() {
  console.log('Success!');
  document.getElementById("topologyImage").style.display = "flex";
}

