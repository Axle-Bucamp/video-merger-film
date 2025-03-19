import cv2
import numpy as np

def resize_frame(frame, target_shape):
    """Resizes a given frame to the target shape (width, height)."""
    return cv2.resize(frame, target_shape, interpolation=cv2.INTER_AREA)

def resize_video(input_path, output_path, target_shape):
    """Resizes an entire video to a given resolution."""
    cap = cv2.VideoCapture(input_path)
    
    if not cap.isOpened():
        print(f"Error: Could not open {input_path}")
        return

    fps = int(cap.get(cv2.CAP_PROP_FPS))
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    width, height = target_shape  # Ensure width and height are extracted correctly

    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))  # Fix: Pass (width, height)

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        resized_frame = resize_frame(frame, (width, height))  # Ensure correct shape
        out.write(resized_frame)

    cap.release()
    out.release()
    print(f"Resized video saved as {output_path}")

resize_video("data/video/two.mp4", "data/video/two-resized.mp4", (1280, 720))
