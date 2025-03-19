import cv2
import numpy as np

def get_first_frame(video_path):
    """Extracts the first frame of a video."""
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error: Could not open {video_path}")
        return None
    ret, frame = cap.read()
    cap.release()
    return frame if ret else None

def get_last_frame(video_path):
    """Extracts the last frame of a video."""
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error: Could not open {video_path}")
        return None

    last_frame = None
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        last_frame = frame

    cap.release()
    return last_frame

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
    out = cv2.VideoWriter(output_path, fourcc, fps, target_shape)

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        resized_frame = resize_frame(frame, target_shape)
        out.write(resized_frame)

    cap.release()
    out.release()
    print(f"Resized video saved as {output_path}")

def merge_videos(video1_path, video2_path, output_path, target_shape):
    """Resizes and merges two videos with a smooth transition."""
    resized_video1 = "resized_video1.mp4"
    resized_video2 = "resized_video2.mp4"
    
    # Resize both videos to match the target shape
    resize_video(video1_path, resized_video1, target_shape)
    resize_video(video2_path, resized_video2, target_shape)

    cap1 = cv2.VideoCapture(resized_video1)
    cap2 = cv2.VideoCapture(resized_video2)

    if not cap1.isOpened() or not cap2.isOpened():
        print("Error: Could not open resized video files.")
        return

    fps = int(cap1.get(cv2.CAP_PROP_FPS))
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, target_shape)

    # Write first video frames
    while True:
        ret, frame = cap1.read()
        if not ret:
            break
        out.write(frame)

    # Get last frame of first video and first frame of second video
    last_frame_video1 = get_last_frame(resized_video1)
    first_frame_video2 = get_first_frame(resized_video2)

    # Smooth transition (optional blending of frames)
    if last_frame_video1 is not None and first_frame_video2 is not None:
        for alpha in np.linspace(0, 1, num=10):  # Create 10 transition frames
            blended_frame = cv2.addWeighted(last_frame_video1, 1 - alpha, first_frame_video2, alpha, 0)
            out.write(blended_frame)

    # Write second video frames
    while True:
        ret, frame = cap2.read()
        if not ret:
            break
        out.write(frame)

    # Release everything
    cap1.release()
    cap2.release()
    out.release()
    print(f"Merged video saved as {output_path}")

# Example usage
target_resolution = (1280, 720)  # Width x Height
merge_videos("video1.mp4", "video2.mp4", "merged_output.mp4", target_resolution)