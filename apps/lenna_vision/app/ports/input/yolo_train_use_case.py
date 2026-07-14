from abc import ABC, abstractmethod

from lenna_vision.app.dtos.yolo_train_dto import YoloTrainCommand, YoloTrainResult


class YoloTrainUseCase(ABC):
    @abstractmethod
    def train(self, command: YoloTrainCommand) -> YoloTrainResult:
        ...
