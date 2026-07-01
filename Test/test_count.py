import os
import unittest
import tempfile
import shutil
from pathlib import Path
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.file_manager import count_files


class TestCount(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        (Path(self.temp_dir) / "file1.txt").write_text("a")
        (Path(self.temp_dir) / "file2.txt").write_text("b")

        subdir = Path(self.temp_dir) / "subdir"
        subdir.mkdir()
        (subdir / "file3.txt").write_text("c")
        (subdir / "file4.txt").write_text("d")

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_count_all_files(self):
        success, message, data = count_files(self.temp_dir)
        self.assertTrue(success)
        self.assertEqual(data["count"], 4)

    def test_count_empty_directory(self):
        empty_dir = Path(self.temp_dir) / "empty"
        empty_dir.mkdir()
        success, message, data = count_files(str(empty_dir))
        self.assertTrue(success)
        self.assertEqual(data["count"], 0)


if __name__ == "__main__":
    unittest.main()