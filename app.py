from flask import Flask, render_template
from api import get_latest_weather

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/weather")
def weather():

    df = get_latest_weather()

    records = df.to_dict(orient="records")

    return render_template(
        "weather.html",
        records=records
    )

if __name__ == "__main__":
    app.run(debug=True)