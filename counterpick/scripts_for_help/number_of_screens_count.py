import os

root_dir = "/mnt/w/Wcounterpick/Screenshots"  # Путь к папке со скриншотами
invalid_prefix = "npc_dota_hero"

hero_stats = {}

# Проходим по каждой подпапке (герою)
for hero_folder in os.listdir(root_dir):
    folder_path = os.path.join(root_dir, hero_folder)
    if not os.path.isdir(folder_path):
        continue

    # Получаем список файлов в папке героя
    files = os.listdir(folder_path)
    # Фильтруем те, что НЕ начинаются с npc_dota_hero
    non_prefixed_files = [f for f in files if not f.startswith(invalid_prefix) and f.lower().endswith(('.png', '.jpg'))]

    hero_stats[hero_folder] = len(non_prefixed_files)

# Сортировка по количеству (опционально)
hero_stats = dict(sorted(hero_stats.items(), key=lambda item: item[1], reverse=True))

# Вывод
for hero, count in hero_stats.items():
    print(f"{hero}: {count} незаюзанных скриншотов")
