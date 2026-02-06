"""
Unit tests for the Natural Language Processor in the AI Todo Assistant.
Tests the intent recognition and command processing functionality.
"""

import pytest
from backend.src.services.natural_language_processor import NaturalLanguageProcessor


def test_natural_language_processor_initialization():
    """Test initialization of the NaturalLanguageProcessor."""
    processor = NaturalLanguageProcessor()

    assert processor is not None
    assert hasattr(processor, 'task_service')
    assert hasattr(processor, 'intent_patterns')


def test_recognize_add_intent():
    """Test recognition of add intent with various patterns."""
    processor = NaturalLanguageProcessor()

    # Test "add" pattern
    result = processor.recognize_intent("add buy groceries")
    assert result['intent'] == 'add'
    assert result['task_description'] == 'buy groceries'

    # Test "create" pattern
    result = processor.recognize_intent("create call mom")
    assert result['intent'] == 'add'
    assert result['task_description'] == 'call mom'

    # Test "remember" pattern
    result = processor.recognize_intent("remember walk the dog")
    assert result['intent'] == 'add'
    assert result['task_description'] == 'walk the dog'


def test_recognize_list_intent():
    """Test recognition of list intent with various patterns."""
    processor = NaturalLanguageProcessor()

    # Test "show my tasks"
    result = processor.recognize_intent("show my tasks")
    assert result['intent'] == 'list'

    # Test "list tasks"
    result = processor.recognize_intent("list tasks")
    assert result['intent'] == 'list'

    # Test "what do I need to do"
    result = processor.recognize_intent("what do I need to do?")
    assert result['intent'] == 'list'


def test_recognize_complete_intent():
    """Test recognition of complete intent with various patterns."""
    processor = NaturalLanguageProcessor()

    # Test "done with" pattern
    result = processor.recognize_intent("done with buy groceries")
    assert result['intent'] == 'complete'
    assert result['task_identifier'] == 'buy groceries'

    # Test "mark as done" pattern
    result = processor.recognize_intent("mark buy groceries as done")
    assert result['intent'] == 'complete'
    assert result['task_identifier'] == 'buy groceries'

    # Test "complete" pattern
    result = processor.recognize_intent("complete call mom")
    assert result['intent'] == 'complete'
    assert result['task_identifier'] == 'call mom'


def test_recognize_delete_intent():
    """Test recognition of delete intent with various patterns."""
    processor = NaturalLanguageProcessor()

    # Test "delete" pattern
    result = processor.recognize_intent("delete old files")
    assert result['intent'] == 'delete'
    assert result['task_identifier'] == 'old files'

    # Test "remove" pattern
    result = processor.recognize_intent("remove the appointment")
    assert result['intent'] == 'delete'
    assert result['task_identifier'] == 'the appointment'


def test_recognize_update_intent():
    """Test recognition of update intent with various patterns."""
    processor = NaturalLanguageProcessor()

    # Test "change to" pattern
    result = processor.recognize_intent("change buy milk to buy almond milk")
    assert result['intent'] == 'update'
    assert result['old_task_identifier'] == 'buy milk'
    assert result['new_description'] == 'buy almond milk'

    # Test "update to" pattern
    result = processor.recognize_intent("update call dad to call parents")
    assert result['intent'] == 'update'
    assert result['old_task_identifier'] == 'call dad'
    assert result['new_description'] == 'call parents'


def test_recognize_unknown_intent():
    """Test recognition of unknown intent."""
    processor = NaturalLanguageProcessor()

    result = processor.recognize_intent("this is not a recognized command")
    assert result['intent'] == 'unknown'
    assert 'this is not a recognized command' in result['raw_input']


def test_process_add_command():
    """Test processing of add command."""
    processor = NaturalLanguageProcessor()

    # Test that the process_command method can handle add commands
    # Without mocking the service layer, we test that the function returns the expected structure
    result = processor.process_command("add test task", "user123")

    # The result should have the expected keys for an add operation
    assert 'success' in result
    assert 'message' in result
    assert 'action_taken' in result
    assert result['action_taken'] == 'add'


def test_process_list_command():
    """Test processing of list command."""
    processor = NaturalLanguageProcessor()

    result = processor.process_command("show my tasks", "user123")

    assert 'success' in result
    assert 'message' in result
    assert 'action_taken' in result
    assert result['action_taken'] == 'list'


def test_process_complete_command():
    """Test processing of complete command."""
    processor = NaturalLanguageProcessor()

    result = processor.process_command("done with test task", "user123")

    assert 'success' in result
    assert 'message' in result
    assert 'action_taken' in result
    assert result['action_taken'] == 'complete'


def test_process_delete_command():
    """Test processing of delete command."""
    processor = NaturalLanguageProcessor()

    result = processor.process_command("delete test task", "user123")

    assert 'success' in result
    assert 'message' in result
    assert 'action_taken' in result
    assert result['action_taken'] == 'delete'


def test_process_update_command():
    """Test processing of update command."""
    processor = NaturalLanguageProcessor()

    result = processor.process_command("change test task to updated task", "user123")

    assert 'success' in result
    assert 'message' in result
    assert 'action_taken' in result
    assert result['action_taken'] == 'update'


def test_process_unknown_command():
    """Test processing of unknown command."""
    processor = NaturalLanguageProcessor()

    result = processor.process_command("this is not a valid command", "user123")

    assert 'success' in result
    assert 'message' in result
    assert 'action_taken' in result
    assert result['action_taken'] == 'unknown'
    assert result['success'] is False


def test_enhance_intent_recognition_with_synonyms():
    """Test that synonym enhancement method returns expected mappings."""
    processor = NaturalLanguageProcessor()

    synonyms = processor.enhance_intent_recognition_with_synonyms()

    assert 'add' in synonyms
    assert 'list' in synonyms
    assert 'complete' in synonyms
    assert 'delete' in synonyms
    assert 'update' in synonyms