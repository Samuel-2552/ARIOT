from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/camera', methods=['GET', 'POST'])
def camera():
    if request.method == 'POST':
        no_cameras = int(request.form['no-cameras'])
        for i in range(1, no_cameras+1):
            if f'camera-{i}' not in request.files:
                continue
            file = request.files[f'camera-{i}']
            if file.filename == '':
                continue
            filename = f'camera-{i}-{file.filename}'
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return redirect(url_for('feed', no_cameras=no_cameras))
    return render_template('camera.html')

@app.route('/feed/<int:no_cameras>')
def feed(no_cameras):
    camera_cards = []
    for i in range(1, no_cameras+1):
        camera_cards.append({
            'title': f'Camera {i}',
            'image_path': os.path.join(app.config['UPLOAD_FOLDER'], f'camera-{i}-' + os.listdir(app.config['UPLOAD_FOLDER'])[i-1]),
        })
    return render_template('feed.html', camera_cards=camera_cards)

if __name__ == '__main__':
    app.config['UPLOAD_FOLDER'] = 'uploads'
    app.run(debug=True)
