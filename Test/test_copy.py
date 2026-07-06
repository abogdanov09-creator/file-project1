import os
import unittest
import tempfile
import shutil
from pathlib import Path
import sys
from file_manager.commands import copy_file
# Добавляем корень проекта в путь
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))



class TestCopy(unittest.TestCase):
    """Тесты для команды copy (3 балла)"""

    def setUp(self):
        """Создаём временную папку с тестовым файлом"""
        self.temp_dir = tempfile.mkdtemp()
        self.source_file = Path(self.temp_dir) / "source.txt"
        self.source_file.write_text("Hello, World!")
        self.dest_file = Path(self.temp_dir) / "dest.txt"

    def tearDown(self):
        """Удаляем временную папку"""
        shutil.rmtree(self.temp_dir)

    def test_copy_success(self):
        """Копирование обычного файла"""
        success, message, _ = copy_file(str(self.source_file), str(self.dest_file))

        self.assertTrue(success)
        self.assertTrue(self.dest_file.exists())
        self.assertEqual(self.dest_file.read_text(), "Hello, World!")

    def test_copy_nonexistent_source(self):
        """Копирование несуществующего файла -> ошибка"""
        success, message, _ = copy_file("/nonexistent/file.txt", str(self.dest_file))

        self.assertFalse(success)
        self.assertIn("не существует", message)

    def test_copy_source_is_directory(self):
        """Копирование папки -> ошибка (не поддерживается)"""
        success, message, _ = copy_file(str(self.temp_dir), str(self.dest_file))

        self.assertFalse(success)
        self.assertIn("не поддерживается", message)


if __name__ == "__main__":
    unittest.main()