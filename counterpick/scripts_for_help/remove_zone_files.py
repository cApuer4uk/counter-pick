import os

def remove_zone_identifier_files(start_path):
    deleted = 0
    for root, dirs, files in os.walk(start_path):
        for file in files:
            if file.endswith('_Zone.Identifier'):
                full_path = os.path.join(root, file)
                try:
                    os.remove(full_path)
                    print(f"Удалено: {full_path}")
                    deleted += 1
                except Exception as e:
                    print(f"Ошибка при удалении {full_path}: {e}")
    print(f"\nИтого удалено: {deleted} .Zone.Identifier файлов")

if __name__ == "__main__":
    remove_zone_identifier_files("/home/capu/projects/counterpick/counterpick/ml")

