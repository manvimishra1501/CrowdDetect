const videoInput = document.getElementById("videoInput");
const videoPlayer = document.getElementById("videoPlayer");
const peopleCountElement = document.querySelector(".people-count");
const generateHeatmapBtn = document.getElementById("generateHeatmap");

// Handle video upload and preview
videoInput.addEventListener("change", (event) => {
    const file = event.target.files[0];
    if (file) {
        const url = URL.createObjectURL(file);
        videoPlayer.src = url;
        videoPlayer.play();

        // Placeholder: simulate backend processing
        peopleCountElement.textContent = "Processing video...";
        setTimeout(() => {
            const simulatedCount = Math.floor(Math.random() * 100);
            peopleCountElement.textContent = `People Count: ${simulatedCount}`;
        }, 3000);
    }
});



// Video upload processing
const videoInput = document.getElementById('videoInput');
const uploadedVideo = document.getElementById('uploadedVideo');

videoInput.addEventListener('change', async () => {
  const file = videoInput.files[0];
  if (!file) return;

  // Play the selected video immediately
  uploadedVideo.src = URL.createObjectURL(file);
  uploadedVideo.load();
  uploadedVideo.play();

  const formData = new FormData();
  formData.append('file', file);

  try {
    const res = await fetch('http://127.0.0.1:5000/upload_video', {
      method: 'POST',
      body: formData
    });
    const data = await res.json();
    document.getElementById('videoCount').innerText = data.max_count_seen;
    console.log("Video processed:", data);

    // After processing, play the annotated output from backend
    uploadedVideo.src = "C:\Users\kritk\OneDrive\Desktop\WhatsApp Video 2025-09-21 at 09.50.40_5e93d6b7.mp4" + new Date().getTime(); // cache-busting
    uploadedVideo.load();
    uploadedVideo.play();
  } catch(err) {
    console.error("Error uploading video:", err);
  }
});

// Navigate to Heatmap page after processing
generateHeatmapBtn.addEventListener("click", () => {
    // TODO: In future, send backend request to generate heatmap
    window.location.href = "heatmap.html";
});
