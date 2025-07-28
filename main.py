import tkinter as tk
from tkinter import messagebox
import pandas as pd
import numpy as np
import requests
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from datetime import datetime, timedelta
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# === ThingSpeak Settings ===
CHANNEL_ID = ' 3007093'
READ_API_KEY = 'ES14NX9UOAFB95Q6'
TEMP_FIELD = 1
HUMIDITY_FIELD = 2

# === Fetch Data ===
def fetch_data(field_num):
    url = f'https://api.thingspeak.com/channels/{CHANNEL_ID}/fields/{field_num}.json?api_key={READ_API_KEY}&results=800'
    response = requests.get(url)
    if response.status_code != 200:
        return None
    data = response.json().get('feeds', [])
    if not data:
        return None
    df = pd.DataFrame(data)
    df['created_at'] = pd.to_datetime(df['created_at'])
    df['value'] = pd.to_numeric(df[f'field{field_num}'], errors='coerce')
    df = df.dropna().sort_values('created_at')
    df['timestamp'] = (df['created_at'] - df['created_at'].min()).dt.total_seconds() / 3600
    return df[['timestamp', 'value', 'created_at']]

# === Train Model ===
def train_model(df):
    X = df[['timestamp']]
    y = df['value']
    model = LinearRegression()
    model.fit(X, y)
    return model

# === Predict Future ===
def predict_future(model, last_timestamp, hours, reference_time):
    future_timestamps = np.arange(last_timestamp + 1, last_timestamp + hours + 1).reshape(-1, 1)
    future_df = pd.DataFrame(future_timestamps, columns=['timestamp'])
    predictions = model.predict(future_df)
    future_times = [reference_time + timedelta(hours=int(h - last_timestamp)) for h in future_timestamps.flatten()]
    return future_times, predictions

# === Rain Prediction Rule ===
def should_rain(predicted_temp):
    return ["Yes there are rain chances" if t < 28 else "no rain chances" for t in predicted_temp]

# === Plot Graphs ===
def plot_prediction(hours):
    temp_df = fetch_data(TEMP_FIELD)
    hum_df = fetch_data(HUMIDITY_FIELD)
    if temp_df is None or hum_df is None or temp_df.empty or hum_df.empty:
        return

    temp_model = train_model(temp_df)
    hum_model = train_model(hum_df)

    temp_times, temp_preds = predict_future(temp_model, temp_df['timestamp'].iloc[-1], hours, temp_df['created_at'].iloc[-1])
    hum_times, hum_preds = predict_future(hum_model, hum_df['timestamp'].iloc[-1], hours, hum_df['created_at'].iloc[-1])

    rain_status = should_rain(temp_preds)

    fig, axs = plt.subplots(1, 2, figsize=(12, 4), dpi=100)
    month_year = temp_times[0].strftime("%B %Y")
    fig.suptitle(f"Weather Forecast - {month_year}", fontsize=14, fontweight='bold')

    axs[0].plot(temp_df['created_at'].dt.strftime('%d'), temp_df['value'], label="Actual Temp", color='blue')
    axs[0].plot([d.strftime('%d') for d in temp_times], temp_preds, label="Predicted Temp", color='red', linestyle='--')
    axs[0].set_title("Temperature")
    axs[0].set_xlabel("Date")
    axs[0].set_ylabel("°C")
    axs[0].legend()
    axs[0].grid(True)

    axs[1].plot(hum_df['created_at'].dt.strftime('%d'), hum_df['value'], label="Actual Humidity", color='green')
    axs[1].plot([d.strftime('%d') for d in hum_times], hum_preds, label="Predicted Humidity", color='orange', linestyle='--')
    axs[1].set_title("Humidity")
    axs[1].set_xlabel("Date")
    axs[1].set_ylabel("%")
    axs[1].legend()
    axs[1].grid(True)

    for widget in plot_frame.winfo_children():
        widget.destroy()

    canvas = FigureCanvasTkAgg(fig, master=plot_frame)
    canvas.draw()
    canvas.get_tk_widget().pack()

    summary = "🌧️ Rain Prediction (Next {} Hours):\n".format(hours)
    for i in range(len(temp_times)):
        summary += "{} - {}\n".format(temp_times[i].strftime("%d %b"), rain_status[i])

    result_label.config(text=summary)

# === GUI Setup ===
root = tk.Tk()
root.title("Weather Forecast Dashboard")
root.geometry("1100x700")
root.configure(bg="#eef6fb")

tk.Label(root, text="🌦️ Weather Forecast Dashboard", font=("Helvetica", 20, "bold"), bg="#eef6fb", fg="#333").pack(pady=20)

btn_frame = tk.Frame(root, bg="#eef6fb")
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="Predict Next Day", width=20, command=lambda: plot_prediction(24), bg="skyblue", font=("Arial", 12)).grid(row=0, column=0, padx=10)
tk.Button(btn_frame, text="Predict Next Week", width=20, command=lambda: plot_prediction(24 * 7), bg="lightgreen", font=("Arial", 12)).grid(row=0, column=1, padx=10)
tk.Button(btn_frame, text="Predict Next Month", width=20, command=lambda: plot_prediction(24 * 30), bg="orange", font=("Arial", 12)).grid(row=0, column=2, padx=10)

plot_frame = tk.Frame(root, bg="#ffffff", bd=2, relief="groove")
plot_frame.pack(fill="both", expand=True, padx=20, pady=20)

result_label = tk.Label(root, text="", bg="#eef6fb", font=("Arial", 12), justify="left")
result_label.pack(pady=10)

root.mainloop()
