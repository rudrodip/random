from flask import Flask, render_template, Response, request
from test import getFrames, getArea

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == 'POST':
      point = request.get_json()
      getArea(point['x'], point['y'])
    return render_template("index.html")


@app.route("/video")
def video():
    return Response(getFrames(), mimetype="multipart/x-mixed-replace; boundary=frame")


if __name__ == "__main__":
    app.run(debug=True)
    # cvThread.start()
