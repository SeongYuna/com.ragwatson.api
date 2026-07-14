"""resources/models/model.pt를 로드해 이미지에서 얼굴을 감지하는 어댑터."""
from __future__ import annotations

import logging
from pathlib import Path

import numpy as np
import cv2
from ultralytics import YOLO

from lenna_vision.app.dtos.yolo_inference_dto import (
    DetectedFace,
    YoloInferenceCommand,
    YoloInferenceResult,
)
from lenna_vision.app.ports.output.yolo_inference_port import YoloInferencePort

logger = logging.getLogger(__name__)

_MODEL_PATH = Path(__file__).resolve().parents[4] / "resources" / "models" / "model.pt"


class YoloInferenceAdapter(YoloInferencePort):
    """model.pt를 싱글톤으로 로드해 추론한다."""

    _model: YOLO | None = None

    def _get_model(self) -> YOLO:
        if self._model is None:
            if not _MODEL_PATH.exists():
                raise FileNotFoundError(f"모델 파일 없음: {_MODEL_PATH}")
            logger.info("[YoloInference] 모델 로드: %s", _MODEL_PATH)
            YoloInferenceAdapter._model = YOLO(str(_MODEL_PATH))
        return self._model

    def predict(self, command: YoloInferenceCommand) -> YoloInferenceResult:
        model = self._get_model()

        # bytes → numpy 배열 → OpenCV 이미지
        arr = np.frombuffer(command.image_bytes, np.uint8)
        img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
        if img is None:
            return YoloInferenceResult(
                filename=command.filename,
                faces=[],
                message="이미지를 읽을 수 없습니다.",
            )

        results = model(img, verbose=False)
        probs = results[0].probs  # classify 모델 출력
        top1_idx = int(probs.top1)
        top1_conf = float(probs.top1conf)
        label = model.names[top1_idx]

        faces = [DetectedFace(label=label, confidence=round(top1_conf, 3))]
        message = f"{label} ({round(top1_conf * 100, 1)}%)"

        return YoloInferenceResult(
            filename=command.filename,
            faces=faces,
            message=message,
        )
