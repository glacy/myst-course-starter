import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add scripts directory to path to import scaffold_course
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../scripts')))
import scaffold_course

class TestScaffoldCourse(unittest.TestCase):

    @patch('scaffold_course.subprocess.run')
    @patch('builtins.print')
    @patch('pathlib.Path.exists')
    def test_run_step_success(self, mock_exists, mock_print, mock_run):
        """Test run_step executes command successfully."""
        mock_run.return_value.returncode = 0
        
        scaffold_course.run_step("Test Step", ["echo", "test"])
        
        mock_run.assert_called_with(["echo", "test"], check=True, text=True)

    @patch('scaffold_course.sys.exit')
    @patch('builtins.input')
    @patch('pathlib.Path.exists')
    def test_force_prompt_no(self, mock_exists, mock_input, mock_exit):
        """Test that --force prompts the user and exits if answer is not 'y'."""
        mock_exists.return_value = True # planeamiento.json exists
        mock_input.return_value = 'n'
        
        with patch('argparse.ArgumentParser.parse_args') as mock_args:
            mock_args.return_value = MagicMock(force=True, yes=False, lang='es')
            
            scaffold_course.main()
            
            mock_input.assert_called_once()
            mock_exit.assert_called_with(0)

    @patch('scaffold_course.subprocess.run')
    @patch('builtins.input')
    @patch('pathlib.Path.exists')
    def test_force_yes_skips_prompt(self, mock_exists, mock_input, mock_run):
        """Test that --force --yes works without prompting."""
        mock_exists.return_value = True
        
        with patch('argparse.ArgumentParser.parse_args') as mock_args:
            mock_args.return_value = MagicMock(force=True, yes=True, lang='es')
            
            # Mock implicit subprocess calls to avoid actual execution
            mock_run.return_value.returncode = 0
            
            # We expect main to run through without exiting or inputting
            # However, main() does a lot of stuff. We should probably mock run_step too 
            # or just verify input wasn't called.
            
            # To catch the end of main without errors, we might mock run_step calls.
            # But run_step calls subprocess.run which we mocked.
            # But the script also does direct Path operations (mkdir).
            # Let's mock the other parts of main logic to isolate the prompt check.
            
            with patch('scaffold_course.Path.mkdir'), \
                 patch('scaffold_course.open'), \
                 patch('json.load'):
                 
                scaffold_course.main()
                
            mock_input.assert_not_called()

if __name__ == '__main__':
    unittest.main()
