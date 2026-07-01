import os
import unittest
import tempfile
import shutil
from pathlib import Path
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.file_manager import search_files


class TestSearch(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        (Path(self.temp_dir) / "file1.py").write_text("")
        (Path(self.temp_dir) / "file2.txt").write_text("")
        (Path(self.temp_dir) / "test_file.py").write_text("")

        subdir = Path(self.temp_dir) / "subdir"
        subdir.mkdir()
        (subdir / "inner.py").write_text("")

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_search_py_files(self):
        success, message, data = search_files(self.temp_dir, r"\.py$", recursive=True)
        self.assertTrue(success)
        self.assertEqual(data["count"], 3)

    def test_search_files_with_test(self):
        success, message, data = search_files(self.temp_dir, "test", recursive=True)
        self.assertTrue(success)
        self.assertEqual(data["count"], 1)


if __name__ == "__main__":
    unittest.main()