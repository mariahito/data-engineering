
from flask import Flask, jsonify, request
import pandas as pd
from pathlib import Path

app = Flask(__name__)

data_path = Path("/home/jhu/data/combined_data.csv")

# load in csv
df = pd.read_csv(data_path)


@app.route("/")
def home():
    return {"message": "Welcome to the Weather, COVID, and Unemployment API"}

@app.route("/cases-by-state", methods=["GET"])
def cases_by_state():
    result = df.groupby("state")["covid_cases"].sum().reset_index()
    return jsonify(result.to_dict(orient="records"))

@app.route("/avg-unemployment-by-state", methods=["GET"])
def avg_unemployment_by_state():
    result = df.groupby("state")["unemployment_rate"].mean().reset_index()
    return jsonify(result.to_dict(orient="records"))

@app.route("/avg-temp-by-state", methods=["GET"])
def avg_temp_by_state():
    result = df.groupby("state")["Temp"].mean().reset_index()
    return jsonify(result.to_dict(orient="records"))

@app.route("/filter", methods=["GET"])
def filter_data():
    state = request.args.get("state")
    month = request.args.get("month/year")
    filtered_df = df.copy()

    if state:
        filtered_df = filtered_df[filtered_df["state"].str.lower() == state.lower()]
    if month:
        filtered_df = filtered_df[filtered_df["month/year"] == month]

    return jsonify(filtered_df.to_dict(orient="records"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
