# Real-Time Campus Security System

An AI-powered real-time campus security monitoring system developed using **Python**, **Flask**, **OpenCV**, **YOLOv11n**, and **SQLite**.

## Features

- Real-time object detection using YOLOv8
- Multi-object tracking with ByteTrack
- Live surveillance dashboard
- Threat detection (Knife & Gun)
- Automatic alarm activation
- Automatic screenshot capture
- Detection logging using SQLite
- Analytics dashboard
- Secure administrator login

## Technologies Used

- Python 3
- Flask
- OpenCV
- Ultralytics YOLOv11n 
- SQLite
- HTML
- CSS
- JavaScript

## Project Structure

```text
RealTime_Campus_Security_System/
│
├── app.py
├── main.py
├── webcamera.py
├── config.py
├── live_data.json
├── detections.db
│
├── utils/
├── static/
├── templates/
├── captures/
├── logs/
├── models/
└── sounds/
```

## Installation

Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/RealTime_Campus_Security_System.git
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the application

```bash
python app.py
```

Open your browser

```
http://127.0.0.1:5000
```

## Default Login

Username

```
securityadmin
```

Password

```
fuoye2026
```

## Developer

**Waya Oluwafemi Daniel**

Department of Computer Science

Federal University Oye-Ekiti

Final Year Project (CSC 499)

2026

## License

This project was developed for academic purposes.