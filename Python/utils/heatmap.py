import cv2
import numpy as np

def generate_heatmap(frame, person_positions):
    """
    Overlay heatmap based on detected person positions with semi-transparent effect.

    Args:
        frame: current video frame
        person_positions: list of (x, y) tuples for detected people

    Returns:
        annotated_frame: frame with heatmap overlay
    """
    overlay = frame.copy()

    for (cx, cy) in person_positions:
        # Draw filled circle for each person
        cv2.circle(overlay, (cx, cy), 20, (0, 0, 255), -1)

    # Blend original frame and overlay (alpha = transparency)
    alpha = 0.4
    annotated_frame = cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0)

    return annotated_frame