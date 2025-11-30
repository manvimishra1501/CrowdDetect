// Toggle Sidebar for Mobile
function toggleSidebar() {
  const sidebar = document.getElementById('sidebar');
  sidebar.classList.toggle('collapsed');
}

// Sparkline Mini-Graphs (Placeholder Data)
function createSparkline(ctxId, data) {
  const ctx = document.getElementById(ctxId).getContext('2d');
  new Chart(ctx, {
    type: 'line',
    data: { labels: [...Array(data.length).keys()], datasets: [{data, borderColor:'#3b82f6', borderWidth:1, fill:false, tension:0.3, pointRadius:0}] },
    options: { responsive:true, plugins:{legend:{display:false}}, scales:{x:{display:false}, y:{display:false}} }
  });
}

// Example Data
createSparkline('sparklineLive', [1000,1150,1200,1250,1230,1200]);
createSparkline('sparklineHeatmap', [3,4,5,5,4,5]);
createSparkline('sparklineAlerts', [1,2,2,3,2,2]);
createSparkline('sparklineTrends', [5,10,15,20,25,18]);
createSparkline('sparklinePrediction', [1200,1300,1400,1450,1500,1480]);
