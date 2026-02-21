import unittest
import os
import tempfile
import shutil
from src import file_manager


class TestFileManager(unittest.TestCase):
    """Тесты для функций работы с файлами"""

    def setUp(self):
        """Создаём временную папку для тестов"""
        self.test_dir = tempfile.mkdtemp()

        # Создаём тестовые файлы
        self.test_file = os.path.join(self.test_dir, "test.txt")
        with open(self.test_file, "w") as f:
            f.write("test content")

        self.test_file2 = os.path.join(self.test_dir, "test2.txt")
        with open(self.test_file2, "w") as f:
            f.write("test content 2")

        # Создаём вложенную папку с файлом
        self.subdir = os.path.join(self.test_dir, "subdir")
        os.mkdir(self.subdir)
        self.subfile = os.path.join(self.subdir, "subfile.txt")
        with open(self.subfile, "w") as f:
            f.write("subdir content")

    def tearDown(self):
        """Удаляем временную папку после тестов"""
        shutil.rmtree(self.test_dir)

    def test_copy_file(self):
        """Тест копирования файла"""
        dst = os.path.join(self.test_dir, "copy.txt")
        file_manager.copy_file(self.test_file, dst)
        self.assertTrue(os.path.exists(dst))

    def test_delete_file(self):
        """Тест удаления файла"""
        file_manager.delete_item(self.test_file)
        self.assertFalse(os.path.exists(self.test_file))

    def test_delete_folder(self):
        """Тест удаления папки"""
        file_manager.delete_item(self.subdir)
        self.assertFalse(os.path.exists(self.subdir))

    def test_count_files(self):
        """Тест подсчёта файлов (должно быть 3)"""
        count = file_manager.count_files(self.test_dir)
        self.assertEqual(count, 3)

    def test_search_files(self):
        """Тест поиска файлов по шаблону"""
        results = file_manager.search_files(self.test_dir, r"test\d*\.txt")
        # Должны найтись test.txt и test2.txt
        self.assertEqual(len(results), 2)

    def test_add_date_to_file(self):
        """Тест добавления даты к имени файла"""
        file_manager.add_date_to_filename(self.test_file)
        # Старый файл должен исчезнуть
        self.assertFalse(os.path.exists(self.test_file))
        # Должен появиться новый файл с датой
        files = os.listdir(self.test_dir)
        self.assertTrue(any("test_" in f and ".txt" in f for f in files))


if __name__ == "__main__":
    unittest.main()