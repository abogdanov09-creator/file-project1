import os
import unittest
import tempfile
import shutil
from pathlib import Path
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from file_manager.commands import delete_file


class TestDelete(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.test_file = Path(self.temp_dir) / "file.txt"
        self.test_file.write_text("content")

        self.test_dir = Path(self.temp_dir) / "folder"
        self.test_dir.mkdir()
        (self.test_dir / "inner.txt").write_text("inner")

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_delete_file_success(self):
        success, message, _ = delete_file(str(self.test_file))
        self.assertTrue(success)
        self.assertFalse(self.test_file.exists())

    def test_delete_directory_without_recursive(self):
        success, message, _ = delete_file(str(self.test_dir))
        self.assertFalse(success)
        self.assertIn("-r", message)

    def test_delete_directory_recursive(self):
        success, message, _ = delete_file(str(self.test_dir), recursive=True)
        self.assertTrue(success)
        self.assertFalse(self.test_dir.exists())

    def test_delete_nonexistent_force(self):
        success, message, _ = delete_file("/nonexistent/file.txt", force=True)
        self.assertTrue(success)
        self.assertIn("force", message)


if __name__ == "__main__":
    unittest.main()