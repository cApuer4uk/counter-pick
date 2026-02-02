import cv2
from ultralytics import YOLO

# Визуализация результатов
def visualize_results_usual_yolo_inference(
    frame, model, imgsz, conf, iou,
    segment=False, delta_colors=1,
    thickness=2, font_scale=1,
    show_boxes=True, show_confidences=True,
    return_image_array=True
):
    results = model.predict(
        source=frame,
        imgsz=imgsz,
        conf=conf,
        iou=iou,
        verbose=False
    )

    for r in results:
        boxes = r.boxes
        for box in boxes:
            cls_id = int(box.cls[0])
            conf_val = float(box.conf[0])
            xyxy = box.xyxy[0].cpu().numpy().astype(int)

            x1, y1, x2, y2 = xyxy
            label = model.names[cls_id]
            color = (0, 255, 0)

            if show_boxes:
                cv2.rectangle(frame, (x1, y1), (x2, y2), color, thickness)

            if show_confidences:
                text = f'{label} {conf_val:.2f}'
                cv2.putText(frame, text, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, font_scale, color, 2)

    return frame if return_image_array else None


# ==== НАСТРОЙКИ ====
imgsz = 640
conf = 0.7
iou = 0.7

# Загружаем модель
model = YOLO('../ml/runs/detect/train/weights/best.pt')

# === путь к видео (У ТЕБЯ НА ДИСКЕ W:) ===
video_path = '/mnt/w/Wcounterpick/dotatest3.mp4'  # <--- можно поменять на dotatest2 или dotatest3

# Загружаем видео
cap = cv2.VideoCapture(video_path)
if not cap.isOpened():
    print('Cannot open video file')
    exit()

# Настройки выходного видео
fps = cap.get(cv2.CAP_PROP_FPS)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
output_path = '/mnt/w/Wcounterpick/test3_detected.mp4'
out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

# Основной цикл
while True:
    ret, frame = cap.read()
    if not ret:
        print('Video ended or error reading frame.')
        break

    frame = visualize_results_usual_yolo_inference(
        frame, model, imgsz, conf, iou,
        segment=False,  # True если у тебя сегментированная модель
        delta_colors=1,
        thickness=2,
        font_scale=1,
        show_boxes=True,
        show_confidences=True,
        return_image_array=True
    )

    cv2.imshow('RES', frame)
    out.write(frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
out.release()
cv2.destroyAllWindows()
