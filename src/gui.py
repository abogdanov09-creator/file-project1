#!/usr/bin/env python3
"""
GUI для файлового менеджера
Использует tkinter (встроенная библиотека)
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from pathlib import Path
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from file_manager.commands import (
    copy_file,
    delete_file,
    count_files,
    search_files,
    add_date_to_filename,
    analyse_size
)


class FileManagerGUI:
    """Главный класс GUI"""

    def __init__(self, root):
        self.root = root
        self.root.title("Файловый менеджер")
        self.root.geometry("900x750")
        self.root.resizable(True, True)

        # Переменные
        self.current_path = tk.StringVar(value=str(Path.cwd()))

        # Создаём интерфейс
        self._create_widgets()

        # Лог запуска
        self._log("✅ Файловый менеджер GUI запущен")
        self._log(f"📁 Рабочая папка: {self.current_path.get()}")

    def _create_widgets(self):
        """Создание всех виджетов"""

        # ===== Верхняя панель =====
        top_frame = ttk.Frame(self.root, padding="5")
        top_frame.pack(fill=tk.X)

        ttk.Label(top_frame, text="📁 Папка:").pack(side=tk.LEFT, padx=(0, 5))
        path_entry = ttk.Entry(top_frame, textvariable=self.current_path)
        path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        ttk.Button(top_frame, text="Обзор", command=self._browse_folder).pack(side=tk.LEFT)

        # ===== Вкладки =====
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Вкладка 1: Копирование и удаление
        tab_copy_delete = ttk.Frame(notebook)
        notebook.add(tab_copy_delete, text="📋 Копировать / Удалить")
        self._create_copy_delete_tab(tab_copy_delete)

        # Вкладка 2: Подсчёт и поиск
        tab_count_search = ttk.Frame(notebook)
        notebook.add(tab_count_search, text="🔍 Подсчёт / Поиск")
        self._create_count_search_tab(tab_count_search)

        # Вкладка 3: Дата и анализ
        tab_date_analyse = ttk.Frame(notebook)
        notebook.add(tab_date_analyse, text="📅 Дата / Анализ")
        self._create_date_analyse_tab(tab_date_analyse)

        # ===== Лог (вывод) =====
        log_frame = ttk.LabelFrame(self.root, text="📄 Результат", padding="5")
        log_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=(0, 5))

        self.log_text = scrolledtext.ScrolledText(log_frame, height=12, wrap=tk.WORD)
        self.log_text.pack(fill=tk.BOTH, expand=True)

        # ===== Статус =====
        self.status_var = tk.StringVar(value="Готов")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(fill=tk.X, padx=5, pady=(0, 5))

    def _create_copy_delete_tab(self, parent):
        """Вкладка: Копирование и удаление"""
        frame = ttk.Frame(parent, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)

        # --- Копирование ---
        ttk.Label(frame, text="📋 КОПИРОВАТЬ ФАЙЛ", font=("", 10, "bold")).pack(anchor=tk.W, pady=(0, 5))

        row_source = ttk.Frame(frame)
        row_source.pack(fill=tk.X, pady=2)
        ttk.Label(row_source, text="Откуда:").pack(side=tk.LEFT, padx=(0, 5))
        self.copy_source = ttk.Entry(row_source)
        self.copy_source.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        ttk.Button(row_source, text="📂", command=lambda: self._browse_file(self.copy_source)).pack(side=tk.LEFT)

        row_dest = ttk.Frame(frame)
        row_dest.pack(fill=tk.X, pady=2)
        ttk.Label(row_dest, text="Куда:").pack(side=tk.LEFT, padx=(0, 5))
        self.copy_dest = ttk.Entry(row_dest)
        self.copy_dest.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        ttk.Button(row_dest, text="📂", command=lambda: self._browse_file(self.copy_dest)).pack(side=tk.LEFT)

        ttk.Button(frame, text="▶ Выполнить копирование", command=self._run_copy).pack(anchor=tk.W, pady=5)

        ttk.Separator(frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)

        # --- Удаление ---
        ttk.Label(frame, text="🗑️ УДАЛИТЬ", font=("", 10, "bold")).pack(anchor=tk.W, pady=(0, 5))

        row_path = ttk.Frame(frame)
        row_path.pack(fill=tk.X, pady=2)
        ttk.Label(row_path, text="Путь:").pack(side=tk.LEFT, padx=(0, 5))
        self.delete_path = ttk.Entry(row_path)
        self.delete_path.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        ttk.Button(row_path, text="📂", command=lambda: self._browse_file_folder(self.delete_path)).pack(side=tk.LEFT)

        self.delete_recursive = tk.BooleanVar()
        self.delete_force = tk.BooleanVar()
        ttk.Checkbutton(frame, text="Рекурсивно (-r)", variable=self.delete_recursive).pack(anchor=tk.W)
        ttk.Checkbutton(frame, text="Принудительно (-f)", variable=self.delete_force).pack(anchor=tk.W)

        ttk.Button(frame, text="▶ Выполнить удаление", command=self._run_delete).pack(anchor=tk.W, pady=5)

    def _create_count_search_tab(self, parent):
        """Вкладка: Подсчёт и поиск"""
        frame = ttk.Frame(parent, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)

        # --- Подсчёт ---
        ttk.Label(frame, text="🔢 ПОДСЧЁТ ФАЙЛОВ", font=("", 10, "bold")).pack(anchor=tk.W, pady=(0, 5))

        row_path = ttk.Frame(frame)
        row_path.pack(fill=tk.X, pady=2)
        ttk.Label(row_path, text="Папка:").pack(side=tk.LEFT, padx=(0, 5))
        self.count_path = ttk.Entry(row_path)
        self.count_path.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        ttk.Button(row_path, text="📂", command=lambda: self._browse_folder(self.count_path)).pack(side=tk.LEFT)

        ttk.Button(frame, text="▶ Подсчитать", command=self._run_count).pack(anchor=tk.W, pady=5)

        ttk.Separator(frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)

        # --- Поиск ---
        ttk.Label(frame, text="🔍 ПОИСК ПО РЕГУЛЯРНОМУ ВЫРАЖЕНИЮ", font=("", 10, "bold")).pack(anchor=tk.W, pady=(0, 5))

        row_path = ttk.Frame(frame)
        row_path.pack(fill=tk.X, pady=2)
        ttk.Label(row_path, text="Папка:").pack(side=tk.LEFT, padx=(0, 5))
        self.search_path = ttk.Entry(row_path)
        self.search_path.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        ttk.Button(row_path, text="📂", command=lambda: self._browse_folder(self.search_path)).pack(side=tk.LEFT)

        row_pattern = ttk.Frame(frame)
        row_pattern.pack(fill=tk.X, pady=2)
        ttk.Label(row_pattern, text="Шаблон:").pack(side=tk.LEFT, padx=(0, 5))
        self.search_pattern = ttk.Entry(row_pattern)
        self.search_pattern.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))

        self.search_recursive = tk.BooleanVar(value=True)
        self.search_case_sensitive = tk.BooleanVar(value=False)
        ttk.Checkbutton(frame, text="Рекурсивно", variable=self.search_recursive).pack(anchor=tk.W)
        ttk.Checkbutton(frame, text="Учитывать регистр", variable=self.search_case_sensitive).pack(anchor=tk.W)

        ttk.Button(frame, text="▶ Искать", command=self._run_search).pack(anchor=tk.W, pady=5)

    def _create_date_analyse_tab(self, parent):
        """Вкладка: Дата и анализ"""
        frame = ttk.Frame(parent, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)

        # --- Дата ---
        ttk.Label(frame, text="📅 ДОБАВИТЬ ДАТУ В ИМЯ ФАЙЛА", font=("", 10, "bold")).pack(anchor=tk.W, pady=(0, 5))

        row_path = ttk.Frame(frame)
        row_path.pack(fill=tk.X, pady=2)
        ttk.Label(row_path, text="Путь:").pack(side=tk.LEFT, padx=(0, 5))
        self.date_path = ttk.Entry(row_path)
        self.date_path.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        ttk.Button(row_path, text="📂", command=lambda: self._browse_file_folder(self.date_path)).pack(side=tk.LEFT)

        self.date_recursive = tk.BooleanVar(value=False)
        self.date_dry_run = tk.BooleanVar(value=True)
        ttk.Checkbutton(frame, text="Рекурсивно (-r)", variable=self.date_recursive).pack(anchor=tk.W)
        ttk.Checkbutton(frame, text="Dry run (только показать)", variable=self.date_dry_run).pack(anchor=tk.W)

        ttk.Button(frame, text="▶ Добавить дату", command=self._run_add_date).pack(anchor=tk.W, pady=5)

        ttk.Separator(frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)

        # --- Анализ ---
        ttk.Label(frame, text="📊 АНАЛИЗ РАЗМЕРА", font=("", 10, "bold")).pack(anchor=tk.W, pady=(0, 5))

        row_path = ttk.Frame(frame)
        row_path.pack(fill=tk.X, pady=2)
        ttk.Label(row_path, text="Папка:").pack(side=tk.LEFT, padx=(0, 5))
        self.analyse_path = ttk.Entry(row_path)
        self.analyse_path.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        ttk.Button(row_path, text="📂", command=lambda: self._browse_folder(self.analyse_path)).pack(side=tk.LEFT)

        row_sort = ttk.Frame(frame)
        row_sort.pack(fill=tk.X, pady=5)
        ttk.Label(row_sort, text="Сортировка:").pack(side=tk.LEFT, padx=(0, 5))
        self.sort_by = ttk.Combobox(row_sort, values=["size", "name"], state="readonly", width=10)
        self.sort_by.set("size")
        self.sort_by.pack(side=tk.LEFT, padx=(0, 15))

        ttk.Label(row_sort, text="Макс. элементов:").pack(side=tk.LEFT, padx=(0, 5))
        self.max_items = ttk.Spinbox(row_sort, from_=1, to=100, width=8)
        self.max_items.set(20)
        self.max_items.pack(side=tk.LEFT)

        ttk.Button(frame, text="▶ Анализировать", command=self._run_analyse).pack(anchor=tk.W, pady=5)

    # ===== ВСПОМОГАТЕЛЬНЫЕ МЕТОДЫ =====

    def _log(self, message, is_error=False):
        """Вывод сообщения в лог"""
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.status_var.set(message[:100])
        if is_error:
            self.log_text.tag_add("error", "end-2l", "end-1l")
            self.log_text.tag_config("error", foreground="red")

    def _show_error(self, message):
        """Показать окно с ошибкой"""
        messagebox.showerror("Ошибка", message)
        self._log(f"❌ {message}", is_error=True)

    def _browse_folder(self):
        """Выбор папки (обновляет текущий путь)"""
        folder = filedialog.askdirectory(initialdir=self.current_path.get())
        if folder:
            self.current_path.set(folder)
            self._log(f"📁 Выбрана папка: {folder}")

    def _browse_file(self, entry):
        """Выбор файла (вставляет путь в поле)"""
        path = filedialog.askopenfilename(initialdir=self.current_path.get())
        if path:
            entry.delete(0, tk.END)
            entry.insert(0, path)

    def _browse_folder(self, entry):
        """Выбор папки (вставляет путь в поле)"""
        path = filedialog.askdirectory(initialdir=self.current_path.get())
        if path:
            entry.delete(0, tk.END)
            entry.insert(0, path)

    def _browse_file_folder(self, entry):
        """Выбор файла или папки"""
        path = filedialog.askopenfilename(initialdir=self.current_path.get())
        if not path:
            path = filedialog.askdirectory(initialdir=self.current_path.get())
        if path:
            entry.delete(0, tk.END)
            entry.insert(0, path)

    # ===== ЗАПУСК КОМАНД =====

    def _run_copy(self):
        """Выполнить копирование"""
        source = self.copy_source.get().strip()
        dest = self.copy_dest.get().strip()
        if not source or not dest:
            self._show_error("Заполните оба поля")
            return
        success, message, _ = copy_file(source, dest)
        self._log(f"{'✅' if success else '❌'} {message}")
        if success:
            self.copy_source.delete(0, tk.END)
            self.copy_dest.delete(0, tk.END)

    def _run_delete(self):
        """Выполнить удаление"""
        path = self.delete_path.get().strip()
        if not path:
            self._show_error("Введите путь")
            return
        success, message, _ = delete_file(
            path,
            recursive=self.delete_recursive.get(),
            force=self.delete_force.get()
        )
        self._log(f"{'✅' if success else '❌'} {message}")
        if success:
            self.delete_path.delete(0, tk.END)

    def _run_count(self):
        """Выполнить подсчёт"""
        path = self.count_path.get().strip()
        if not path:
            path = self.current_path.get()
        success, message, data = count_files(path)
        self._log(f"{'✅' if success else '❌'} {message}")
        if success and data:
            self._log(f"📊 Всего файлов: {data.get('count', 0)}")

    def _run_search(self):
        """Выполнить поиск"""
        path = self.search_path.get().strip()
        if not path:
            path = self.current_path.get()
        pattern = self.search_pattern.get().strip()
        if not pattern:
            self._show_error("Введите шаблон поиска")
            return
        success, message, data = search_files(
            path,
            pattern,
            recursive=self.search_recursive.get(),
            case_sensitive=self.search_case_sensitive.get()
        )
        self._log(f"{'✅' if success else '❌'} {message}")
        if success and data and data.get("found"):
            for file_path in data["found"][:10]:
                self._log(f"  📄 {file_path}")
            if len(data["found"]) > 10:
                self._log(f"  ... и ещё {len(data['found']) - 10} файлов")

    def _run_add_date(self):
        """Выполнить добавление даты"""
        path = self.date_path.get().strip()
        if not path:
            self._show_error("Введите путь")
            return
        success, message, data = add_date_to_filename(
            path,
            recursive=self.date_recursive.get(),
            dry_run=self.date_dry_run.get()
        )
        self._log(f"{'✅' if success else '❌'} {message}")

    def _run_analyse(self):
        """Выполнить анализ размера"""
        path = self.analyse_path.get().strip()
        if not path:
            path = self.current_path.get()
        try:
            max_n = int(self.max_items.get())
        except ValueError:
            max_n = 20
        success, message, data = analyse_size(
            path,
            sort_by=self.sort_by.get(),
            max_items=max_n
        )
        self._log(f"{'✅' if success else '❌'} {message}")
        if success and data:
            self._log(f"📊 Общий размер: {data.get('total_size', '')}")
            if data.get("items"):
                for name, size, item_type in data["items"][:10]:
                    icon = "📁" if item_type == "dir" else "📄"
                    self._log(f"  {icon} {name} {size}")


def main():
    """Точка входа"""
    root = tk.Tk()
    app = FileManagerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()