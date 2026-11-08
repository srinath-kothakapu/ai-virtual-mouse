# AI Virtual Mouse

A webcam-based hand-tracking prototype using OpenCV and MediaPipe. The current
code detects hands and draws their landmarks in a live camera window. Mouse
cursor movement and gesture-based clicks are not implemented yet.

## Requirements

- Python
- A webcam

## Setup

```bash
python -m venv .venv
```

Activate the virtual environment, then install the dependencies:

```bash
python -m pip install -r requirements.txt
```

## Run

Start hand tracking:

```bash
python hand_tracking.py
```

Press `q` in the camera window to exit. To check the webcam by itself, run:

```bash
python camera_test.py
```

## Files

- `hand_tracking.py` — detects hands and renders their landmarks.
- `camera_test.py` — verifies that the default camera can be opened.
- `test.py` — basic Python interpreter check.

The scripts use camera device `0` by default. Change the `VideoCapture(0)` value
if your webcam uses a different device index.
