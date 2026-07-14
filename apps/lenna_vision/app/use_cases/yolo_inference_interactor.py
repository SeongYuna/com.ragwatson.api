from __future__ import annotations

import logging

from lenna_vision.app.dtos.yolo_inference_dto import YoloInferenceCommand, YoloInferenceResult
from lenna_vision.app.ports.input.yolo_inference_use_case import YoloInferenceUseCase
from lenna_vision.app.ports.output.yolo_inference_port import YoloInferencePort

logger = logging.getLogger(__name__)


class YoloInferenceInteractor(YoloInferenceUseCase):
    def __init__(self, inference_port: YoloInferencePort) -> None:
        self._inference_port = inference_port

    def predict(self, command: YoloInferenceCommand) -> YoloInferenceResult:
        logger.info("[YoloInference] 추론 요청 — file=%s", command.filename)
        result = self._inference_port.predict(command)
        logger.info("[YoloInference] 감지 결과 — %d명", len(result.faces))
        return result
