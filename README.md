✨ Air Drawing Experience
A fun and interactive Streamlit-based web app that lets you draw in the air using your fingers and a webcam! Powered by MediaPipe and OpenCV, this app detects hand gestures and converts them into real-time air drawings—no touchscreen required!

🎯 Features
🖐️ 1 Finger to draw

✌️ 2 Fingers to pause drawing

🧽 Eraser to selectively erase parts of your sketch

🎨 Select from Red, Green, or Blue drawing colors

📷 Real-time hand tracking with your webcam

🚀 How It Works
Launch the app using Streamlit.

Click Start Webcam.

Use your index finger to draw in the air.

Show two fingers to stop drawing temporarily.

Choose your favorite color to sketch freely in 3D space!

🧰 Tech Stack
Python 3.10+

Streamlit

MediaPipe

OpenCV

NumPy

⚙️ Installation
bash
Copy
Edit
git clone https://github.com/your-username/air-drawing-app.git
cd air-drawing-app
pip install -r requirements.txt
streamlit run try.py
🛠 Troubleshooting
❌ ImportError: libGL.so.1: cannot open shared object file
To resolve this on Linux servers (like Streamlit Cloud), run:

bash
Copy
Edit
sudo apt-get update
sudo apt-get install -y libgl1-mesa-glx
📸 Example
(Insert your animated GIF or screenshot here to showcase the app in action)

🙌 Acknowledgements
MediaPipe by Google for hand tracking

OpenCV for real-time image processing

Streamlit for easy web UI
