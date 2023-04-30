import cv2
from flask import Flask, Response

# Créer une instance de l'application Flask
app = Flask(__name__)

# Définir la source de la vidéo
video_capture = cv2.VideoCapture(0)

# Fonction pour la lecture de la vidéo et l'envoi du flux en continu
def generate_frames():
    while True:
        # Capture d'une trame de la vidéo
        success, frame = video_capture.read()
        if not success:
            break
        else:
            # Encodage de la trame en jpg
            ret, buffer = cv2.imencode('.jpeg', frame)
            frame = buffer.tobytes()

            # Envoi de la trame
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# Route de l'application pour la lecture du flux vidéo
@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

# Démarrer l'application Flask
if __name__ == '__main__':
    app.run(debug=True)