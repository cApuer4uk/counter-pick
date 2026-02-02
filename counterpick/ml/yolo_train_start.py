from ultralytics import YOLO

model = YOLO("../scripts_for_help/yolov8m.pt")
model.train(data="/home/capu/projects/counterpick/counterpick/ml/data.yaml", epochs=100, imgsz=640)