import cv2
import dlib
from imutils import face_utils
from scipy.spatial import distance as dist
from flask import Flask, render_template, Response

app = Flask(__name__)

def eye_aspect_ratio(eye):
    # Compute the Euclidean distances between the two sets of
    # vertical eye landmarks (x, y)-coordinates
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])

    # Compute the Euclidean distance between the horizontal
    # eye landmark (x, y)-coordinates
    C = dist.euclidean(eye[0], eye[3])

    # Compute the eye aspect ratio
    ear = (A + B) / (2.0 * C)

    # Return the eye aspect ratio
    return ear

def track_alertness():
    video_capture = cv2.VideoCapture(0)

    # Load the facial landmark predictor
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

    EYE_AR_THRESH = 0.2  # Eye aspect ratio threshold for closed eyes
    EYE_AR_CONSEC_FRAMES = 3  # Number of consecutive frames the eye must be below the threshold to trigger an alert
    YAWN_AR_THRESH = 20.0  # Distance threshold between the upper and lower lip for a yawn

    COUNTER = 0
    ALARM_ON = False

    while True:
        ret, frame = video_capture.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces in the grayscale frame
        faces = detector(gray, 0)

        for face in faces:
            # Detect facial landmarks
            shape = predictor(gray, face)
            shape = face_utils.shape_to_np(shape)

            # Extract eye coordinates for eye aspect ratio calculation
            left_eye = shape[36:42]
            right_eye = shape[42:48]

            # Calculate eye aspect ratio for left and right eyes
            left_ear = eye_aspect_ratio(left_eye)
            right_ear = eye_aspect_ratio(right_eye)

            # Average the eye aspect ratio for both eyes
            ear = (left_ear + right_ear) / 2.0

            # Check if the eye aspect ratio is below the threshold
            if ear < EYE_AR_THRESH:
                COUNTER += 1

                # If the eyes have been closed for a sufficient number of frames, sound the alarm
                if COUNTER >= EYE_AR_CONSEC_FRAMES:
                    cv2.putText(frame, "Eye Closed!", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                    ALARM_ON = True

            else:
                COUNTER = 0
                ALARM_ON = False

            # Calculate the distance between the upper and lower lip
            mouth = shape[48:68]
            mar = dist.euclidean(mouth[2], mouth[10])

            # Check if the mouth is open wide enough to indicate a yawn
            if mar > YAWN_AR_THRESH:
                cv2.putText(frame, "Yawning!", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                ALARM_ON = True

        # Display the frame
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    video_capture.release()
    cv2.destroyAllWindows()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(track_alertness(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
