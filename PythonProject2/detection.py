import streamlit as st
from ultralytics import YOLO
from PIL import Image
import numpy as np
import sqlite3
import os
import cv2

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
model = YOLO("best.pt")

def detection_page():
    st.title("🩸 Malaria Parasite Detection")
    st.markdown("Upload an image or capture using your camera.")

    col1, col2 = st.columns(2)
    image = None

    with col1:
        uploaded_file = st.file_uploader("📤 Upload Image", type=["jpg","png","jpeg"])
        if uploaded_file:
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image", use_container_width=True)
            save_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
            image.save(save_path)

    with col2:
        camera_image = st.camera_input("📸 Capture Image")
        if camera_image:
            image = Image.open(camera_image)
            st.image(image, caption="Captured Image", use_container_width=True)
            save_path = os.path.join(UPLOAD_FOLDER, f"camera_{st.session_state['username']}_{np.random.randint(1000,9999)}.png")
            image.save(save_path)

    if image and st.button("🚀 Run Detection"):
        results = model.predict(np.array(image))
        result_img = results[0].plot()
        st.image(result_img, caption="Detection Result", use_container_width=True)

        boxes = results[0].boxes
        classes_list = boxes.cls.tolist() if boxes is not None and boxes.cls is not None else []
        conf_list = boxes.conf.tolist() if boxes is not None and boxes.conf is not None else []
        has_detections = len(conf_list) > 0 and len(classes_list) > 0

        result_str = str(classes_list) if has_detections else "[]"
        top_conf = float(conf_list[0]) if has_detections else 0.0

        conn = sqlite3.connect("malaria.db")
        c = conn.cursor()
        c.execute("INSERT INTO results (username, image_name, result, confidence) VALUES (?, ?, ?, ?)",
                  (st.session_state["username"], os.path.basename(save_path), result_str, top_conf))
        conn.commit()
        conn.close()
        st.success("✅ Detection result saved")