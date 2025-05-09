# Face-Recognition-FrameWork
A Python-based multi-phase face recognition system for business intelligence that enables real-time detection, attendance logging, and cloud integration using OpenCV, FaceRecognition, and Firebase to support automation and smart workplace solutions.
# A Multi-Phase Framework for Face Recognition in Business Intelligence

## 📌 Overview

This project presents a **Multi-Phase Framework for Face Recognition** designed for **Business Intelligence applications** such as automated attendance, access control, and behavioral analytics. It integrates real-time face recognition, data logging, and cloud connectivity to streamline and enhance business operations.

## 🚀 Features

- 🔍 Face detection and recognition using the [FaceRecognition](https://github.com/ageitgey/face_recognition) library
- 🧠 Multi-phase architecture for improved recognition accuracy
- 🎥 Real-time video processing via OpenCV
- 💾 Face encoding storage using Pickle
- ☁️ Integration with Firebase for attendance logs and image uploads
- 📸 Storage of known and unknown face snapshots

## ⚙️ Technologies Used

- Python 3.x
- face_recognition
- OpenCV
- Firebase Admin SDK
- Pickle
- NumPy
- datetime


## ➕🧑‍💼 Add known face images

Place images of known individuals in the known_faces/ directory with filenames as their names (e.g., john_doe.jpg).


## 🔧 Set up Firebase

Create a Firebase project.

Download the service account key JSON file.

Update firebase_config.py with your Firebase details.


## 🧪 How It Works

Phase 1: Detects and encodes faces from a live video stream.

Phase 2: Compares the live encodings with the stored ones.

Phase 3: Logs attendance and uploads images to Firebase based on recognition results.

## 📊 Applications

Office and classroom attendance systems
Secure entry monitoring
Retail and customer analytics
Employee behavior analysis


## 📌 Future Improvements
Add liveness detection to prevent spoofing

Mobile app integration for dashboard access

Expand to support multiple camera feeds


## 📄 License
This project is for educational purposes only.

## 🙌 Acknowledgments
[face_recognition by Adam Geitgey](https://github.com/ageitgey/face_recognition)

Firebase for cloud database and storage





