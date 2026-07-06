import os
import unittest
import tempfile
import shutil
from pathlib import Path
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from file_manager.commands import analyse_size


class TestAnalyse(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        (Path(self.temp_dir) / "small.txt").write_text("x" * 100)
        (Path(self.temp_dir) / "large.bin").write_bytes(b'\x00' * 10000)

        subdir = Path(self.temp_dir) / "subdir"
        subdir.mkdir()
        (subdir / "inner.txt").write_text("x" * 500)

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_analyse_success(self):
        success, message, data = analyse_size(self.temp_dir)
        self.assertTrue(success)
        self.assertIn("Общий размер", message)
        self.assertIsInstance(data, dict)
        self.assertIn("total_size", data)


if __name__ == "__main__":
    unittest.main()