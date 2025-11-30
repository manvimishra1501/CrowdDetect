import cv2
from pathlib import Path
from ultralytics import YOLO

# -----------------------------
# --- Paths ---
# -----------------------------
VIDEO_PATH = r"C:\Users\kritk\OneDrive\Desktop\WhatsApp Video 2025-09-21 at 09.50.40_5e93d6b7.mp4"  # your video
OUTPUT_PATH = "output_video.mp4"
YOLO_WEIGHTS = "models/yolov8n.pt"  # make sure this exists

# -----------------------------
# --- Open Video ---
# -----------------------------
cap = cv2.VideoCapture(VIDEO_PATH)
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)

# -----------------------------
# --- Video Writer ---
# -----------------------------
out = cv2.VideoWriter(
    OUTPUT_PATH,
    cv2.VideoWriter_fourcc(*'mp4v'),
    fps,
    (frame_width, frame_height)
)

# -----------------------------
# --- Load YOLO Model ---
# -----------------------------
model = YOLO(YOLO_WEIGHTS)

# -----------------------------
# --- Counting Variables ---
# -----------------------------
max_people = 0
total_people = 0
frame_count = 0

# -----------------------------
# --- Process Video ---
# -----------------------------
while True:
    ret, frame = cap.read()
    if not ret:
        break

    # YOLOv8 detection
    results = model(frame)[0]

    # Count people (class 0 = person)
    person_count = 0
    for box, cls in zip(results.boxes.xyxy, results.boxes.cls):
        if int(cls) == 0:
            person_count += 1
            x1, y1, x2, y2 = map(int, box)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, "Person", (x1, y1-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1)

    # Update counters
    total_people += person_count
    if person_count > max_people:
        max_people = person_count

    # Overlay counts on frame
    cv2.putText(frame, f"People in frame: {person_count}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
    cv2.putText(frame, f"Max people so far: {max_people}", (10, 70),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)

    # Write frame
    out.write(frame)
    frame_count += 1
    print(f"Frame {frame_count}: {person_count} people detected")

# -----------------------------
# --- Release Video ---
# -----------------------------
cap.release()
out.release()

print("Processing completed. Output saved as:", OUTPUT_PATH)
print("Total people in crowd", max_people)