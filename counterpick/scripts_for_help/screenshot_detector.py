import os
import cv2
import time
import json
from datetime import datetime
from ultralytics import YOLO

# === Пути ===
SAVE_DIR = '/mnt/w/Wcounterpick/tmp_screenshots'
MODEL_PATH = '../ml/runs/detect/train/weights/best.pt'
COUNTERS_PATH = '../app/db/counters.json'

imgsz = 640
conf = 0.7
iou = 0.7

# === Загрузка модели YOLO ===
model = YOLO(MODEL_PATH)

# === Загрузка counters.json ===
with open(COUNTERS_PATH, 'r') as f:
    counters_data = json.load(f)

def get_counter_names(hero_label: str):
    short_name = hero_label.split('_')[0]
    full_name = f"npc_dota_hero_{short_name}"
    for entry in counters_data:
        if entry["hero"] == full_name:
            return [
                counter["counter"].replace("npc_dota_hero_", "")
                for counter in entry["counters"]
            ]
    return []

# === Подготовка видео ===
timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
video_output_path = f'/mnt/w/Wcounterpick/detected_{timestamp}.mp4'
video_writer = None
video_fps = 5

# === Основной цикл ===
try:
    print('🟢 Запущен детектор. Для выхода — Ctrl+C.')

    while True:
        files = sorted(
            [f for f in os.listdir(SAVE_DIR) if f.endswith(('.png', '.jpg'))],
            key=lambda x: os.path.getctime(os.path.join(SAVE_DIR, x))
        )

        if not files:
            time.sleep(0.5)
            continue

        filepath = os.path.join(SAVE_DIR, files[0])
        img = cv2.imread(filepath)

        if img is None:
            print(f"⚠️ Невозможно прочитать: {filepath}")
            time.sleep(0.2)
            continue

        frame = img.copy()
        results = model.predict(
            source=img,
            imgsz=imgsz,
            conf=conf,
            iou=iou,
            verbose=False
        )

        r = results[0]
        boxes = r.boxes

        if boxes and len(boxes) > 0:
            for box in boxes:
                cls_id = int(box.cls[0])
                xyxy = box.xyxy[0].cpu().numpy().astype(int)

                x1, y1, x2, y2 = xyxy
                label = model.names[cls_id]
                color = (0, 255, 0)

                # Рисуем бокс и метку
                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                text_size, _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
                cv2.putText(frame, label, (x1 + 5, y1 + text_size[1] + 5),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)

                # Контрпики
                counters = get_counter_names(label)
                if counters:
                    n = len(counters[:4])
                    box_height = y2 - y1

                    font_scale = 0.5
                    font_thickness = 1
                    spacing = box_height // (n + 1)

                    box_center_x = (x1 + x2) // 2
                    draw_left = box_center_x > frame.shape[1] // 2

                    for idx, name in enumerate(counters[:4]):
                        text_y = y1 + spacing * (idx + 1)
                        text_size, _ = cv2.getTextSize(name, cv2.FONT_HERSHEY_SIMPLEX, font_scale, font_thickness)
                        text_x = x1 - text_size[0] - 10 if draw_left else x2 + 10
                        cv2.putText(
                            frame,
                            name,
                            (text_x, text_y),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            font_scale,
                            (0, 150, 255),
                            font_thickness
                        )
        else:
            print(f'👻 На скрине {os.path.basename(filepath)} герои не найдены.')

        if video_writer is None:
            height, width, _ = frame.shape
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            video_writer = cv2.VideoWriter(video_output_path, fourcc, video_fps, (width, height))

        video_writer.write(frame)
        os.remove(filepath)

except KeyboardInterrupt:
    print('\n🛑 Остановка по Ctrl+C')

finally:
    if video_writer is not None:
        video_writer.release()
        print(f'🎥 Видео сохранено: {video_output_path}')

    deleted = 0
    for f in os.listdir(SAVE_DIR):
        if f.endswith(('.png', '.jpg')):
            try:
                os.remove(os.path.join(SAVE_DIR, f))
                deleted += 1
            except Exception as e:
                print(f"⚠️ Не удалось удалить {f}: {e}")
    print(f'🧹 Удалено {deleted} оставшихся скриншотов из {SAVE_DIR}')
