import cv2
from flask import Flask, Response, render_template, request, make_response

app = Flask(__name__)

# Set your username and password
USERNAME = 'lf'
PASSWORD = 'lf'

# Initialize the webcam
camera = cv2.VideoCapture(0)


def generate_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            # Encode the frame as JPEG
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/')
def index():
    # Check if the user is authenticated
    auth = request.authorization
    if not auth or not (auth.username == USERNAME and auth.password == PASSWORD):
        # Return a 401 Unauthorized error
        return make_response('Could not verify your login!', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})
    else:
        # Render the index template with the video stream
        return render_template('index.html')


@app.route('/video_feed')
def video_feed():
    # Check if the user is authenticated
    auth = request.authorization
    if not auth or not (auth.username == USERNAME and auth.password == PASSWORD):
        # Return a 401 Unauthorized error
        return make_response('Could not verify your login!', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})
    else:
        # Stream the video from the webcam
        return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
