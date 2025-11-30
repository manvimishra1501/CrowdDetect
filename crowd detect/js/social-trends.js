// Dummy trending hashtags (will connect to backend later)
const trendingHashtags = [
  "#RCBMeetup",
  "#TempleFestival",
  "#CityMarathon",
  "#MusicConcert",
  "#ProtestRally"
];

const hashtagsList = document.getElementById('hashtagsList');
trendingHashtags.forEach(tag => {
  const li = document.createElement('li');
  li.textContent = tag;
  hashtagsList.appendChild(li);
});

// Keyword Spike Chart using Chart.js
const ctx = document.getElementById('keywordChart').getContext('2d');
const keywordChart = new Chart(ctx, {
  type: 'line',
  data: {
    labels: ['10:00', '10:05', '10:10', '10:15', '10:20', '10:25'],
    datasets: [{
      label: 'Mentions per minute',
      data: [5, 12, 25, 40, 30, 50], // placeholder
      backgroundColor: 'rgba(59,130,246,0.2)',
      borderColor: 'rgba(59,130,246,1)',
      borderWidth: 2,
      tension: 0.4,
      fill: true,
      pointRadius: 4,
      pointBackgroundColor: 'rgba(59,130,246,1)'
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
        title: { display: true, text: 'Mentions' },
        beginAtZero: true
      }
    }
  }
});
