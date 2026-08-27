# 📡 Spatial Scanning using Time-of-Flight (ToF) Sensor

A low-cost spatial scanning system built using a **VL53L0X Time-of-Flight sensor**, **Arduino Uno**, and a **Python-based GUI**. The system performs **1D, 2D, and basic 3D scanning** by combining precise distance measurement with controlled motion using servo and stepper motors.

---

## 🎥 Demo Video

A short demonstration of the system performing real-time spatial scanning:

[Watch Demo Video](./Demo_video)

---

## 🚀 Features

- 📏 Accurate distance measurement using ToF technology  
- 🔄 Multi-axis scanning (servo + stepper integration)  
- 🧠 Real-time data acquisition via Arduino  
- 💻 Python GUI for control and visualization  
- 📊 Live plotting using Matplotlib  
- 📡 Serial communication using PySerial  

---

## 🛠️ Tech Stack

### Hardware
- Arduino Uno  
- VL53L0X ToF Sensor  
- Servo Motor (SG90)  
- Stepper Motor (28BYJ-48 + ULN2003 Driver)  

### Software
- Arduino IDE (C/C++)  
- Python  
  - Tkinter (GUI)  
  - PySerial (communication)  
  - Matplotlib (visualization)  

---

## ⚙️ How it Works

1. The ToF sensor emits infrared light pulses and measures the return time to calculate distance.  
2. A servo motor controls vertical scanning angles.  
3. A stepper motor controls horizontal rotation.  
4. Arduino collects distance data and sends it to the computer via serial communication.  
5. A Python GUI reads this data and visualizes it in real time.  

---

## 📊 Output

- **1D Scanning** → Distance vs angle  
- **2D Mapping** → Surface scan (polar/grid)  
- **Basic 3D Representation** → Point cloud approximation  

---

## 📂 Project Structure
```
├── Arduino/
│ └── tof_scanner.ino
├── Python/
│ ├── gui.py
│ ├── serial_handler.py
│ └── visualization.py
├── demo_video.mp4
├── README.md
```
---

## 🔧 Setup & Usage

### 1. Hardware Setup
- Connect VL53L0X sensor via I2C to Arduino  
- Connect servo motor to PWM pin  
- Connect stepper motor via ULN2003 driver  

### 2. Arduino Code
- Upload the `.ino` file using Arduino IDE  

### 3. Python Setup

Install required libraries:

```bash
pip install pyserial matplotlib
```

## 🔮 Future Improvements

- Higher resolution ToF sensors (e.g., 8×8 array sensors)  
- Wireless communication using ESP32  
- Advanced 3D point cloud visualization  
- Mobile app integration (Flutter)  
- SLAM-based mapping  

---

## 📌 Applications

- Robotics navigation & obstacle detection  
- Autonomous systems  
- AR/VR depth sensing  
- Indoor mapping  
- Low-cost LiDAR alternative  

---

## 👥 Contributors

- [Adreet Sarkar](https://github.com/Golden-Adreet)  
- Alok Kumar Pandey  
- Aman Kumar Patel  
- [Aman Upadhyay](https://github.com/amanupadhayay-3009)  
- [Anshuman Pandey](https://github.com/anshuman1947)
