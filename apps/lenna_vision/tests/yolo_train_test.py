"""YOLO 파인튜닝 실행 테스트 (로컬 resources/yolo_train 데이터셋 사용)."""
from lenna_vision.app.dtos.yolo_train_dto import YoloTrainCommand
from lenna_vision.dependencies.yolo_provider import get_yolo_train_use_case

if __name__ == "__main__":
    use_case = get_yolo_train_use_case()
    result = use_case.train(
        YoloTrainCommand(epochs=5, batch=8, imgsz=640, device=0)
    )
    print(result)
