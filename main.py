import cv2
import time
from flask import Flask, Response, render_template, request, make_response

app = Flask(__name__)

USERNAME = 'lf'
PASSWORD = 'lf'

num_cameras = 0
while True:
    camera = cv2.VideoCapture(num_cameras)
    if not camera.isOpened():
        break
    else:
        camera.release()
        num_cameras += 1

def generate_frames(camera):
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            # Encode the frame as JPEG
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

            yield(b'--frame\r\n'
                  b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    auth = request.authorization
    if not auth or not (auth.username == USERNAME and auth.password == PASSWORD):
        # Return a 401 Unauthorized error
        return make_response('Could not verify your login!', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})
    else:
        # Render the index template with the video stream
        return render_template('index.html', num_cameras=num_cameras)

@app.route('/video_feed/<int:camera_id>')
def video_feed(camera_id):
    # Check if the user is authenticated
    auth = request.authorization
    if not auth or not (auth.username == USERNAME and auth.password == PASSWORD):
        # Return a 401 Unauthorized error
        return make_response('Could not verify your login!', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})
    else:
        # Stream the video from the specified webcam
        camera = cv2.VideoCapture(camera_id)
        return Response(generate_frames(camera), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
