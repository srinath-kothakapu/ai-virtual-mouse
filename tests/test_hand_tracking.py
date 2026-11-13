"""Smoke tests that run the real MediaPipe Hands model on synthetic frames (no camera needed)."""

import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import hand_tracking  # noqa: E402


@pytest.fixture(scope="module")
def detector():
    with hand_tracking.mp_hands.Hands(static_image_mode=True) as hands:
        yield hands


def test_blank_frame_has_no_hands_and_is_left_unchanged(detector):
    frame = np.zeros((240, 320, 3), dtype=np.uint8)
    out, count = hand_tracking.annotate_frame(detector, frame)
    assert count == 0
    assert out.shape == (240, 320, 3)
    assert not out.any()  # nothing drawn when no hand is found


def test_noise_frame_runs_through_the_pipeline(detector):
    rng = np.random.default_rng(0)
    frame = rng.integers(0, 256, size=(240, 320, 3), dtype=np.uint8)
    out, count = hand_tracking.annotate_frame(detector, frame)
    assert out.shape == (240, 320, 3)
    assert count >= 0


def test_main_reports_missing_camera(monkeypatch):
    class NoCamera:
        def __init__(self, *_):
            pass

        def isOpened(self):
            return False

    monkeypatch.setattr(hand_tracking.cv2, "VideoCapture", NoCamera)
    with pytest.raises(RuntimeError, match="default camera"):
        hand_tracking.main()
