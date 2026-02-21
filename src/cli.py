import argparse
from src import file_manager

def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("copy").add_argument("args", nargs=2)
    sub.add_parser("delete").add_argument("path")
    sub.add_parser("count").add_argument("folder")
    p = sub.add_parser("search")
    p.add_argument("folder")
    p.add_argument("pattern")
    p = sub.add_parser("add-date")
    p.add_argument("path")
    p.add_argument("--recursive", action="store_true")
    sub.add_parser("analyse").add_argument("path")

    args = parser.parse_args()

    if args.command == "copy":
        file_manager.copy_file(*args.args)
    elif args.command == "delete":
        file_manager.delete_item(args.path)
    elif args.command == "count":
        file_manager.count_files(args.folder)
    elif args.command == "search":
        file_manager.search_files(args.folder, args.pattern)
    elif args.command == "add-date":
        file_manager.add_date_to_filename(args.path, args.recursive)
    elif args.command == "analyse":
        file_manager.analyse_folder(args.path)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()