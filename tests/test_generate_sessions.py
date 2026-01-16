
"""
Unit tests for the generate_sessions.py script.

Tests the filename generation logic, standard file creation workflow, duplicate handling (counter appending),
and week filtering functionality using mocking to avoid actual file system IO.
"""

import unittest
from unittest.mock import patch, mock_open, MagicMock
import os
import sys
import json
import argparse

# Mock yaml module before importing generate_sessions
# This allows tests to run even if yaml is not installed
sys.modules['yaml'] = MagicMock()
sys.modules['yaml'].dump = lambda data, **kwargs: "mocked_yaml_output"

# Adjust path to import the script under test
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../scripts')))

import generate_sessions

class TestGenerateSessions(unittest.TestCase):

    def test_generate_filename(self):
        """Test filename generation with various inputs."""
        self.assertEqual(generate_sessions.generate_filename(1, "Sesión de Introducción"), "01-sesion-de-introduccion.md")
        self.assertEqual(generate_sessions.generate_filename(2, "Ángulos y Energías"), "02-angulos-y-energias.md")
        self.assertEqual(generate_sessions.generate_filename(10, "  Trim Spaces  "), "10-trim-spaces.md")
        self.assertEqual(generate_sessions.generate_filename(5, "Title with   Multiple Spaces"), "05-title-with-multiple-spaces.md")

    @patch('generate_sessions.os.makedirs')
    @patch('generate_sessions.os.path.exists')
    @patch('generate_sessions.json.load')
    @patch('builtins.open', new_callable=mock_open)
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_standard_generation(self, mock_args, mock_file, mock_json_load, mock_exists, mock_makedirs):
        """Test standard generation flow."""
        # Setup mocks
        mock_args.return_value = argparse.Namespace(week=None, force=False, lang='es')
        mock_exists.side_effect = lambda x: False # Output dir doesn't exist initially, file doesn't exist
        mock_json_load.return_value = [
            {
                "week": 1,
                "title": "Contenido 1",
                "content": ["Contenido 1"],
                "objectives": ["Obj 1"],
                "activities": "Activity 1",
                "evaluation": [{"type": "Test", "description": "Desc"}],
                "references": [{"text": "Ref 1"}]
            }
        ]

        generate_sessions.main()

        # Verify calls
        mock_makedirs.assert_called_with('sessions')
        # Check if file was opened for writing (ignoring the read open for json)
        # We expect 2 open calls: 1 for reading JSON (which we mocked via json.load but opened via builtins.open context), 
        # and 1 for writing markdown.
        # Since we mocked open, we can check calls.
        
        # Verify write call (Session 1)
        # The exact path depends on how it's constructed in the script, using the title
        expected_path = os.path.join('sessions', '01-contenido-1.md')
        mock_file.assert_any_call(expected_path, 'w', encoding='utf-8')
        
        # Verify content was written
        handle = mock_file()
        handle.write.assert_called()
        
        # Get the written content to inspect
        # write might be called multiple times, we want to check the body
        written_content = "".join(call.args[0] for call in handle.write.call_args_list)
        
        # Verification 1: Check for badge format
        # Contenido 1 -> https://img.shields.io/badge/-Contenido_1-lightgrey
        expected_badge = "https://img.shields.io/badge/-Contenido_1-lightgrey"
        self.assertIn(expected_badge, written_content)
        
        # Verification 2: Check for order (Badges before Objectives)
        badge_pos = written_content.find(expected_badge)
        objectives_pos = written_content.find(":::{note} Objetivos")
        
        self.assertNotEqual(badge_pos, -1, "Badge not found")
        self.assertNotEqual(objectives_pos, -1, "Objectives block not found")
        self.assertLess(badge_pos, objectives_pos, "Content badges should appear before Objectives")

    @patch('generate_sessions.os.makedirs')
    @patch('generate_sessions.os.path.exists')
    @patch('generate_sessions.json.load')
    @patch('builtins.open', new_callable=mock_open)
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_skip_existing_without_force(self, mock_args, mock_file, mock_json_load, mock_exists, mock_makedirs):
        """Test that the script skips existing files if --force is not provided."""
        mock_args.return_value = argparse.Namespace(week=None, force=False, lang='es')
        
        mock_json_load.return_value = [
            {"week": 1, "title": "Topic", "content": ["Topic"]}
        ]

        def exists_side_effect(path):
            if path == 'sessions': return True
            if path.endswith('01-topic.md'): return True
            return False

        mock_exists.side_effect = exists_side_effect

        generate_sessions.main()

        expected_path = os.path.join('sessions', '01-topic.md')
        # Should NOT write
        with self.assertRaises(AssertionError):
             mock_file.assert_any_call(expected_path, 'w', encoding='utf-8')

    @patch('generate_sessions.os.makedirs')
    @patch('generate_sessions.os.path.exists')
    @patch('generate_sessions.json.load')
    @patch('builtins.open', new_callable=mock_open)
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_force_overwrite(self, mock_args, mock_file, mock_json_load, mock_exists, mock_makedirs):
        """Test that the script overwrites existing files if --force IS provided."""
        mock_args.return_value = argparse.Namespace(week=None, force=True, lang='es')
        
        mock_json_load.return_value = [
            {"week": 1, "title": "Topic", "content": ["Topic"]}
        ]

        def exists_side_effect(path):
            if path == 'sessions': return True
            if path.endswith('01-topic.md'): return True
            return False

        mock_exists.side_effect = exists_side_effect

        generate_sessions.main()

        expected_path = os.path.join('sessions', '01-topic.md')
        # Should write
        mock_file.assert_any_call(expected_path, 'w', encoding='utf-8')


    @patch('generate_sessions.os.makedirs')
    @patch('generate_sessions.os.path.exists')
    @patch('generate_sessions.json.load')
    @patch('builtins.open', new_callable=mock_open)
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_filter_week(self, mock_args, mock_file, mock_json_load, mock_exists, mock_makedirs):
        """Test generating a specific week."""
        mock_args.return_value = argparse.Namespace(week=2, force=False, lang='es')
        mock_exists.return_value = False
        
        mock_json_load.return_value = [
            {"week": 1, "title": "Topic 1", "content": ["Topic 1"]},
            {"week": 2, "title": "Topic 2", "content": ["Topic 2"]}
        ]

        generate_sessions.main()

        # Should only write week 2
        path_week_1 = os.path.join('sessions', '01-topic-1.md')
        path_week_2 = os.path.join('sessions', '02-topic-2.md')

        with self.assertRaises(AssertionError):
             mock_file.assert_any_call(path_week_1, 'w', encoding='utf-8')
        
        mock_file.assert_any_call(path_week_2, 'w', encoding='utf-8')

if __name__ == '__main__':
    unittest.main()
