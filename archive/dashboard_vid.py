import streamlit as st
import cv2
import numpy as np
from PIL import Image
from ultralytics import YOLO
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase, RTCConfiguration
import av

# Load YOLOv8 model
model = YOLO("yolov8n.pt")  # Ensure the model path is correct

# Streamlit title
st.title("Real-Time YOLOv8 Object Detection")

# RTC Configuration for WebRTC
RTC_CONFIGURATION = RTCConfiguration({
    "iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]
})

class VideoProcessor(VideoProcessorBase):
    def __init__(self):
        self.model = model

    def recv(self, frame: av.VideoFrame) -> av.VideoFrame:
        img = frame.to_ndarray(format="bgr24")
        frame_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # Perform inference on the frame
        results = self.model(frame_rgb, imgsz=640)

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
                label = f"{self.model.names[cls]} {conf:.2f}"
                cv2.rectangle(img, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
                cv2.putText(img, label, (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # Convert frame to av.VideoFrame
        return av.VideoFrame.from_ndarray(img, format="bgr24")

# Streamlit WebRTC streamer
webrtc_streamer(
    key="example",
    video_processor_factory=VideoProcessor,
    rtc_configuration=RTC_CONFIGURATION,
    media_stream_constraints={"video": True, "audio": False}
)
