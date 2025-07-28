
# 🌤️ IoT-Based Weather Forecasting and Rain Prediction System

This project combines an ESP32 microcontroller with a DHT22 sensor and a Python GUI to create a real-time weather monitoring and forecasting dashboard. It uploads temperature and humidity data to ThingSpeak and uses Machine Learning to predict future weather trends and chances of rain.

---

## 📌 Features

- Real-time data logging (temperature & humidity) using ESP32 and DHT22.
- Data visualization and prediction using Python (Tkinter + Matplotlib).
- Predicts weather trends for:
  - Next Day (24 hours)
  - Next Week (7 days)
  - Next Month (30 days)
- Simple rule-based rain prediction logic.
- Uses Linear Regression for forecasting trends.

---

## 🧰 Tech Stack

### ⚙️ Hardware
- ESP32 Microcontroller
- DHT22 Temperature and Humidity Sensor

### 🖥️ Software
- Arduino (ESP32) using `main.ino`
- Python with:
  - `Tkinter` (GUI)
  - `pandas`, `numpy`, `scikit-learn`
  - `matplotlib` for plotting
  - `requests` for ThingSpeak API

---

## 🔌 Setup Instructions

### 1. ESP32 Firmware (main.ino)
#### Libraries Required:
- `WiFi.h`
- `DHT.h`
- `ThingSpeak.h`

#### Steps:
1. Open `main.ino` in Arduino IDE.
2. Connect DHT22 to **GPIO 21** of ESP32.
3. Enter your WiFi credentials:
   ```cpp
   const char* ssid = "YOUR_SSID";
   const char* password = "YOUR_PASSWORD";
   ```
4. Upload the code to ESP32.
5. It reads and uploads data to ThingSpeak every 20 seconds.

---

### 2. Python GUI (main.py)

#### Requirements:
Install the required libraries using pip:
```bash
pip install pandas numpy matplotlib scikit-learn requests
```

#### Run the Dashboard:
```bash
python main.py
```

#### Features:
- Fetches data from ThingSpeak fields.
- Trains a simple regression model.
- Predicts and visualizes:
  - Temperature
  - Humidity
  - Rain forecast (rule-based: if temp < 28°C, then rain likely).

---

## 📊 ThingSpeak Configuration

- **Channel ID**: `2995393`
- **Write API Key (for ESP32)**: `PLU2BL3KFQ7AXOPG`
- **Read API Key (for Python)**: `CEAXKGRIZT8NVBA5`
- **Field 1**: Temperature (°C)
- **Field 2**: Humidity (%)

---

## 🌧️ Rain Prediction Logic

If predicted temperature is **< 28°C**, it indicates possible **rain**. Else, it shows “no rain chances.”

---

## 📸 Screenshots

> You can add screenshots of:
- ESP32 serial monitor
- GUI prediction results
- Graphs for better visualization

---

## 📎 Folder Structure

```
/weather_forecast_project
│
├── main.ino          # ESP32 IoT code (Arduino)
├── main.py           # Python GUI with forecasting
├── README.md         # Project documentation (this file)
```

---

## ✅ Future Enhancements

- Use more advanced forecasting models (e.g., LSTM).
- Add real-time notifications or SMS alerts.
- Use rain sensors for real rain validation.

---

## 👩‍💻 Developed By

- **[Your Name]** – ESP32 + Python Integration
- **Platform** – [ThingSpeak](https://thingspeak.com)

---

## 📬 Contact

For queries or collaborations, feel free to reach out via [maddy@makeskilled.com].
