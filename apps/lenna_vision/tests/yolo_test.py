"""YOLO 헬로 월드 — YOLOv8n으로 샘플 이미지 객체 감지 후 결과 화면 출력."""
from ultralytics import YOLO

model = YOLO("yolov8n.pt")  # 최초 실행 시 자동 다운로드 (~6 MB)

results = model("https://ultralytics.com/images/bus.jpg")

results[0].show()  # 바운딩 박스가 그려진 이미지 창 열기
