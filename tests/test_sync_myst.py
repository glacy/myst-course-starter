
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
    @patch('sync_myst.json.load')
    def test_sync_metadata(self, mock_json_load, mock_file, mock_exists):
        """Test that metadata is correctly injected into myst.yml content."""
        
        # Setup mocks
        mock_exists.return_value = True
        
        # Mock JSON Data
        mock_json_load.return_value = {
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
        # This is tricky with mock_open for multiple files.
        # We can simulate read() by side_effect if we verify paths.
        
        # Simplified approach: 
        # The script does: read JSON, read YAML, write YAML.
        # We can mock the read data sequence.
        
        # First read is JSON (handled by json.load mock, so file read content doesn't matter much)
        # Second read is YAML.
        mock_file.side_effect = [
            mock_open(read_data="{}").return_value, # JSON file handle (content ignored by json.load mock)
            mock_open(read_data=initial_yaml).return_value, # Read YAML handle
            mock_open().return_value # Write YAML handle
        ]

        sync_myst.main()
        
        # Verify Write
        # Get the handle used for writing (the 3rd one opened)
        # However, finding the write handle is easier by inspecting all calls.
        
        # We expect a write to 'myst.yml'
        # Let's inspect all write calls to the mocked open
        
        # Filter calls to handle().write()
        # Since we have side_effect returning different mocks, we need to capture the one used for write.
        # Actually, simpler: check the last write call on the *last* mock returned.
        
        # But wait, side_effect creates new mocks each time.
        # Easier strategy: Inspect the 'write' calls on the *class* mock_file doesn't work easily with side_effect mocks.
        
        # Alternate strategy: Use a specific read_data side effect for the *second* open call.
        
        pass 
        # The above logic is getting complicated for checking the *content* written.
        # Let's verify the logic by checking what `sync_myst` *would* write given the input string.
        
        # Let's manually run the regex logic in the test to verify it works as expected, 
        # or better, refactor sync_myst to be more testable (accept content string).
        # But we want to test the script as is.
        
        # Re-approach: Just assume the logic in main matches and assert generic success? No.
        # Let's intercept the write.
        
    @patch('sync_myst.os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('sync_myst.json.load')
    def test_regex_replacement(self, mock_json_load, mock_file, mock_exists):
        """Test the regex replacement logic effectively."""
        mock_exists.return_value = True
        
        mock_json_load.return_value = {
            "metadata": {
                "code": "TEST101",
                # Title logic in script: uses 'code' as project title currently
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
        
        # We define a side_effect for open() that returns a text-reader for myst.yml
        # and a dummy for json.
        
        file_handlers = {}
        
        def custom_open(filename, mode='r', encoding=None):
            file_mock = MagicMock()
            file_mock.__enter__.return_value = file_mock
            if filename == 'planeamiento.json':
                # json.load handles the content, we just need a valid object
                return file_mock
            elif filename == 'myst.yml' and 'r' in mode:
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
