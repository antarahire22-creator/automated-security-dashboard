from flask import Flask, render_template, request
import os
import pandas as pd

app = Flask(__name__)

@app.route("/")
def home():
   return render_template("index.html")

@app.route("/dashboard")
def dashboard():
    try:
        df = pd.read_csv("uploads/security_logs.csv")

        total_alerts = len(df)
        critical = len(df[df["Severity"] == "Critical"])
        high = len(df[df["Severity"] == "High"])
        medium = len(df[df["Severity"] == "Medium"])
        low = len(df[df["Severity"] == "Low"])

    except:
        total_alerts = 0
        critical = 0
        high = 0
        medium = 0
        low = 0

    return render_template(
        "dashboard.html",
        total_alerts=total_alerts,
        critical=critical,
        high=high,
        medium=medium,
        low=low,
        logs=df.to_dict(orient="records")
    )

@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        file = request.files.get("file")

        if file and file.filename != "":
           filepath = os.path.join("uploads", file.filename)
           file.save(filepath)

           df = pd.read_csv(filepath)
           total_alerts = len(df)
           critical = len(df[df["Severity"] == "Critical"])
           high = len(df[df["Severity"] == "High"])
           medium = len(df[df["Severity"] == "Medium"])
           low = len(df[df["Severity"] == "Low"])
           print(df.head())

           return "File uploaded and saved successfully!"
        else:
           return "Please select a file first."

    return render_template("upload.html")

if __name__ == "__main__":
    app.run(host="127.0.0.1",port=5000,debug=True)