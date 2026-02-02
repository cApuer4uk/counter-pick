from pathlib import Path
import yaml

# Определяем корень проекта (на два уровня выше текущего файла)
project_root = Path(__file__).resolve().parents[2]

# Пути к файлам
labels_file = project_root / 'counterpick' / 'ml' / 'all_labels.txt'
output_file = project_root / 'counterpick' / 'ml' / 'data.yaml'

# Считываем список классов
with labels_file.open('r', encoding='utf-8') as f:
    class_names = [line.strip() for line in f if line.strip()]

# Формируем структуру YAML
data = {
    'train': 'counterpick/ml/images/train',
    'val': 'counterpick/ml/images/val',
    'test': 'counterpick/ml/images/test',
    'nc': len(class_names),
    'names': class_names
}

# Сохраняем YAML-файл
with output_file.open('w', encoding='utf-8') as f:
    yaml.dump(data, f, sort_keys=False, allow_unicode=True)

print(f"✅ data.yaml успешно создан по пути: {output_file}")
