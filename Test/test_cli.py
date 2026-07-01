import os
import unittest
import subprocess
import sys
import tempfile
import shutil
from pathlib import Path


class TestCLI(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.test_file = Path(self.temp_dir) / "test.txt"
        self.test_file.write_text("hello")

        # cli.py лежит в папке src
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.cli_path = os.path.join(project_root, "src", "cli.py")

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def run_cli(self, args):
        """Запуск cli.py с аргументами (с utf-8 кодировкой)"""
        cmd = [sys.executable, self.cli_path] + args
        return subprocess.run(
            cmd,
            cwd=self.temp_dir,
            capture_output=True,
            text=True,
            encoding='utf-8'  # 👈 ФИКС: правильная кодировка
        )

    def test_cli_copy(self):
        result = self.run_cli(["copy", "test.txt", "copy.txt"])
        self.assertEqual(result.returncode, 0, f"stdout: {result.stdout}, stderr: {result.stderr}")
        self.assertTrue((Path(self.temp_dir) / "copy.txt").exists())

    def test_cli_delete(self):
        result = self.run_cli(["delete", "test.txt"])
        self.assertEqual(result.returncode, 0, f"stdout: {result.stdout}, stderr: {result.stderr}")
        self.assertFalse((Path(self.temp_dir) / "test.txt").exists())

    def test_cli_count(self):
        result = self.run_cli(["count", "."])
        self.assertEqual(result.returncode, 0, f"stdout: {result.stdout}, stderr: {result.stderr}")
        self.assertIn("Файлов: 1", result.stdout)

    def test_cli_search(self):
        result = self.run_cli(["search", ".", r"\.txt$"])
        self.assertEqual(result.returncode, 0, f"stdout: {result.stdout}, stderr: {result.stderr}")
        self.assertIn("test.txt", result.stdout)

    def test_cli_help(self):
        result = self.run_cli(["--help"])
        self.assertEqual(result.returncode, 0, f"stdout: {result.stdout}, stderr: {result.stderr}")
        self.assertIn("copy", result.stdout)
        self.assertIn("delete", result.stdout)


if __name__ == "__main__":
    unittest.main()