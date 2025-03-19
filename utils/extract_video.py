import cv2

def save_first_frame(video_path, output_image_path):
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("Error: Could not open video.")
        return

    ret, frame = cap.read()  # Read the first frame
    if ret:
        cv2.imwrite(output_image_path, frame)
        print(f"First frame saved as {output_image_path}")
    else:
        print("Error: Could not read the first frame.")

    cap.release()

def save_last_frame(video_path, output_image_path):
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("Error: Could not open video.")
        return

    last_frame = None

    while True:
        ret, frame = cap.read()
        if not ret:
            break  # Break when video ends
        last_frame = frame

    cap.release()

    if last_frame is not None:
        cv2.imwrite(output_image_path, last_frame)
        print(f"Last frame saved as {output_image_path}")
    else:
        print("Error: No frames were read.")

# Example usage
videoin_file = "data/video/input_video.mp4"
videoout_file = "data/video/input_video.mp4"

save_first_frame(videoin_file, "data/frame/first_frame.jpg")
save_last_frame(videoout_file, "data/frame/last_frame.jpg")
