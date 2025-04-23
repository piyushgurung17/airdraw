import streamlit as st
import cv2
import numpy as np
import mediapipe as mp
import time

# Page config
st.set_page_config(page_title="Air Drawing Experience", layout="wide")

# Layout: Centered content
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image(
        "https://sdmntpreastus2.oaiusercontent.com/files/00000000-0fac-61f6-8efa-86871580f6d6/raw?se=2025-04-23T16%3A01%3A23Z&sp=r&sv=2024-08-04&sr=b&scid=5025305a-93ba-57d3-a625-338b57b51ede&skoid=2f36945c-3adc-4614-ac2b-eced8f672c58&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2025-04-23T04%3A35%3A55Z&ske=2025-04-24T04%3A35%3A55Z&sks=b&skv=2024-08-04&sig=ANFBoixnIgM2jM4SImr6uLmziqnb/hIrDhmfkFwTV98%3D",
        width=500
    )
    st.title("🪄 Air Drawing Experience")
    st.caption("Use 1 finger to draw. Show 2 fingers to pause. Eraser only removes part of the drawing. Enjoy!")

    # Controls
    run = st.checkbox("📷 Start Webcam")
    color_option = st.radio("🎨 Choose Drawing Color:", ["Red", "Green", "Blue", "Black", "Eraser"])
    thickness = st.slider("✏️ Line Thickness", 3, 20, 10)
    clear_canvas = st.button("🧹 Clear Canvas")
    save_drawing = st.button("💾 Save Drawing")

# Drawing color map
color_map = {
    "Red": (0, 0, 255),
    "Green": (0, 255, 0),
    "Blue": (255, 0, 0),
    "Black": (0, 0, 0),
    "Eraser": (255, 255, 255)
}
draw_color = color_map[color_option]

# Webcam + ML init
frame_placeholder = st.empty()
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)
drawing_utils = mp.solutions.drawing_utils
cap = cv2.VideoCapture(0)

canvas = None
prev_x, prev_y = None, None

# Finger count function
def count_fingers(hand_landmarks, frame_shape):
    tips = [mp_hands.HandLandmark.INDEX_FINGER_TIP,
            mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
    pips = [mp_hands.HandLandmark.INDEX_FINGER_PIP,
            mp_hands.HandLandmark.MIDDLE_FINGER_PIP]
    
    count = 0
    for tip, pip in zip(tips, pips):
        tip_y = hand_landmarks.landmark[tip].y * frame_shape[0]
        pip_y = hand_landmarks.landmark[pip].y * frame_shape[0]
        if tip_y < pip_y:
            count += 1
    return count

# App loop
while run:
    ret, frame = cap.read()
    if not ret:
        st.warning("❌ Cannot grab webcam frame.")
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    # Create canvas once
    if canvas is None:
        canvas = np.ones_like(frame) * 255

    # Only clear when explicitly clicking clear
    if clear_canvas:
        canvas[:, :] = 255
        prev_x, prev_y = None, None

    draw = False

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            fingers_up = count_fingers(hand_landmarks, frame.shape)
            draw = fingers_up == 1  # draw if only 1 finger is up

            index = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            x, y = int(index.x * frame.shape[1]), int(index.y * frame.shape[0])

            if draw:
                if color_option == "Eraser":
                    cv2.circle(canvas, (x, y), thickness, (255, 255, 255), -1)
                elif prev_x is not None and prev_y is not None:
                    cv2.line(canvas, (prev_x, prev_y), (x, y), draw_color, thickness)
                prev_x, prev_y = x, y
            else:
                prev_x, prev_y = None, None

            drawing_utils.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    # Combine canvas + frame
    combined = cv2.addWeighted(frame, 0.7, canvas, 0.3, 0)
    frame_placeholder.image(combined, channels="BGR")

    # Save if requested
    if save_drawing:
        filename = f"drawing_{int(time.time())}.png"
        cv2.imwrite(filename, canvas)
        st.success(f"✅ Drawing saved as `{filename}`")

cap.release()
