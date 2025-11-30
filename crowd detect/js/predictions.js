// Placeholder data (to be replaced by backend predictions)
const ctx = document.getElementById('predictionChart').getContext('2d');

const predictionChart = new Chart(ctx, {
  type: 'line',
  data: {
    labels: ['Now', '10 min', '20 min', '30 min', '40 min', '50 min', '60 min'],
    datasets: [{
      label: 'Predicted Crowd Count',
      data: [150, 200, 320, 450, 600, 750, 900], // example values
      backgroundColor: 'rgba(16,185,129,0.2)',
      borderColor: 'rgba(16,185,129,1)',
      borderWidth: 2,
      tension: 0.4,
      fill: true,
      pointRadius: 4,
      pointBackgroundColor: 'rgba(16,185,129,1)'
    }]
  },
  options: {
    responsive: true,
    plugins: {
      legend: { display: false },
      tooltip: { mode: 'index', intersect: false }
    },
    scales: {
      x: {
        title: { display: true, text: 'Time' }
      },
      y: {
        title: { display: true, text: 'Number of People' },
        beginAtZero: true
      }
    }
  }
});
