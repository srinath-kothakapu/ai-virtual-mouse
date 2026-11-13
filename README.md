# Hand Tracking Demo (groundwork for an AI virtual mouse)

![CI](https://github.com/srinath-kothakapu/hand-tracking-demo/actions/workflows/ci.yml/badge.svg)

This repository is the first visual hand-tracking stage of an AI virtual mouse idea; it was renamed from `ai-virtual-mouse` because the mouse control is not built yet. It opens a webcam, runs MediaPipe Hands on each captured frame, and draws detected hand landmarks and their connections on the video using OpenCV.

**The current code does not control the operating-system mouse.** It does not move the pointer, recognize click gestures, or send mouse or keyboard events. It is a camera and hand-landmark visualization prototype that provides a base for a future, explicitly implemented gesture-to-pointer feature.

## What the current version does

1. Opens the default webcam (`VideoCapture(0)`).
2. Reads camera frames until the stream ends or the user requests exit.
3. Converts each frame from OpenCV's BGR format to RGB for MediaPipe.
4. Uses MediaPipe Hands to detect hand landmarks when hands are visible.
5. Draws the detected landmarks and the built-in hand-connection graph on the original camera frame.
6. Displays the annotated video in an OpenCV window titled **Hand Tracking**.
7. Releases the camera and closes OpenCV windows when the application exits, including on an error path.

The repository also includes `camera_test.py`, a minimal webcam preview to confirm that OpenCV can open and read the default camera without running hand detection, and an automated test suite in `tests/` that runs the real MediaPipe model on synthetic frames, so it needs no camera.

## Data flow

```text
Webcam frame (BGR)
       │
       ▼
OpenCV converts frame to RGB
       │
       ▼
MediaPipe Hands detects landmarks
       │
       ▼
OpenCV draws landmarks + connections
       │
       ▼
Local preview window
```

The existing scripts process camera frames for the on-screen preview. They do not contain code that stores frames or transmits them to a remote service. Camera permissions and operating-system camera access are still required.

## Requirements

- Python 3.9 to 3.12 (MediaPipe 0.10.21 has no wheels for newer Python versions)
- A webcam or another camera device accessible through OpenCV
- A desktop session capable of opening an OpenCV display window

The project pins these direct dependencies:

| Package | Role |
|---|---|
| `mediapipe==0.10.21` | Hand landmark detection |
| `opencv-python==4.11.0.86` | Camera capture, color conversion, drawing, and display |
| `pytest` | Test runner |

The versions are pinned deliberately. The code uses MediaPipe's `mp.solutions` API, which was removed in later releases (it is gone in 0.10.30 and newer), and newer OpenCV releases require a NumPy version that MediaPipe 0.10.21 does not support. Moving to a newer MediaPipe would mean porting the code to the MediaPipe Tasks `HandLandmarker` API.

## Install

Clone the repository and create an isolated Python environment:

```bash
git clone https://github.com/srinath-kothakapu/hand-tracking-demo.git
cd hand-tracking-demo
python -m venv .venv
```

Activate the environment and install the pinned dependencies:

```bash
# Windows PowerShell
.\.venv\Scripts\Activate.ps1

# macOS / Linux
source .venv/bin/activate

python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

If installation fails, confirm that the selected Python interpreter is supported by the installed MediaPipe wheel for your operating system and CPU architecture. An environment without a graphical desktop may install the libraries but cannot display the preview window.

## Run hand tracking

```bash
python hand_tracking.py
```

Place one or more hands in view of the selected camera. Detected landmarks and the hand skeleton connections are drawn over the live image. Press **q** while the preview window is focused to quit.

The program uses camera index `0` by default. If your device is exposed at a different index, change `cv2.VideoCapture(0)` in `hand_tracking.py` to the index reported by your local setup. The current project does not provide a command-line camera selector.

## Test the camera separately

Before troubleshooting hand detection, verify that the camera can be read by OpenCV:

```bash
python camera_test.py
```

This opens a window titled **Camera Test** and displays the raw frame. Press **q** to close it. The script raises an explicit error if the default camera cannot be opened or a frame cannot be read.

## Run the tests

```bash
python -m pytest
```

The tests feed blank and random-noise frames through the real MediaPipe Hands model and check that the pipeline runs, that nothing is drawn when no hand is found, and that a missing camera raises a clear error. They run on every push through GitHub Actions. They do not measure detection accuracy; there is no hand-detection accuracy evaluation in this repository yet.

## Repository structure

```text
hand_tracking.py    Webcam capture, MediaPipe Hands inference, landmark rendering
camera_test.py      Minimal OpenCV webcam preview without hand inference
tests/              Pipeline smoke tests that run without a camera
requirements.txt    Pinned MediaPipe, OpenCV and pytest dependencies
.github/workflows/  CI that runs the tests on every push
```

## Troubleshooting

- **Could not open the default camera:** allow camera access for your terminal/editor, close other applications using the webcam, and check whether your device uses a different camera index.
- **A preview window opens but frames fail:** check the camera connection and operating-system privacy settings. The script raises a `RuntimeError` when frame capture fails.
- **No landmarks appear:** improve lighting, keep the hand in frame, and make sure it is not heavily occluded. The current scripts do not expose model confidence, detection thresholds, or tracking controls.
- **The window will not start in a headless environment:** use a desktop session with an OpenCV-compatible display backend; this version has no headless output mode.
- **`module 'mediapipe' has no attribute 'solutions'`:** you have a newer MediaPipe than the pinned 0.10.21; reinstall from `requirements.txt` in a fresh environment.
- **Package installation fails:** check the Python version (3.9 to 3.12), operating system, CPU architecture, and wheel availability for both pinned dependencies.

## Scope and next steps

The current version is deliberately limited to displaying hand landmarks. Building a usable virtual mouse would require additional features that are not present, such as:

- Mapping a filtered hand landmark to screen coordinates and calibrating the interaction area.
- Smoothing motion and handling jitter, hand loss, camera movement, and changes in distance.
- Explicit gesture definitions, click-state debouncing, and accidental-activation safeguards.
- An opt-in operating-system input backend for pointer and click events.
- Unit tests for coordinate mapping and gesture state, plus a manual usability evaluation (the existing tests only smoke-test the detection pipeline).
- Clear permission and privacy controls before enabling any input automation.

## Privacy and responsible use

The current scripts display a webcam stream and do not implement recording or remote upload. Camera input is sensitive: use only a camera and environment that you are authorized to access, avoid exposing identifiable people in screenshots or recordings, and close the program when it is no longer needed. No cursor control or gesture-triggered system actions are implemented.

