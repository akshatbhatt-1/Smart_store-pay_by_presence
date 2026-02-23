# Smart_store-pay_by_presence

A Computer Vision Based Automated Retail Checkout System

## Overview

Pay-By-Presence is a multi-modal computer vision system that performs automatic customer identification and product billing inside a retail store without manual checkout.
The system combines **face recognition**, **object detection**, and **weight verification** to determine who picked which item and automatically add it to the customer’s cart.

The goal is to remove queues, billing counters, and human intervention while maintaining billing accuracy and theft prevention.

---

## Key Features

* Automatic customer identification using face recognition
* Real-time product detection using deep learning
* Weight sensor confirmation for pickup verification
* Multi-camera tracking of customers and products
* Automatic cart creation and billing
* No QR scanning or barcode scanning required
* Anti-theft verification (vision + weight fusion)

---

## System Workflow

1. Customer registers on the website.
2. Customer enters the store.
3. Entry camera recognizes the customer’s face.
4. A virtual cart is created for that person.
5. Shelf camera monitors products continuously.
6. When a product is picked:

   * Object detection identifies the item.
   * Weight sensor confirms the pickup.
7. The item is assigned to the nearest identified person.
8. The product is added to the user’s cart automatically.
9. Customer leaves the store.
10. Final bill is generated and payment can be processed digitally.

---

## Technologies Used

### Programming

* Python 3.10+

### Computer Vision

* OpenCV
* InsightFace (face embeddings and recognition)
* YOLO (real-time object detection)

### Machine Learning

* Deep learning based object classification
* Face embedding matching

### Hardware

* USB Cameras (multiple streams)
* Load Cell + HX711 Weight Sensor
* Microcontroller (Arduino/ESP)

### Other Libraries

* NumPy
* SciPy
* Mediapipe (optional tracking support)
* PySerial (sensor communication)

---

## Project Architecture

The system consists of three parallel subsystems:

### 1. Face Recognition Module

Identifies each person entering the store and assigns a persistent identity.

### 2. Object Detection Module

Detects products picked from shelves using YOLO real-time detection.

### 3. Pickup Verification Module

Uses a load cell to verify that a physical object was removed and prevent false positives from vision alone.

The final decision engine fuses:

```
Person ID + Detected Object + Weight Change
```

to update the billing cart.

---

---

## Installation

### 1. Clone the repository

```
git clone https://github.com/YOUR_USERNAME/pay-by-presence.git
cd pay-by-presence
```

### 2. Create virtual environment

```
python3.11 -m venv venv
```

Windows:

```
venv\Scripts\activate
```

Linux/macOS:

```
source venv/bin/activate
```

### 3. Install dependencies

```
pip install -r requirements.txt
```

---

## Required External Files (Important)

The repository does NOT include large files.

You must download them separately:

### Model Weights

Download YOLO weights from:

```
[ADD GOOGLE DRIVE LINK]
```

Place inside:

```
/weights
```

### Face Embeddings

After registering users, embeddings will automatically generate inside:

```
/embeddings
```

---

## Running the System

Connect:

* Cameras
* Weight sensor (HX711 via serial)

Then run:

```
python main.py
```

If cameras are in different indices, update them inside:

```
initialize_camera.py
```

---

## Hardware Setup

* Load cell connected to HX711 amplifier
* HX711 connected to Arduino
* Arduino sends weight data over Serial (9600 baud)
* Python reads data using PySerial

---

## Current Limitations

* Works best under consistent lighting
* Requires initial face registration
* Requires calibrated shelf weight
* Similar-looking people may reduce confidence accuracy

---

## Future Improvements

* Payment gateway integration
* Mobile app support
* Multiple shelf support
* RFID fusion
* Store analytics dashboard
* Edge GPU acceleration

---

## Research Contribution

This project demonstrates a low-cost alternative to Amazon Go-style checkout systems using only commodity hardware and open-source deep learning frameworks.

---

## Authors

Akshat Bhatt
B.Tech Computer Science (AI & ML)

(You may add team members here)

---

## License

This project is for academic and research purposes.
