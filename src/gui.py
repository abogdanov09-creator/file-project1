import os
import shutil
import sys
from io import StringIO
import flet as ft
from file_manager import copy_file, delete_item, count_files, search_files, analyse_folder

# Константы
MAX_SEARCH_RESULTS_DISPLAY = 5  # Максимальное количество результатов поиска для отображения
MAX_ANALYSIS_OUTPUT_LENGTH = 500  # Максимальная длина вывода анализа


def main(page: ft.Page):
    # Настройка окна
    page.title = "Файловый менеджер"
    page.window_width = 500
    page.window_height = 400
    page.padding = 20
    page.theme_mode = ft.ThemeMode.LIGHT

    # Переменные
    selected_path = None

    # Показ сообщений (программа НЕ падает)
    def show_message(msg, is_error=False):
        color = ft.colors.RED if is_error else ft.colors.GREEN
        page.snack_bar = ft.SnackBar(ft.Text(msg), bgcolor=color)
        page.snack_bar.open = True
        page.update()

    # Выбор файла/папки через пикер (нативный)
    def pick_file(e):
        def on_result(e):
            nonlocal selected_path
            if e.files:
                selected_path = e.files[0].path
                file_text.value = f"Выбрано: {os.path.basename(selected_path)}"
            elif e.path:
                selected_path = e.path
                file_text.value = f"Выбрано: {selected_path}"
            page.update()

        file_picker = ft.FilePicker(on_result=on_result)
        page.overlay.append(file_picker)
        page.update()
        file_picker.pick_files(allow_multiple=False)

    # Выбор папки
    def pick_folder(e):
        def on_result(e):
            nonlocal selected_path
            if e.path:
                selected_path = e.path
                file_text.value = f"Выбрано: {selected_path}"
            page.update()

        folder_picker = ft.FilePicker(on_result=on_result)
        page.overlay.append(folder_picker)
        page.update()
        folder_picker.get_directory_path()

    # Копирование - создаем копию в той же папке с префиксом "copy_"
    # (можно изменить логику для копирования в другую папку при необходимости)
    def do_copy(e):
        if not selected_path:
            show_message("Сначала выберите файл!", True)
            return
        try:
            # Создаем копию в той же папке
            dst = os.path.join(os.path.dirname(selected_path), "copy_" + os.path.basename(selected_path))
            result = copy_file(selected_path, dst)
            show_message(result)
        except Exception as ex:
            show_message(f"Ошибка: {ex}", True)

    # Удаление (с обработкой ошибок)
    def do_delete(e):
        if not selected_path:
            show_message("Сначала выберите файл!", True)
            return

        def confirm(confirm_event):
            dlg.open = False
            page.update()
            try:
                result = delete_item(selected_path)
                show_message(result)
            except Exception as ex:
                show_message(f"Ошибка: {ex}", True)

        dlg = ft.AlertDialog(
            title=ft.Text("Подтверждение"),
            content=ft.Text(f"Удалить {os.path.basename(selected_path)}?"),
            actions=[ft.TextButton("Да", on_click=confirm)]
        )
        page.dialog = dlg
        dlg.open = True
        page.update()

    # Подсчет файлов (с обработкой ошибок)
    def do_count(e):
        if not selected_path or not os.path.isdir(selected_path):
            show_message("Выберите ПАПКУ!", True)
            return
        try:
            result = count_files(selected_path)
            show_message(result)
        except Exception as ex:
            show_message(f"Ошибка: {ex}", True)

    # Поиск (с обработкой ошибок)
    def do_search(search_event):
        if not selected_path or not os.path.isdir(selected_path):
            show_message("Выберите ПАПКУ!", True)
            return
        if not search_input.value:
            show_message("Введите шаблон поиска!", True)
            return
        try:
            results = search_files(selected_path, search_input.value)
            if results:
                msg = "\n".join(results[:MAX_SEARCH_RESULTS_DISPLAY])
                if len(results) > MAX_SEARCH_RESULTS_DISPLAY:
                    msg += f"\n... и еще {len(results) - MAX_SEARCH_RESULTS_DISPLAY}"
            else:
                msg = "Ничего не найдено"
            show_message(msg)
        except Exception as ex:
            show_message(f"Ошибка: {ex}", True)

    # Анализ (с обработкой ошибок)
    def do_analyse(e):
        if not selected_path or not os.path.isdir(selected_path):
            show_message("Выберите ПАПКУ!", True)
            return
        try:
            # Перенаправляем вывод
            old_stdout = sys.stdout
            sys.stdout = StringIO()

            analyse_folder(selected_path)

            output = sys.stdout.getvalue()
            sys.stdout = old_stdout

            # Показываем в диалоге
            def close_dialog(close_event):
                dlg.open = False
                page.update()

            dlg = ft.AlertDialog(
                title=ft.Text("Анализ папки"),
                content=ft.Container(
                    content=ft.Text(output[:MAX_ANALYSIS_OUTPUT_LENGTH]),
                    width=400,
                    height=300
                ),
                actions=[ft.TextButton("OK", on_click=close_dialog)]
            )
            page.dialog = dlg
            dlg.open = True
            page.update()
        except Exception as ex:
            show_message(f"Ошибка: {ex}", True)

    # === ИНТЕРФЕЙС ===
    file_text = ft.Text("Ничего не выбрано")

    search_input = ft.TextField(
        label="Шаблон поиска",
        hint_text="*.txt",
        width=300
    )

    # Кнопки с тултипами
    page.add(
        ft.Text("Файловый менеджер", size=24, weight=ft.FontWeight.BOLD),

        ft.Row([
            ft.ElevatedButton(
                "Выбрать файл",
                icon=ft.icons.FILE_OPEN,
                on_click=pick_file,
                tooltip="Выберите файл для операций"
            ),
            ft.ElevatedButton(
                "Выбрать папку",
                icon=ft.icons.FOLDER_OPEN,
                on_click=pick_folder,
                tooltip="Выберите папку для операций"
            ),
        ]),

        file_text,

        ft.Divider(),
        ft.Text("Операции:", weight=ft.FontWeight.BOLD),

        ft.Row([
            ft.ElevatedButton("Копировать", on_click=do_copy, tooltip="Копировать файл"),
            ft.ElevatedButton("Удалить", on_click=do_delete, tooltip="Удалить файл/папку"),
        ]),

        ft.Row([
            ft.ElevatedButton("Подсчет", on_click=do_count, tooltip="Посчитать файлы в папке"),
            ft.ElevatedButton("Анализ", on_click=do_analyse, tooltip="Показать структуру папки"),
        ]),

        ft.Divider(),
        ft.Text("Поиск:", weight=ft.FontWeight.BOLD),
        search_input,
        ft.ElevatedButton("Искать", on_click=do_search, tooltip="Искать файлы по шаблону"),
    )


if __name__ == "__main__":
    ft.app(target=main, view=ft.WEB_BROWSER, port=8080)