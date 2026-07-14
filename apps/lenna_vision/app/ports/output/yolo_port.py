from abc import ABC, abstractmethod

from lenna_vision.app.dtos.yolo_train_dto import YoloTrainCommand, YoloTrainResult


class YoloTrainerPort(ABC):
    """YOLO 모델 훈련을 추상화한 output port.

    ultralytics 의존성은 이 포트를 구현하는 outbound 어댑터에만 존재한다.
    """

    @abstractmethod
    def train(self, yaml_path: str, command: YoloTrainCommand) -> YoloTrainResult:
        """data.yaml 경로와 훈련 파라미터를 받아 파인튜닝을 실행한다."""
