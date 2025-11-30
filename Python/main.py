import cv2
from ultralytics import YOLO
from utils.heatmap import generate_heatmap
from utils.alert import check_crowd_alert


# -----------------------------
# --- YOLO Model ---
# -----------------------------
# ✅ Use built-in yolov8n.pt (auto-downloads if not present)
model = YOLO("yolov8n.pt")  # nano = smallest and fastest


# -----------------------------
# --- Video / Camera ---
# -----------------------------
cap = cv2.VideoCapture(0)  # 0 = default webcam
if not cap.isOpened():
    print("❌ Cannot open webcam")
    exit()


# -----------------------------
# --- Counting Variables ---
# -----------------------------
max_people = 0
frame_count = 0
CROWD_THRESHOLD = 2  # ⚠ Threshold for alert


# -----------------------------
# --- Live Processing Loop ---
# -----------------------------
while True:
    ret, frame = cap.read()
    if not ret:
        break


    frame_count += 1


    # YOLO detection
    results = model(frame)[0]


    person_count = 0
    person_positions = []


    # Loop through detections
    for box, cls in zip(results.boxes.xyxy, results.boxes.cls):
        if int(cls) == 0:  # class 0 = person
            person_count += 1
            x1, y1, x2, y2 = map(int, box)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, "Person", (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
            person_positions.append(((x1 + x2) // 2, (y1 + y2) // 2))


    if person_count > max_people:
        max_people = person_count


    # ⚡ ALERT CHECK
    check_crowd_alert(frame_count, person_count, CROWD_THRESHOLD)


    # Heatmap overlay
    frame = generate_heatmap(frame, person_positions)


    # Display counts
    cv2.putText(frame, f"People: {person_count}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    cv2.putText(frame, f"Max so far: {max_people}", (10, 70),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    cv2.putText(frame, f"Frame: {frame_count}", (10, 110),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)


    # Show live frame
    cv2.imshow("Live Crowd Monitoring", frame)


    # Exit on 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


# -----------------------------
# --- Cleanup ---
# -----------------------------
cap.release()
cv2.destroyAllWindows()
print("✅ Live detection ended. Max people detected:", max_people)