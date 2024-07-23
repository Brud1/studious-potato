import streamlit as st
import cv2
from PIL import Image
from ultralytics import YOLO
import numpy as np

st.title("Camera Feed with YOLOv8 Object Detection")

# Load YOLOv8 model
model = YOLO("yolov8n.pt")  # Ensure the model path is correct

# Streamlit camera input widget
camera_input = st.camera_input("Take a picture")

if camera_input:
    # Read the image from the camera input
    image = Image.open(camera_input)
    frame = np.array(image)

    # Convert frame to RGB for YOLO
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Perform inference on the frame
    results = model(frame_rgb, imgsz=640)  # Adjust size as needed

    # Process the results
    for result in results:
        boxes = result.boxes
        for box in boxes:
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
    st.image(image, use_column_width=True)
