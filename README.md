# 🚗 Thai License Plate Recognition & Management System

A Python-based real-time License Plate Recognition (LPR) system using OpenCV and EasyOCR with Thai language support.

This system:
- Detects license plates using OpenCV
- Reads Thai license plates using EasyOCR
- Displays results in real-time
- Stores recognized plates in MySQL
- Provides CRUD functionality via Tkinter GUI
- Supports access control (Allowed / Denied)

---

## 👨‍💻 Author

Sheshehang Limbu  
Thailand License Plate Recognition Project  

---

## 🚀 Features

- 🎥 Real-time camera detection
- 🇹🇭 Thai OCR support (EasyOCR)
- 🖥 Tkinter GUI interface
- 🗄 MySQL database integration
- ➕ Add / Remove license plates (CRUD)
- ✅ Access control system
- 🔴 Live display with Thai font rendering
- 📦 Multiple system versions (Standalone, GUI + DB, Access Control)

---

## 🛠 Tech Stack

- Python 3.x
- OpenCV
- EasyOCR
- Tkinter
- MySQL
- Pillow (PIL)
- NumPy
- Imutils

---

## 📂 Project Structure

.
├── license_plate_app.py
├── standalone_recognition.py
├── access_control_gui.py
├── font/
│   └── THSarabunNew.ttf
├── database/
│   └── licenseDB.sql
├── requirements.txt
└── README.md

---

## 🧠 How It Works

1. Capture video frame from webcam
2. Convert to grayscale
3. Apply bilateral filter
4. Detect edges (Canny)
5. Find contours
6. Extract rectangular region (license plate)
7. Apply EasyOCR (Thai model)
8. Display detected number
9. Insert into MySQL database
10. Allow or deny access based on stored records

---

## 🗄 Database Setup

Create database:

CREATE DATABASE licenseDB;

Create table:

CREATE TABLE LicensePlateData (
    id INT AUTO_INCREMENT PRIMARY KEY,
    license_number VARCHAR(20) NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

Update connection in code:

self.db_connection = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="YOUR_PASSWORD",
    database="licenseDB"
)

---

## 📦 Installation

1️⃣ Create virtual environment:

python -m venv venv
source venv/bin/activate

2️⃣ Install dependencies:

pip install -r requirements.txt

3️⃣ Run application:

python license_plate_app.py

Press:
q → to quit camera

---

## 📄 Requirements.txt

opencv-python
easyocr
numpy
imutils
pillow
mysql-connector-python

---

## 🎯 Modes Available

### 1️⃣ Standalone Recognition
- Detects and displays Thai plates
- No database storage

### 2️⃣ Recognition + MySQL Storage
- Stores detected plates
- Logs access attempts

### 3️⃣ Access Control System
- Pre-register allowed plates
- Shows:
  - “You are allowed to enter”
  - “Access Denied”
- Displays Thai message:
  - ยินดีต้อนรับ (Welcome)

---

## 🔤 Thai Font Setup

Make sure font path is correct:

font_path = "path/to/THSarabunNew.ttf"

Without correct font path, Thai text will not render properly.

---

## ⚠️ Important Notes

- Ensure webcam is connected
- Install Tesseract if needed for EasyOCR backend
- Make sure MySQL server is running
- Close camera properly using 'q'
- Adjust Canny thresholds for better detection
- Performance depends on lighting conditions

---

## 📈 Future Improvements

- Add license plate image saving
- Add admin dashboard
- Add search & filter in GUI
- Deploy with REST API (FastAPI)
- Replace EasyOCR with custom-trained YOLO model
- Add confidence score filtering
- Add duplicate detection prevention
- Dockerize entire system

---

## 🔒 Security Notes

- Use secure MySQL credentials
- Do not use empty root password in production
- Add duplicate check before DB insert
- Add database indexing on license_number
- Add logging system

---

## 📜 License

Copyright (c) 2026 Sheshehang Limbu (HunterVinic)

All rights reserved.

This software may not be copied, modified, or distributed
without explicit permission from the author.

---

## 🎥 Demo Flow

1. Start camera
2. Detect Thai plate
3. OCR reads number
4. System checks database
5. Displays:
   - Green → Access granted
   - Red → Access denied
6. Plate stored in database

---

## 🏆 Project Type

Computer Vision + OCR + Database + GUI Integration Project  
Suitable for:
- Smart parking systems
- Gated communities
- Security checkpoints
- University projects
- Portfolio demonstrations
