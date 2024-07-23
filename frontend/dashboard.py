import streamlit as st
import cv2
import numpy as np
from ultralytics import YOLO
from PIL import Image

st.title("Camera Feed with YOLOv8 Object Detection")

# Load YOLOv8 model
model = YOLO("yolov8n.pt")  # Ensure the model path is correct

# Initialize video capture
video_capture = cv2.VideoCapture(0)  # Use 0 for the default camera

if not video_capture.isOpened():
    st.error("Error: Could not open video stream.")
else:
    # Display the video stream
    stframe = st.empty()

    # Loop to capture and process frames
    while True:
        ret, frame = video_capture.read()
        if not ret:
            st.error("Error: Failed to capture image.")
            break
        
        # Perform inference on the frame
        results = model(frame, imgsz=640)  # Adjust size as needed
        
        # Process the results
        for result in results:
            boxes = result.boxes
            for box in boxes:
                # Convert box properties to a list
                xyxy = box.xyxy[0].tolist()  # Convert tensor to list
                conf = box.conf[0].tolist()
                cls = int(box.cls[0].tolist())
                
                if len(xyxy) == 4:
                    x1, y1, x2, y2 = xyxy
                else:
                    continue  # Skip if not enough coordinates are present
                
                # Draw bounding box and label
                label = f"{model.names[cls]} {conf:.2f}"
                cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
                cv2.putText(frame, label, (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # Convert frame to PIL Image for Streamlit
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(frame_rgb)
        
        # Display the frame in Streamlit
        stframe.image(image, use_column_width=True)
    # Release the video capture
    video_capture.release()