from flask import Flask, Response, jsonify, request, render_template
from flask_cors import CORS
import cv2
import threading
import numpy as np
from ultralytics import YOLO
from utils.heatmap import generate_heatmap
from utils.alert import check_crowd_alert

# -----------------------------
# --- YOLO Model ---
# -----------------------------
try:
    model = YOLO("yolov8n.pt")  # auto-download if missing
except Exception as e:
    print("❌ Error loading YOLO model:", e)
    raise

# -----------------------------
# --- Flask App ---
# -----------------------------
app = Flask(__name__)
CORS(app)

# -----------------------------
# --- Global Variables ---
# -----------------------------
latest_count_lock = threading.Lock()
latest_count = 0
CROWD_THRESHOLD = 5
processing = True
video_source = 0  # default camera

# -----------------------------
# --- Detection Function ---
# -----------------------------
def detect_frame(frame):
    global latest_count
    try:
        results = model(frame)[0]
    except Exception as e:
        print("Error in model detection:", e)
        return frame, 0

    person_count = 0
    person_positions = []

    for box, cls in zip(results.boxes.xyxy, results.boxes.cls):
        if int(cls) == 0:  # person class
            person_count += 1
            x1, y1, x2, y2 = map(int, box)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, "Person", (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
            person_positions.append(((x1 + x2) // 2, (y1 + y2) // 2))

    check_crowd_alert(0, person_count, CROWD_THRESHOLD)
    frame = generate_heatmap(frame, person_positions)

    with latest_count_lock:
        latest_count = person_count

    return frame, person_count

# -----------------------------
# --- Video Generator ---
# -----------------------------
def video_generator(source=0):
    cap = cv2.VideoCapture(source)
    if not cap.isOpened():
        print("⚠️ Cannot open video source:", source)
        # fallback blank frame
        blank_frame = 255 * np.ones((480, 640, 3), dtype=np.uint8)
        while True:
            ret, jpeg = cv2.imencode('.jpg', blank_frame)
            frame_bytes = jpeg.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
        return

    global processing, latest_count
    last_frame = 255 * np.ones((480, 640, 3), dtype=np.uint8)

    while True:
        ret, frame = cap.read()
        if not ret:
            # show last frame if camera fails
            ret, jpeg = cv2.imencode('.jpg', last_frame)
            frame_bytes = jpeg.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
            continue

        if processing:
            annotated, _ = detect_frame(frame)
            last_frame = annotated

        ret, jpeg = cv2.imencode('.jpg', last_frame)
        frame_bytes = jpeg.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

    cap.release()

# -----------------------------
# --- Flask Routes ---
# -----------------------------
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(video_generator(video_source),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/count')
def get_count():
    with latest_count_lock:
        c = latest_count
    return jsonify({"peopleCount": int(c)})

@app.route('/start_stream', methods=['POST'])
def start_stream():
    global processing
    processing = True
    return jsonify({"status": "started"})

@app.route('/stop_stream', methods=['POST'])
def stop_stream():
    global processing
    processing = False
    return jsonify({"status": "stopped"})

@app.route('/set_threshold', methods=['POST'])
def set_threshold():
    global CROWD_THRESHOLD
    data = request.json
    try:
        CROWD_THRESHOLD = int(data.get("threshold", CROWD_THRESHOLD))
        return jsonify({"status": "threshold set", "threshold": CROWD_THRESHOLD})
    except:
        return jsonify({"error": "Invalid threshold"}), 400

@app.route('/upload_video', methods=['POST'])
def upload_video():
    file = request.files.get('file')
    if not file:
        return jsonify({"error": "No file uploaded"}), 400

    temp_path = "temp_video.mp4"
    file.save(temp_path)

    cap = cv2.VideoCapture(temp_path)
    max_count_seen = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        _, person_count = detect_frame(frame)
        if person_count > max_count_seen:
            max_count_seen = person_count

    cap.release()
    return jsonify({"max_count_seen": int(max_count_seen)})

@app.route('/health')
def health():
    return jsonify({"status": "ok"})

# -----------------------------
# --- Main ---
# -----------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True, threaded=True)
