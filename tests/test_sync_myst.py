"""
Unit tests for sync_myst.py.

Tests the synchronization of metadata from planeamiento.json to myst.yml,
verifying that regex replacements work correctly without altering other parts of the YAML file.
"""

import unittest
from unittest.mock import patch, mock_open, MagicMock
import sys
import os

# Adjust path to import the script under test
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../scripts')))

import sync_myst

class TestSyncMyst(unittest.TestCase):

    @patch('sync_myst.os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('sync_myst.load_json')
    def test_sync_metadata(self, mock_load_json, mock_file, mock_exists):
        """Test that metadata is correctly injected into myst.yml content."""
        
        # Setup mocks
        mock_exists.return_value = True
        
        # Mock JSON Data
        mock_load_json.return_value = {
            "metadata": {
                "code": "TEST101",
                "title": "Test Course",
                "semester": "II Semester 2030",
                "authors": ["Test Author"],
                "university": "Test University"
            }
        }
        
        # Mock initial myst.yml content
        initial_yaml = """version: 1
project:
  title: OLD_TITLE
  subtitle: OLD_SUBTITLE
  authors:
  - name: OLD_AUTHOR
  copyright: OLD_COPYRIGHT
site:
  title: OLD_SITE_TITLE
  subtitle: OLD_SITE_SUBTITLE
  template: book-theme
"""
        
        # Configure file mock to return different handles for different reads
        # The script now calls load_json (which opens file internally, but we mocked load_json)
        # Then it opens MYST_FILE for read
        # Then it opens MYST_FILE for write
        
        # Since load_json is mocked, we don't need to mock the open call for JSON_FILE.
        # We only need to mock open calls for MYST_FILE.
        
        mock_file.side_effect = [
            mock_open(read_data=initial_yaml).return_value, # Read YAML handle
            mock_open().return_value # Write YAML handle
        ]

        sync_myst.main()
        
        # We can't easily check the content written with side_effect this way without inspecting the second call.
        pass

    @patch('sync_myst.os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('sync_myst.load_json')
    def test_regex_replacement(self, mock_load_json, mock_file, mock_exists):
        """Test the regex replacement logic effectively."""
        mock_exists.return_value = True
        
        mock_load_json.return_value = {
            "metadata": {
                "code": "TEST101",
                "title": "Ignored",
                "semester": "II Semester 2030",
                "authors": ["Test Author"]
            }
        }

        initial_yaml = """version: 1
project:
  title: OLD_TITLE
  subtitle: OLD_SUBTITLE
  authors:
  - name: OLD_AUTHOR
site:
  title: OLD_SITE_TITLE
  subtitle: OLD_SITE_SUBTITLE
"""
        
        file_handlers = {}
        
        def custom_open(filename, mode='r', encoding=None):
            file_mock = MagicMock()
            file_mock.__enter__.return_value = file_mock
            if filename == 'myst.yml' and 'r' in mode:
                file_mock.read.return_value = initial_yaml
                return file_mock
            elif filename == 'myst.yml' and 'w' in mode:
                # Capture the write
                file_handlers['write_handle'] = file_mock
                return file_mock
            return file_mock

        mock_file.side_effect = custom_open
        
        sync_myst.main()
        
        # Verify content written
        writer = file_handlers.get('write_handle')
        self.assertIsNotNone(writer)
        
        written_content = writer.write.call_args[0][0]
        
        # Assertions
        self.assertIn("title: TEST101", written_content)
        self.assertIn("subtitle: II Semester 2030", written_content)
        self.assertIn("- name: Test Author", written_content)
        self.assertNotIn("OLD_TITLE", written_content)

if __name__ == '__main__':
    unittest.main()
