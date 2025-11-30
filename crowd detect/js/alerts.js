// Placeholder alerts (dynamic data will come from Python backend)
const dummyAlerts = [
  {
    message: "High crowd density detected near Gate 3",
    severity: "high",
    time: "2 mins ago"
  },
  {
    message: "Moderate congestion near Temple entrance",
    severity: "medium",
    time: "5 mins ago"
  },
  {
    message: "Low crowd density at Parking Area B",
    severity: "low",
    time: "10 mins ago"
  }
];

const alertsContainer = document.getElementById('alertsContainer');

dummyAlerts.forEach(alert => {
  const alertCard = document.createElement('div');
  alertCard.classList.add('alert-card', `alert-${alert.severity}`);

  alertCard.innerHTML = `
    <div class="alert-info">
      <h3>${alert.message}</h3>
      <p class="alert-time">${alert.time}</p>
    </div>
  `;

  alertsContainer.appendChild(alertCard);
});

// TODO: Connect with Python backend to fetch live alerts dynamically
