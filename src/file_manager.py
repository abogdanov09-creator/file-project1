"""
Файловый менеджер — вся логика в одном файле
Каждая функция возвращает (success: bool, message: str, data: any)
"""

import os
import re
import shutil
from datetime import datetime
from pathlib import Path
from typing import Tuple, Any


def _format_size(size_bytes: float) -> str:
    """Форматирование размера в человекочитаемый вид"""
    if size_bytes == 0:
        return "0 B"
    units = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    while size_bytes >= 1024 and i < len(units) - 1:
        size_bytes /= 1024.0
        i += 1
    return f"{size_bytes:.1f} {units[i]}" if i > 0 else f"{size_bytes:.0f} {units[i]}"


# ==================== COPY (3 балла) ====================

def copy_file(source: str, destination: str) -> Tuple[bool, str, Any]:
    """Копирование файла"""
    try:
        src = Path(source)
        dst = Path(destination)

        if not src.exists():
            return False, f"Источник не существует: {source}", None
        if src.is_dir():
            return False, "Копирование папок не поддерживается", None
        if dst.exists() and dst.is_dir():
            dst = dst / src.name
        if dst.exists():
            return False, f"Назначение уже существует: {destination}", None

        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        return True, f"Скопировано: {src} -> {dst}", str(dst)
    except PermissionError as e:
        return False, f"Нет прав доступа: {e}", None
    except Exception as e:
        return False, f"Ошибка: {e}", None


# ==================== DELETE (3 балла) ====================

def delete_file(path: str, recursive: bool = False, force: bool = False) -> Tuple[bool, str, Any]:
    """Удаление файла или папки"""
    try:
        target = Path(path)
        if not target.exists():
            if force:
                return True, f"Игнорируем (force): {path} не существует", None
            return False, f"Объект не существует: {path}", None
        if target.is_dir():
            if not recursive:
                return False, "Для удаления папки используйте -r", None
            if target.absolute() == Path.cwd().absolute():
                return False, "Нельзя удалить текущую папку", None
            shutil.rmtree(target)
            return True, f"Удалена папка: {path}", None
        else:
            os.remove(target)
            return True, f"Удалён файл: {path}", None
    except PermissionError as e:
        return False, f"Нет прав доступа: {e}", None
    except Exception as e:
        return False, f"Ошибка: {e}", None


# ==================== COUNT (4 балла) ====================

def count_files(path: str) -> Tuple[bool, str, Any]:
    """Рекурсивный подсчёт файлов"""
    try:
        target = Path(path)
        if not target.exists():
            return False, f"Путь не существует: {path}", None
        if not target.is_dir():
            return False, f"Не является папкой: {path}", None

        total = 0
        for _, _, files in os.walk(target):
            total += len(files)

        return True, f"Файлов: {total}", {"count": total, "path": str(target)}
    except PermissionError as e:
        return False, f"Нет доступа: {e}", None
    except Exception as e:
        return False, f"Ошибка: {e}", None


# ==================== SEARCH (4 балла) ====================

def search_files(path: str, pattern: str, recursive: bool = True, case_sensitive: bool = False) -> Tuple[
    bool, str, Any]:
    """Поиск файлов по regex"""
    try:
        target = Path(path)
        if not target.exists():
            return False, f"Путь не существует: {path}", None
        if not target.is_dir():
            return False, f"Не является папкой: {path}", None

        try:
            flags = 0 if case_sensitive else re.IGNORECASE
            regex = re.compile(pattern, flags)
        except re.error as e:
            return False, f"Ошибка regex: {e}", None

        found = []
        if recursive:
            for root, _, files in os.walk(target):
                for f in files:
                    if regex.search(f):
                        found.append(str(Path(root) / f))
        else:
            for f in target.iterdir():
                if f.is_file() and regex.search(f.name):
                    found.append(str(f))

        return True, f"Найдено: {len(found)}", {"found": found, "count": len(found)}
    except PermissionError as e:
        return False, f"Нет доступа: {e}", None
    except Exception as e:
        return False, f"Ошибка: {e}", None


# ==================== ADD_DATE (6 баллов) ====================

def add_date_to_filename(path: str, recursive: bool = False, dry_run: bool = False) -> Tuple[bool, str, Any]:
    """Добавление даты создания в имя файла"""
    try:
        target = Path(path)
        if not target.exists():
            return False, f"Путь не существует: {path}", None

        results = []
        renamed_count = 0

        def process(p: Path):
            nonlocal renamed_count
            try:
                date = datetime.fromtimestamp(p.stat().st_ctime).strftime("%Y-%m-%d")
                new_name = f"{p.stem}_{date}{p.suffix}"
                new_path = p.parent / new_name
                if f"_{date}" in p.stem:
                    return False, f"Пропущен (дата уже есть): {p.name}"
                if new_path.exists():
                    return False, f"Конфликт: {new_name} уже существует"
                if dry_run:
                    return True, f"[DRY RUN] {p.name} -> {new_name}"
                p.rename(new_path)
                renamed_count += 1
                return True, f"{p.name} -> {new_name}"
            except Exception as e:
                return False, f"Ошибка: {p.name} - {e}"

        if target.is_file():
            ok, msg = process(target)
            results.append(msg)
        else:
            if recursive:
                for root, _, files in os.walk(target):
                    for f in files:
                        ok, msg = process(Path(root) / f)
                        results.append(msg)
            else:
                for f in target.iterdir():
                    if f.is_file():
                        ok, msg = process(f)
                        results.append(msg)

        mode = "DRY RUN" if dry_run else "Обработано"
        return True, f"{mode}: {renamed_count if not dry_run else len([r for r in results if 'DRY RUN' in r])} файлов", {
            "results": results}
    except Exception as e:
        return False, f"Ошибка: {e}", None


# ==================== ANALYSE (10 баллов) ====================

def analyse_size(path: str, sort_by: str = "size", max_items: int = 20) -> Tuple[bool, str, Any]:
    """Анализ размера папки"""
    try:
        target = Path(path)
        if not target.exists():
            return False, f"Путь не существует: {path}", None
        if not target.is_dir():
            return False, f"Не является папкой: {path}", None

        def get_size(p: Path):
            total = 0
            items = []
            try:
                for item in p.iterdir():
                    try:
                        if item.is_file():
                            size = item.stat().st_size
                            total += size
                            items.append((item.name, size, "file"))
                        elif item.is_dir():
                            sub_size, _ = get_size(item)
                            total += sub_size
                            items.append((f"{item.name}/", sub_size, "dir"))
                    except (PermissionError, OSError):
                        items.append((f"{item.name}/ (нет доступа)", 0, "error"))
            except PermissionError:
                pass
            return total, items

        total, items = get_size(target)

        if sort_by == "size":
            items.sort(key=lambda x: x[1], reverse=True)
        else:
            items.sort(key=lambda x: x[0].lower())

        display = items[:max_items]

        # Формируем результат
        result_lines = [f"📊 Анализ: {target.absolute()}", f"💾 Общий размер: {_format_size(total)}", "=" * 50]
        for name, size, typ in display:
            icon = "📁" if typ == "dir" else "📄" if typ == "file" else "⚠️"
            result_lines.append(f"  {icon} {name:<45} {_format_size(size)}")

        if len(items) > max_items:
            result_lines.append(f"  ... и ещё {len(items) - max_items} элементов")

        files_cnt = sum(1 for _, _, t in items if t == "file")
        dirs_cnt = sum(1 for _, _, t in items if t == "dir")
        result_lines.extend(["", "📈 Статистика:", f"  Файлов: {files_cnt}, Папок: {dirs_cnt}"])

        files = [(n, s) for n, s, t in items if t == "file"]
        if files:
            largest = max(files, key=lambda x: x[1])
            result_lines.append(f"  Самый большой файл: {largest[0]} ({_format_size(largest[1])})")

        if files_cnt > 0:
            avg = sum(s for _, s in files) / files_cnt
            result_lines.append(f"  Средний размер файла: {_format_size(avg)}")

        data = {
            "total_size": _format_size(total),
            "items": display,
            "stats": result_lines[-3:]
        }

        return True, f"Общий размер: {_format_size(total)}", data
    except Exception as e:
        return False, f"Ошибка: {e}", None