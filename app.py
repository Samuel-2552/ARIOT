from flask import Flask, render_template, Response
import cv2

app = Flask(__name__)

camera = cv2.VideoCapture(0)  # Initialize camera object

def gen_frames():  # Generate camera frames
    while True:
        success, frame = camera.read()  # Read camera frames
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)  # Encode camera frame as JPEG image
            frame = buffer.tobytes()  # Convert encoded frame to bytes
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # Yield camera frame

@app.route('/')  # Route for home page
def index():
    return render_template('video.html')

@app.route('/video_feed')  # Route for camera feed
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
