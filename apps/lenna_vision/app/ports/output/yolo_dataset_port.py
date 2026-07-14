from abc import ABC, abstractmethod


class YoloDatasetPort(ABC):
    @abstractmethod
    def get_dataset_yaml_path(self) -> str:
        """YOLO 학습에 필요한 data.yaml 절대 경로를 반환한다."""
