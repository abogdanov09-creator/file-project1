import os
import unittest
import tempfile
import shutil
import time
from pathlib import Path
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.file_manager import add_date_to_filename


class TestAddDate(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.test_file = Path(self.temp_dir) / "test.txt"
        self.test_file.write_text("content")
        time.sleep(0.1)

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_add_date_dry_run(self):
        success, message, data = add_date_to_filename(str(self.test_file), dry_run=True)
        self.assertTrue(success)
        self.assertIn("DRY RUN", message)
        self.assertTrue(self.test_file.exists())

    def test_add_date_real(self):
        old_name = self.test_file.name
        success, message, data = add_date_to_filename(str(self.test_file), dry_run=False)
        self.assertTrue(success)
        new_files = [f for f in Path(self.temp_dir).iterdir() if f.is_file()]
        self.assertEqual(len(new_files), 1)
        self.assertNotEqual(new_files[0].name, old_name)


if __name__ == "__main__":
    unittest.main()