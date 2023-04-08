from flask import Flask, render_template, request, redirect, url_for, Response
import os
import cv2

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/camera', methods=['GET', 'POST'])
def camera():
    if request.method == 'POST':
        no_cameras = int(request.form.get('no-cameras'))
        for i in range(1, no_cameras+1):
            if 'camera-' + str(i) not in request.files:
                continue
            file = request.files[f'camera-{i}']
            if file.filename == '':
                continue
            filename = f'camera-{i}-{file.filename}'
            file.save(os.path.join("static", filename))
        return redirect(url_for('feed', no_cameras=no_cameras))
    return render_template('camera.html')

# @app.route('/feed/<int:no_cameras>')
@app.route('/feed/<int:no_cameras>')
def feed(no_cameras):
    camera_cards = []
    for i in range(1, no_cameras+1):
        camera_cards.append({
            'title': f'Camera {i}',
            'image_path': ""
        })
    return render_template('feed.html', camera_cards=camera_cards)

def gen_frames():
    # cap = cv2.VideoCapture(0)
    while True:
        # replace "http://ip_address:port/video" with your DroidCam IP address and port
        cap = cv2.VideoCapture(0)

        success, frame = cap.read()

        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            print(ret)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

        cap.release()

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.config['UPLOAD_FOLDER'] = 'uploads'
    app.run(debug=True)
