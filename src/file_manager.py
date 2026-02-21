import os
import shutil
import re
from datetime import datetime

def copy_file(src, dst):
    shutil.copy2(src, dst)
    print(f"Скопировано: {src} -> {dst}")

def delete_item(path):
    if os.path.isfile(path):
        os.remove(path)
        print(f"Удалён файл: {path}")
    else:
        shutil.rmtree(path)
        print(f"Удалена папка: {path}")

def count_files(folder):
    total = 0
    for root, dirs, files in os.walk(folder):
        total += len(files)
    print(f"Всего файлов: {total}")
    return total

def search_files(folder, pattern):
    for root, dirs, files in os.walk(folder):
        for file in files:
            if re.search(pattern, file):
                print(os.path.join(root, file))

def add_date_to_filename(path, recursive=False):
    if os.path.isfile(path):
        _rename(path)
    elif recursive:
        for root, dirs, files in os.walk(path):
            for file in files:
                _rename(os.path.join(root, file))
    else:
        for file in os.listdir(path):
            file_path = os.path.join(path, file)
            if os.path.isfile(file_path):
                _rename(file_path)

def _rename(file_path):
    folder = os.path.dirname(file_path)
    name, ext = os.path.splitext(os.path.basename(file_path))
    date = datetime.fromtimestamp(os.path.getctime(file_path)).strftime("%Y-%m-%d")
    new_path = os.path.join(folder, f"{name}_{date}{ext}")
    os.rename(file_path, new_path)
    print(f"Переименован: {new_path}")

def analyse_folder(path):
    def get_size(p):
        if os.path.isfile(p):
            return os.path.getsize(p)
        return sum(get_size(os.path.join(root, f)) for root, dirs, files in os.walk(p) for f in files)

    def size_str(s):
        for unit in ['B', 'KB', 'MB', 'GB']:
            if s < 1024:
                return f"{s:.1f}{unit}"
            s /= 1024
        return f"{s:.1f}TB"

    def tree(p, level=0):
        print("  " * level + f"- {os.path.basename(p) or p} {size_str(get_size(p))}")
        if os.path.isdir(p):
            for item in sorted(os.listdir(p)):
                tree(os.path.join(p, item), level + 1)

    tree(path)