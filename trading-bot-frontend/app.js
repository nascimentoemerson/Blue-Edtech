const botState = document.getElementById('botState');
const connectionBadge = document.getElementById('connectionBadge');
const logList = document.getElementById('logList');
const tradesToday = document.getElementById('tradesToday');
const dailyPnl = document.getElementById('dailyPnl');
const lastSignal = document.getElementById('lastSignal');

const configForm = document.getElementById('configForm');
const startBtn = document.getElementById('startBtn');
const pauseBtn = document.getElementById('pauseBtn');
const stopBtn = document.getElementById('stopBtn');

let state = {
  running: false,
  trades: 0,
  pnl: 0,
};

function addLog(message) {
  const time = new Date().toLocaleTimeString('pt-BR');
  const li = document.createElement('li');
  li.textContent = `[${time}] ${message}`;
  logList.prepend(li);
}

function render() {
  botState.textContent = state.running ? 'Executando' : 'Parado';
  connectionBadge.textContent = state.running ? 'Conectado' : 'Desconectado';
  connectionBadge.className = `badge ${state.running ? 'online' : 'offline'}`;
  tradesToday.textContent = String(state.trades);
  dailyPnl.textContent = `${state.pnl.toFixed(2)}%`;
}

configForm.addEventListener('submit', (event) => {
  event.preventDefault();
  const data = new FormData(configForm);
  addLog(`Config salva: ${JSON.stringify(Object.fromEntries(data.entries()))}`);
});

startBtn.addEventListener('click', () => {
  state.running = true;
  state.trades += 1;
  state.pnl += 0.35;
  lastSignal.textContent = 'buy (simulado)';
  addLog('Bot iniciado em modo simulado.');
  render();
});

pauseBtn.addEventListener('click', () => {
  state.running = false;
  addLog('Bot pausado pelo usuário.');
  render();
});

stopBtn.addEventListener('click', () => {
  state.running = false;
  state.pnl = 0;
  lastSignal.textContent = '-';
  addLog('Bot encerrado e estado reiniciado.');
  render();
});

render();
addLog('Painel carregado. Conecte ao backend privado para operar de verdade.');
