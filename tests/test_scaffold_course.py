import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add scripts directory to path to import scaffold_course
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../scripts')))
import scaffold_course

class TestScaffoldCourse(unittest.TestCase):

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

    @patch('scaffold_course.generate_sessions_table_json.run')
    @patch('scaffold_course.inject_activity_header.run')
    @patch('scaffold_course.update_toc.main')
    @patch('scaffold_course.sync_myst.main')
    @patch('scaffold_course.generate_sessions.run')
    @patch('scaffold_course.generate_activities.run')
    @patch('scaffold_course.generate_program.run')
    @patch('scaffold_course.create_myst_config')
    @patch('builtins.input')
    @patch('pathlib.Path.exists')
    def test_force_yes_skips_prompt(self, mock_exists, mock_input, mock_create_config, mock_gen_prog, mock_gen_act, mock_gen_sess, mock_sync, mock_update_toc, mock_inject, mock_gen_table):
        """Test that --force --yes works without prompting and calls all steps."""
        mock_exists.return_value = True
        
        with patch('argparse.ArgumentParser.parse_args') as mock_args:
            mock_args.return_value = MagicMock(force=True, yes=True, lang='es')
            
            with patch('scaffold_course.Path.mkdir'):
                scaffold_course.main()
                
            mock_input.assert_not_called()
            mock_create_config.assert_called()
            mock_gen_prog.assert_called()
            mock_gen_sess.assert_called()
            mock_sync.assert_called()
            mock_update_toc.assert_called()
            mock_gen_act.assert_called()
            mock_inject.assert_called()
            mock_gen_table.assert_called()

if __name__ == '__main__':
    unittest.main()
