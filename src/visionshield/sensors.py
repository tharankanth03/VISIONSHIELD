"""Optional hardware source adapters.

The core agent consumes typed observations. These adapters isolate camera and
thermal hardware dependencies so the fusion logic remains testable on a PC.
"""

from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Protocol

from .models import FrameObservation, ThermalObservation


class RGBSource(Protocol):
    def read(self) -> tuple[Any, datetime]:
        """Return one RGB frame and its UTC capture timestamp."""

    def close(self) -> None:
        """Release the source."""


class ThermalSource(Protocol):
    def read(self) -> tuple[list[float], datetime]:
        """Return one flattened thermal frame and its UTC capture timestamp."""

    def close(self) -> None:
        """Release the source."""


class OpenCVCameraSource:
    """Read RGB frames from a local OpenCV camera device."""

    def __init__(self, device: int = 0, width: int | None = None, height: int | None = None):
        try:
            import cv2
        except ImportError as exc:
            raise RuntimeError("Install optional camera dependencies with: pip install -e .[ai]") from exc
        self._capture = cv2.VideoCapture(device)
        if not self._capture.isOpened():
            self._capture.release()
            raise RuntimeError(f"Unable to open RGB camera device {device}.")
        if width:
            self._capture.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        if height:
            self._capture.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    def read(self) -> tuple[Any, datetime]:
        ok, frame = self._capture.read()
        if not ok:
            raise RuntimeError("RGB camera returned no frame.")
        return frame, datetime.now(timezone.utc)

    def close(self) -> None:
        self._capture.release()


class MLX90640Source:
    """Read flattened frames from an MLX90640 using an injected reader.

    Injecting the reader keeps the hardware library and bus setup outside the
    agent. A production application can pass its configured sensor callable.
    """

    def __init__(self, reader):
        if not callable(reader):
            raise TypeError("MLX90640 reader must be callable.")
        self._reader = reader

    def read(self) -> tuple[list[float], datetime]:
        values = [float(value) for value in self._reader()]
        if len(values) != 32 * 24:
            raise ValueError("MLX90640 frames must contain exactly 768 values.")
        return values, datetime.now(timezone.utc)

    def close(self) -> None:
        return None
