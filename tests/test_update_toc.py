
"""
Unit tests for update_toc.py.

Tests the surgical update of filenames in myst.yml based on the presence of
files in the sessions directory, ensuring regex replacements work correctly
and do not scramble the file structure.
"""

import unittest
from unittest.mock import patch, mock_open, MagicMock
import sys
import os

# Adjust path to import the script under test
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../scripts')))

import update_toc

class TestUpdateToc(unittest.TestCase):

    @patch('update_toc.os.path.exists')
    @patch('update_toc.glob.glob')
    @patch('builtins.open', new_callable=mock_open)
    def test_update_toc_filenames(self, mock_file, mock_glob, mock_exists):
        """Test that filenames in myst.yml are updated to match files on disk."""
        
        mock_exists.return_value = True
        
        # Mock file system: exists '01-new-name.md' in sessions
        # The script uses glob.glob(os.path.join(SESSIONS_DIR, '[0-9][0-9]-*.md'))
        mock_glob.return_value = [
            os.path.join('sessions', '01-new-name.md'),
            os.path.join('sessions', '02-unchanged.md')
        ]
        
        # Mock initial myst.yml content
        initial_yaml = """version: 1
project:
  toc:
    - title: Week 1
      children:
      - file: sessions/01-old-name.md
      - file: activities/01-lab.md
    - title: Week 2
      children:
      - file: sessions/02-unchanged.md
        """
        
        # Configure file mock
        # We need independent mocks for reading and writing if we want to be precise,
        # but mock_open handles read_data for all reads by default unless side_effect used.
        # Since we read once then write once, simple read_data is fine for the read.
        
        mock_file.return_value.read.return_value = initial_yaml

        # Reset the mock to clear the read calls from setup if any (though none here)
        # Actually, we need to capture the write.
        
        update_toc.main()
        
        # Verify Write
        # Get the handle used for writing
        handle = mock_file()
        
        # Verify content written
        # Check if write was called
        handle.write.assert_called()
        
        written_content = handle.write.call_args[0][0]
        
        # Assertions
        # 1. 01-old-name.md should be replaced by 01-new-name.md
        self.assertIn("file: sessions/01-new-name.md", written_content)
        self.assertNotIn("01-old-name.md", written_content)
        
        # 2. 02-unchanged.md should handle being "replaced" by itself gracefully (or regex just matches same)
        self.assertIn("file: sessions/02-unchanged.md", written_content)
        
        # 3. Structure preservation: activities link should remains
        self.assertIn("file: activities/01-lab.md", written_content)

if __name__ == '__main__':
    unittest.main()
