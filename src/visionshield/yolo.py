"""Optional YOLO adapter.

The dependency is loaded only when this adapter is instantiated. This keeps
the deterministic core usable on a Raspberry Pi before model assets exist.
"""

from pathlib import Path
from typing import Any

from .models import ObjectDetection


class YOLODetector:
    """Run an Ultralytics YOLO model and return typed detections.

    Install the optional AI dependencies with ``pip install -e .[ai]`` and
    provide a trained ``.pt`` path. No weights are downloaded implicitly.
    """

    def __init__(self, weights: str | Path, confidence: float = 0.35) -> None:
        if not 0 < confidence <= 1:
            raise ValueError("YOLO confidence must be between 0 and 1.")
        try:
            from ultralytics import YOLO
        except ImportError as exc:
            raise RuntimeError(
                "YOLO support requires optional dependencies: pip install -e .[ai]"
            ) from exc
        self._model = YOLO(str(weights))
        self.confidence = confidence
        self.names: dict[int, str] = getattr(self._model, "names", {})

    def detect(self, image: Any) -> tuple[ObjectDetection, ...]:
        results = self._model.predict(source=image, conf=self.confidence, verbose=False)
        detections: list[ObjectDetection] = []
        for result in results:
            boxes = getattr(result, "boxes", None)
            if boxes is None:
                continue
            for cls, confidence in zip(boxes.cls.tolist(), boxes.conf.tolist()):
                label = self.names.get(int(cls), str(int(cls)))
                detections.append(ObjectDetection(label, float(confidence)))
        return tuple(detections)

    def score(self, frame: Any) -> float:
        detections = self.detect(frame)
        return max((item.confidence for item in detections), default=0.0)
