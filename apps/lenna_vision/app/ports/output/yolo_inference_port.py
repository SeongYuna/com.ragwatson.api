from abc import ABC, abstractmethod

from lenna_vision.app.dtos.yolo_inference_dto import YoloInferenceCommand, YoloInferenceResult


class YoloInferencePort(ABC):
    @abstractmethod
    def predict(self, command: YoloInferenceCommand) -> YoloInferenceResult:
        """이미지 바이트를 받아 감지된 얼굴 목록을 반환한다."""
