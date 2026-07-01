

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import argparse
from file_manager import (
    copy_file,
    delete_file,
    count_files,
    search_files,
    add_date_to_filename,
    analyse_size
)


def main():
    parser = argparse.ArgumentParser(
        prog="filemanager",
        description="Файловый менеджер для работы с файловой системой",
        epilog="Примеры:\n"
               "  python cli.py copy file.txt copy.txt\n"
               "  python cli.py delete folder -r\n"
               "  python cli.py count .\n"
               "  python cli.py search . '\\.py$'\n"
               "  python cli.py add_date file.txt\n"
               "  python cli.py analyse . -s size -n 10"
    )

    subparsers = parser.add_subparsers(dest="command", required=True, help="Команды")

    # COPY (3 балла)
    p_copy = subparsers.add_parser("copy", help="Копировать файл")
    p_copy.add_argument("source", help="Исходный файл")
    p_copy.add_argument("destination", help="Куда копировать")

    # DELETE (3 балла)
    p_del = subparsers.add_parser("delete", help="Удалить файл или папку")
    p_del.add_argument("path", help="Путь")
    p_del.add_argument("-r", "--recursive", action="store_true", help="Удалять папки рекурсивно")
    p_del.add_argument("-f", "--force", action="store_true", help="Принудительно (игнорировать ошибки)")

    # COUNT (4 балла)
    p_cnt = subparsers.add_parser("count", help="Подсчитать количество файлов")
    p_cnt.add_argument("path", nargs="?", default=".", help="Путь к папке")

    # SEARCH (4 балла)
    p_search = subparsers.add_parser("search", help="Поиск по regex")
    p_search.add_argument("path", help="Путь для поиска")
    p_search.add_argument("pattern", help="Регулярное выражение")
    p_search.add_argument("-r", "--recursive", action="store_true", default=True, help="Рекурсивно")
    p_search.add_argument("--no-recursive", action="store_true", help="Отключить рекурсию")
    p_search.add_argument("-c", "--case-sensitive", action="store_true", help="Учитывать регистр")

    # ADD_DATE (6 баллов)
    p_date = subparsers.add_parser("add_date", help="Добавить дату создания в имя")
    p_date.add_argument("path", help="Файл или папка")
    p_date.add_argument("-r", "--recursive", action="store_true", help="Рекурсивно")
    p_date.add_argument("-d", "--dry-run", action="store_true", help="Только показать")

    # ANALYSE (10 баллов)
    p_anal = subparsers.add_parser("analyse", aliases=["analyze"], help="Анализ размера")
    p_anal.add_argument("path", nargs="?", default=".", help="Путь")
    p_anal.add_argument("-s", "--sort", choices=["size", "name"], default="size", help="Сортировка")
    p_anal.add_argument("-n", "--max-items", type=int, default=20, help="Максимум элементов")

    args = parser.parse_args()

    # Вызов команд
    try:
        if args.command == "copy":
            success, msg, _ = copy_file(args.source, args.destination)
        elif args.command == "delete":
            success, msg, _ = delete_file(args.path, args.recursive, args.force)
        elif args.command == "count":
            success, msg, data = count_files(args.path)
        elif args.command == "search":
            recursive = not args.no_recursive if hasattr(args, 'no_recursive') else args.recursive
            success, msg, data = search_files(args.path, args.pattern, recursive, args.case_sensitive)
        elif args.command == "add_date":
            success, msg, data = add_date_to_filename(args.path, args.recursive, args.dry_run)
        elif args.command in ["analyse", "analyze"]:
            success, msg, data = analyse_size(args.path, args.sort, args.max_items)
        else:
            print(f"❌ Неизвестная команда: {args.command}")
            sys.exit(1)

        if success:
            print(f"✅ {msg}")
            if args.command == "search" and data and data.get("found"):
                print("\nНайденные файлы:")
                for f in data["found"][:20]:
                    print(f"  - {f}")
                if len(data["found"]) > 20:
                    print(f"  ... и ещё {len(data['found']) - 20} файлов")
            sys.exit(0)
        else:
            print(f"❌ {msg}")
            sys.exit(1)
    except Exception as e:
        print(f"❌ Критическая ошибка: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()