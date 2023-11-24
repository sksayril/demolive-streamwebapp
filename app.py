from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import cv2
import base64

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
socketio = SocketIO(app)

camera = cv2.VideoCapture(0)  # Access the default camera (change index if needed)

def generate_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = base64.b64encode(buffer).decode('utf-8')
            yield frame

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    emit('start_stream', {'data': 'Camera stream started'})

@socketio.on('request_frame')
def send_frame():
    frame = next(generate_frames())
    emit('update_frame', {'image': frame})

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)

# # from flask import Flask, render_template
# # from flask_socketio import SocketIO, emit
# # import cv2
# # import base64

# # app = Flask(__name__)
# # app.config['SECRET_KEY'] = 'secret'
# # socketio = SocketIO(app)
# # camera = None  # Initialize the camera as None

# # def generate_frames():
# #     global camera
# #     while True:
# #         if camera:
# #             success, frame = camera.read()
# #             if not success:
# #                 break
# #             else:
# #                 ret, buffer = cv2.imencode('.jpg', frame)
# #                 frame = base64.b64encode(buffer).decode('utf-8')
# #                 yield frame

# # @app.route('/')
# # def index():
# #     return render_template('index.html')

# # @socketio.on('connect')
# # def handle_connect():
# #     global camera
# #     if camera is None:
# #         camera = cv2.VideoCapture(0)  # Access the default camera (change index if needed)
# #         emit('start_stream', {'data': 'Camera stream started'})

# # @socketio.on('disconnect')
# # def handle_disconnect():
# #     global camera
# #     if camera:
# #         camera.release()
# #         camera = None

# # @socketio.on('request_frame')
# # def send_frame():
# #     frame = next(generate_frames())
# #     emit('update_frame', {'image': frame})

# # if __name__ == '__main__':
# #     socketio.run(app, host='0.0.0.0', port=5000, debug=True)

# import cv2
# import streamlit as st
# import numpy as np

# # Function to capture frames from the camera
# def capture_video():
#     cap = cv2.VideoCapture(0)
#     if not cap.isOpened():
#         st.error("Cannot access the camera.")
#         return

#     while True:
#         ret, frame = cap.read()
#         if not ret:
#             st.error("Failed to capture frame.")
#             break

#         # Convert the OpenCV frame to RGB format
#         frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

#         # Display the frame in Streamlit
#         st.image(frame, channels="RGB", use_column_width=True)

#         if st.button("Stop"):
#             break

#     cap.release()
#     cv2.destroyAllWindows()

# def main():
#     st.title("Camera Stream")

#     capture_video()

# if __name__ == "__main__":
#     main()

