// Global Application State & Chart references
let telemetryChart = null;
const maxChartPoints = 15;
const chartTimeLabels = [];
const cpuHistoryData = [];
const ramHistoryData = [];

// Initialize Dashboard UI once DOM loads
document.addEventListener('DOMContentLoaded', () => {
  initTelemetryChart();
  startMetricsPolling();
  setupActionListeners();
  
  // Initial metrics fetch
  fetchMetrics();
});

// Initialize Chart.js configuration with neon styling
function initTelemetryChart() {
  const ctx = document.getElementById('telemetryChart').getContext('2d');
  
  // Custom neon line gradients
  const cpuGradient = ctx.createLinearGradient(0, 0, 0, 200);
  cpuGradient.addColorStop(0, 'rgba(59, 130, 246, 0.4)');
  cpuGradient.addColorStop(1, 'rgba(59, 130, 246, 0.0)');

  const ramGradient = ctx.createLinearGradient(0, 0, 0, 200);
  ramGradient.addColorStop(0, 'rgba(16, 185, 129, 0.4)');
  ramGradient.addColorStop(1, 'rgba(16, 185, 129, 0.0)');

  telemetryChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: chartTimeLabels,
      datasets: [
        {
          label: 'CPU Utilization (%)',
          data: cpuHistoryData,
          borderColor: '#3b82f6',
          borderWidth: 2,
          backgroundColor: cpuGradient,
          fill: true,
          tension: 0.3,
          pointRadius: 3,
          pointHoverRadius: 5
        },
        {
          label: 'RAM Allocation (%)',
          data: ramHistoryData,
          borderColor: '#10b981',
          borderWidth: 2,
          backgroundColor: ramGradient,
          fill: true,
          tension: 0.3,
          pointRadius: 3,
          pointHoverRadius: 5
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: 'top',
          labels: {
            color: '#9ca3af',
            font: { family: 'Outfit', size: 12 }
          }
        }
      },
      scales: {
        y: {
          min: 0,
          max: 100,
          grid: { color: 'rgba(255, 255, 255, 0.05)' },
          ticks: {
            color: '#9ca3af',
            font: { family: 'Outfit' },
            callback: value => value + '%'
          }
        },
        x: {
          grid: { display: false },
          ticks: {
            color: '#9ca3af',
            font: { family: 'Outfit' }
          }
        }
      }
    }
  });
}

// Poll server metrics endpoints
function startMetricsPolling() {
  setInterval(fetchMetrics, 2000);
}

// Fetch stats and update charts
async function fetchMetrics() {
  try {
    const res = await fetch('/api/metrics');
    if (!res.ok) throw new Error('Failed to retrieve metrics');
    const data = await res.json();
    
    updateUIElements(data);
    updateChartData(data.cpu, data.ram);
  } catch (error) {
    console.error('Scrape error: ', error);
  }
}

// Update DOM components
function updateUIElements(data) {
  // Numeric Values
  document.getElementById('cpu-val').innerText = `${data.cpu}%`;
  document.getElementById('ram-val').innerText = `${data.ram}%`;
  document.getElementById('disk-val').innerText = `${data.disk}%`;
  
  // Progress Fills
  document.getElementById('cpu-bar').style.width = `${data.cpu}%`;
  document.getElementById('ram-bar').style.width = `${data.ram}%`;
  document.getElementById('disk-bar').style.width = `${data.disk}%`;

  // Hostname & details
  document.getElementById('hostname-display').innerHTML = `<i class="fa-solid fa-server"></i> ${data.environment.hostname} (${data.environment.arch})`;
  document.getElementById('ram-details').innerText = `Used: ${data.ramDetails.used} / Total: ${data.ramDetails.total}`;
  document.getElementById('disk-details').innerText = `Used: ${data.diskDetails.used} / Total: ${data.diskDetails.total}`;

  // Process CPU active simulation highlights
  const cpuCard = document.getElementById('cpu-card');
  if (data.cpuSpikeActive) {
    cpuCard.classList.add('card-glow-rose');
    cpuCard.style.borderColor = 'rgba(244, 63, 94, 0.4)';
  } else {
    cpuCard.classList.remove('card-glow-rose');
    cpuCard.style.borderColor = '';
  }

  // Format and load uptime clock
  updateUptimeClock(data.uptime);

  // Re-build processes table
  const processList = document.getElementById('process-list');
  processList.innerHTML = '';
  data.processes.forEach(proc => {
    const statusClass = proc.status === 'RUNNING' ? 'status-running' : 'status-sleeping';
    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td>${proc.pid}</td>
      <td style="color: #60a5fa">${proc.name}</td>
      <td>${proc.cpu}</td>
      <td>${proc.mem}</td>
      <td><span class="status-pill ${statusClass}">${proc.status}</span></td>
    `;
    processList.appendChild(tr);
  });
}

// Uptime calculations formatting
function updateUptimeClock(totalSeconds) {
  const days = Math.floor(totalSeconds / (3600 * 24));
  const hours = Math.floor((totalSeconds % (3600 * 24)) / 3600);
  const minutes = Math.floor((totalSeconds % 3600) / 60);
  const seconds = totalSeconds % 60;
  
  document.getElementById('uptime-val').innerText = 
    `${days}d ${hours.toString().padStart(2, '0')}h ${minutes.toString().padStart(2, '0')}m ${seconds.toString().padStart(2, '0')}s`;
}

// Scrolling graph updates
function updateChartData(cpu, ram) {
  const now = new Date();
  const timeStr = `${now.getHours().toString().padStart(2, '0')}:${now.getMinutes().toString().padStart(2, '0')}:${now.getSeconds().toString().padStart(2, '0')}`;
  
  chartTimeLabels.push(timeStr);
  cpuHistoryData.push(cpu);
  ramHistoryData.push(ram);

  // Prune old history elements
  if (chartTimeLabels.length > maxChartPoints) {
    chartTimeLabels.shift();
    cpuHistoryData.shift();
    ramHistoryData.shift();
  }

  telemetryChart.update();
}

// Virtual command line output logging
function printToTerminal(text, type = 'stdout') {
  const terminal = document.getElementById('terminal-stdout');
  const lines = text.split('\n');
  
  lines.forEach(line => {
    const lineDiv = document.createElement('div');
    lineDiv.className = `term-line output-${type}`;
    lineDiv.innerText = line;
    terminal.appendChild(lineDiv);
  });

  // Keep auto-scroll active
  terminal.scrollTop = terminal.scrollHeight;
}

// Wire actions and clicks
function setupActionListeners() {
  const termBody = document.getElementById('terminal-stdout');

  // Clear Terminal Button
  document.getElementById('btn-clear-term').addEventListener('click', () => {
    termBody.innerHTML = '';
    printToTerminal('Terminal console flushed.', 'system');
  });

  // Spike CPU Load Button
  document.getElementById('btn-spike').addEventListener('click', async () => {
    printToTerminal('curl -X POST http://localhost:3000/api/simulate-load', 'cmd');
    try {
      const res = await fetch('/api/simulate-load', { method: 'POST' });
      const data = await res.json();
      printToTerminal(`[SYSTEM INFO] ${data.message}`, 'system');
    } catch (err) {
      printToTerminal(`[ERROR] Failed to contact load spikes controller`, 'error');
    }
  });

  // Trigger Backup Script Button
  document.getElementById('btn-backup').addEventListener('click', async () => {
    printToTerminal('sh scripts/backup.sh', 'cmd');
    
    // Disable button to prevent click flooding during script execution
    const btn = document.getElementById('btn-backup');
    btn.style.opacity = '0.5';
    btn.style.pointerEvents = 'none';

    try {
      const res = await fetch('/api/trigger-backup', { method: 'POST' });
      const data = await res.json();
      
      printToTerminal(data.stdout, 'stdout');
      if (data.stderr) printToTerminal(data.stderr, 'error');
      
      printToTerminal(`[SYSTEM] Command finished successfully. (${data.note})`, 'system');
    } catch (err) {
      printToTerminal(`[ERROR] Failed to run automated backup script.`, 'error');
    } finally {
      btn.style.opacity = '1';
      btn.style.pointerEvents = 'auto';
    }
  });

  // Trigger Log Cleanup Button
  document.getElementById('btn-cleanup').addEventListener('click', async () => {
    printToTerminal('sh scripts/cleanup.sh', 'cmd');
    
    const btn = document.getElementById('btn-cleanup');
    btn.style.opacity = '0.5';
    btn.style.pointerEvents = 'none';

    try {
      const res = await fetch('/api/trigger-cleanup', { method: 'POST' });
      const data = await res.json();
      
      printToTerminal(data.stdout, 'stdout');
      if (data.stderr) printToTerminal(data.stderr, 'error');
      
      printToTerminal(`[SYSTEM] Command finished successfully. (${data.note})`, 'system');
    } catch (err) {
      printToTerminal(`[ERROR] Failed to execute cleanup script.`, 'error');
    } finally {
      btn.style.opacity = '1';
      btn.style.pointerEvents = 'auto';
    }
  });
}
