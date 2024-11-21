# Face Recognition Authentication System 🤖📸

## Overview

This project is a **Face Recognition Authentication System** that can identify and authenticate individuals using face recognition techniques. It supports:
- **Real-time video-based authentication** 🎥.
- **Group photo-based authentication** 📸.

Built with Python, it leverages the `face_recognition` and `OpenCV` libraries for facial recognition and provides a user-friendly GUI using `Tkinter` 🖥️.

---

## Features ✨

1. **Face Encoding** 🔒:
   - Pre-encodes faces from the `Images` folder.
   - Each file should contain the image of an individual, and the filename should represent their name.

2. **Real-Time Face Recognition** 👀:
   - Uses webcam to authenticate faces in real-time.
   - Recognized faces are highlighted with green boxes ✅, while unrecognized faces are marked with red boxes ❌.

3. **Group Photo Recognition** 👥:
   - Allows users to upload a group photo.
   - Detects and labels known and unknown faces in the image.

4. **Logging** 📝:
   - Logs events such as successful authentications, unrecognized faces, and errors in an `authentication_log.txt` file.

5. **GUI Integration** 🖱️:
   - Provides a Tkinter-based interface for easy navigation.

---

## Setup Instructions ⚙️

1. **Clone the Repository** 📥:
   ```bash
   git clone https://github.com/Riddhi554/Face-Recogniting-Authentication-System.git
   cd Face-Recogniting-Authentication-System
  
2. **Requirements** 📋:
   - Python 3.7 or above
- Libraries:
  - face_recognition
  - numpy
  - opencv-python
  - tkinter
