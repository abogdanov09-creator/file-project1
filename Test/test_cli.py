import unittest
from unittest.mock import patch
import sys
from src.cli import main


class TestCLI(unittest.TestCase):
    """Тесты для командной строки"""

    @patch('src.file_manager.copy_file')
    def test_copy_command(self, mock_copy):
        """Тест команды copy"""
        test_args = ['cli.py', 'copy', 'test.txt', 'new.txt']
        with patch.object(sys, 'argv', test_args):
            main()
        mock_copy.assert_called_once_with('test.txt', 'new.txt')

    @patch('src.file_manager.delete_item')
    def test_delete_command(self, mock_delete):
        """Тест команды delete"""
        test_args = ['cli.py', 'delete', 'test.txt']
        with patch.object(sys, 'argv', test_args):
            main()
        mock_delete.assert_called_once_with('test.txt')

    @patch('src.file_manager.count_files')
    def test_count_command(self, mock_count):
        """Тест команды count"""
        test_args = ['cli.py', 'count', 'folder']
        with patch.object(sys, 'argv', test_args):
            main()
        mock_count.assert_called_once_with('folder')

    @patch('src.file_manager.search_files')
    def test_search_command(self, mock_search):
        """Тест команды search"""
        test_args = ['cli.py', 'search', 'folder', '.*\.txt']
        with patch.object(sys, 'argv', test_args):
            main()
        mock_search.assert_called_once_with('folder', '.*\.txt')

    @patch('src.file_manager.add_date_to_filename')
    def test_add_date_command(self, mock_add_date):
        """Тест команды add-date"""
        test_args = ['cli.py', 'add-date', 'file.txt', '--recursive']
        with patch.object(sys, 'argv', test_args):
            main()
        mock_add_date.assert_called_once_with('file.txt', True)

    @patch('src.file_manager.analyse_folder')
    def test_analyse_command(self, mock_analyse):
        """Тест команды analyse"""
        test_args = ['cli.py', 'analyse', 'folder']
        with patch.object(sys, 'argv', test_args):
            main()
        mock_analyse.assert_called_once_with('folder')


if __name__ == "__main__":
    unittest.main()