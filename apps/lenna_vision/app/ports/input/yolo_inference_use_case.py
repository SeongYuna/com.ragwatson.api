from abc import ABC, abstractmethod

from lenna_vision.app.dtos.yolo_inference_dto import YoloInferenceCommand, YoloInferenceResult


class YoloInferenceUseCase(ABC):
    @abstractmethod
    def predict(self, command: YoloInferenceCommand) -> YoloInferenceResult:
        ...
