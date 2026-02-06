"""
Natural language processor for the AI Todo Assistant.
Handles intent recognition and maps natural language to MCP tools.
Enhanced with smart intent recognition and fuzzy matching capabilities.
"""

import re
from typing import Dict, Any, List, Optional
from difflib import SequenceMatcher
from ..services.task_service import TaskService



class NaturalLanguageProcessor:
    """
    Processes natural language commands and maps them to appropriate MCP tools.
    Implements intent recognition for add, list, complete, delete, and update actions.
    Enhanced with fuzzy matching and clarification logic for ambiguous requests.
    """

    def __init__(self):
        """Initialize the natural language processor with action patterns."""
        self.task_service = TaskService()

        # Define patterns for recognizing different intents
        self.intent_patterns = {
            'add': [
                r'^add\s+(.+)$',
                r'^create\s+(.+)$',
                r'^remember\s+(.+)$',
                r'^make\s+(.+)$',
                r'^add\s+task\s+(.+)$',
                r'^i\s+need\s+to\s+(.+)$',
                r'^don\'t\s+forget\s+to\s+(.+)$'
            ],
            'list': [
                r'^(show|list|display)\s+(my|all)?\s*(tasks|todos|todo)$',
                r'^what\s+(do\s+i\s+need\s+to|should\s+i)\s+(do|get\s+done)$',
                r'^(see|view)\s+(my|all)?\s*(tasks|todos|todo)$',
                r'^(show\s+me\s+)?(my\s+)?(current|existing)?\s*(tasks|todos|todo)$',
                r'^what(\'s|s)\s+(there|on\s+my\s+list|left\s+to\s+do)$',
                r'^my\s+(tasks|todos)$'
            ],
            'complete': [
                r'^(done|complete|finished|finish)\s+(with\s+)?(.+)$',
                r'^mark\s+(.+)\s+(as\s+)?(done|complete|finished)$',
                r'^tick\s+(off|complete)\s+(.+)$',
                r'^completed\s+(.+)$',
                r'^did\s+(.+)$',
                r'^i\s+(finished|completed)\s+(.+)$'
            ],
            'delete': [
                r'^(delete|remove|cancel|eliminate|get rid of|trash|erase)\s+(.+)$',
                r'^get\s+rid\s+of\s+(.+)$',
                r'^trash\s+(.+)$',
                r'^remove\s+(.+)$'
            ],
            'update': [
                r'^change\s+(.+)\s+to\s+(.+)$',
                r'^update\s+(.+)\s+to\s+(.+)$',
                r'^rename\s+(.+)\s+to\s+(.+)$',
                r'^modify\s+(.+)\s+to\s+(.+)$',
                r'^switch\s+(.+)\s+to\s+(.+)$',
                r'^alter\s+(.+)\s+to\s+(.+)$'
            ]
        }

        # Enhanced synonym mapping for smart intent recognition
        self.synonym_mappings = {
            'add': ['create', 'remember', 'add', 'make', 'i need to', 'don\'t forget to'],
            'list': ['show', 'display', 'view', 'list', 'what', 'see', 'my', 'tasks', 'todos'],
            'complete': ['done', 'complete', 'finish', 'finished', 'mark', 'completed', 'did', 'finished'],
            'delete': ['delete', 'remove', 'cancel', 'eliminate', 'get rid of', 'trash', 'erase'],
            'update': ['change', 'update', 'rename', 'modify', 'switch', 'alter']
        }

    def recognize_intent(self, user_input: str) -> Dict[str, Any]:
        """
        Recognize the intent from user input and extract relevant parameters.

        Args:
            user_input: The raw user input string

        Returns:
            Dictionary with intent type and extracted parameters
        """
        user_input_lower = user_input.lower().strip()

        # Normalize the input
        normalized_input = re.sub(r'\s+', ' ', user_input_lower).strip()

        # Check for each intent type using regex patterns
        for intent, patterns in self.intent_patterns.items():
            for pattern in patterns:
                match = re.match(pattern, normalized_input)
                if match:
                    groups = match.groups()

                    if intent == 'add':
                        return {'intent': 'add', 'task_description': groups[-1].strip()}
                    elif intent == 'list':
                        return {'intent': 'list'}
                    elif intent == 'complete':
                        # Handle different group patterns for complete
                        if len(groups) >= 3:  # e.g., "done with buy groceries"
                            return {'intent': 'complete', 'task_identifier': groups[-1].strip()}
                        else:  # e.g., "done buy groceries" or "mark buy groceries as done"
                            return {'intent': 'complete', 'task_identifier': groups[0].strip()}
                    elif intent == 'delete':
                        return {'intent': 'delete', 'task_identifier': groups[-1].strip()}
                    elif intent == 'update':
                        # Update has 2 parameters - first is old, last is new
                        if len(groups) >= 2:
                            return {
                                'intent': 'update',
                                'old_task_identifier': groups[0].strip(),
                                'new_description': groups[-1].strip()
                            }

        # If no regex pattern matched, try fuzzy matching with synonyms
        fuzzy_match = self._fuzzy_intent_match(normalized_input)
        if fuzzy_match:
            return fuzzy_match

        # If no pattern matched, return unknown intent
        return {'intent': 'unknown', 'raw_input': user_input}

    def _fuzzy_intent_match(self, user_input: str) -> Optional[Dict[str, Any]]:
        """
        Attempt to match intent using fuzzy matching with synonyms.

        Args:
            user_input: Normalized user input string

        Returns:
            Dictionary with intent type and extracted parameters, or None if no match
        """
        # Split input into words for analysis
        input_words = user_input.split()

        # Score each intent based on how many synonym words are present
        intent_scores = {}
        for intent, synonyms in self.synonym_mappings.items():
            score = 0
            for word in input_words:
                for synonym in synonyms:
                    # Check for exact matches or substring matches
                    if synonym in word or word in synonym:
                        score += 1
                    else:
                        # Use sequence matcher for similarity
                        similarity = SequenceMatcher(None, word, synonym).ratio()
                        if similarity > 0.7:  # High similarity threshold
                            score += similarity

            if score > 0:
                intent_scores[intent] = score

        # If we have any matches, pick the highest scoring intent
        if intent_scores:
            best_intent = max(intent_scores, key=intent_scores.get)

            # Try to extract the task description based on the identified intent
            if best_intent == 'add':
                # Look for the main action content after the verb
                for synonym in self.synonym_mappings['add']:
                    if synonym in user_input:
                        # Extract everything after the verb
                        parts = user_input.split(synonym, 1)
                        if len(parts) > 1 and parts[1].strip():
                            return {'intent': 'add', 'task_description': parts[1].strip()}
            elif best_intent in ['complete', 'delete']:
                # Extract the task identifier
                # Remove intent words to isolate the task
                cleaned_input = user_input
                for synonym in self.synonym_mappings[best_intent]:
                    cleaned_input = cleaned_input.replace(synonym, '').strip()

                # Remove common prepositions
                for prep in ['the', 'task', 'with', 'to', 'on', 'at', 'by']:
                    cleaned_input = cleaned_input.replace(f' {prep} ', ' ').strip()

                if cleaned_input:
                    return {'intent': best_intent, 'task_identifier': cleaned_input.strip()}
            elif best_intent == 'update':
                # Try to identify "change X to Y" patterns even if not caught by regex
                if ' to ' in user_input:
                    parts = user_input.split(' to ', 1)
                    if len(parts) == 2:
                        # Further clean the first part to extract the old task
                        old_parts = parts[0].split()
                        old_task = ' '.join(old_parts[1:])  # Skip the verb
                        new_task = parts[1]

                        if old_task and new_task:
                            return {
                                'intent': 'update',
                                'old_task_identifier': old_task.strip(),
                                'new_description': new_task.strip()
                            }

        return None

    def _find_task_by_fuzzy_matching(self, task_identifier: str, available_tasks: List[Any]) -> Optional[Any]:
        """
        Find a task by fuzzy matching the identifier against available tasks.

        Args:
            task_identifier: The identifier provided by the user
            available_tasks: List of available tasks to match against

        Returns:
            The best matching task or None if no good match found
        """
        if not available_tasks:
            return None

        best_match = None
        best_score = 0

        for task in available_tasks:
            # Direct match first
            if task_identifier.lower() in task.description.lower() or \
               task.description.lower() in task_identifier.lower():
                return task

            # Fuzzy matching using SequenceMatcher
            score1 = SequenceMatcher(None, task_identifier.lower(), task.description.lower()).ratio()
            # Check if identifier matches partially
            score2 = SequenceMatcher(None, task_identifier.lower(), task.description.lower()[:len(task_identifier)]).ratio()

            score = max(score1, score2)

            if score > best_score and score > 0.6:  # Require decent match
                best_score = score
                best_match = task

        return best_match

    def _suggest_possible_tasks(self, task_identifier: str, available_tasks: List[Any], limit: int = 5) -> List[str]:
        """
        Suggest possible tasks when user request is ambiguous.

        Args:
            task_identifier: The identifier provided by the user
            available_tasks: List of available tasks to match against
            limit: Maximum number of suggestions to return

        Returns:
            List of suggested task descriptions
        """
        suggestions = []

        for task in available_tasks:
            if task_identifier.lower() in task.description.lower():
                suggestions.append(task.description)
            elif SequenceMatcher(None, task_identifier.lower(), task.description.lower()).ratio() > 0.5:
                suggestions.append(task.description)

        # If we don't have exact matches, return top similar ones
        if not suggestions and available_tasks:
            scored_tasks = []
            for task in available_tasks:
                score = SequenceMatcher(None, task_identifier.lower(), task.description.lower()).ratio()
                scored_tasks.append((score, task.description))

            # Sort by score descending
            scored_tasks.sort(key=lambda x: x[0], reverse=True)
            suggestions = [task[1] for task in scored_tasks[:limit]]

        return suggestions[:limit]

    def process_command(self, user_input: str, user_id: str, conversation_context: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Process a natural language command and execute the appropriate action.

        Args:
            user_input: The natural language command from the user
            user_id: The ID of the user making the request
            conversation_context: Optional conversation history

        Returns:
            Dictionary with the result of processing
        """
        # Recognize the intent
        intent_result = self.recognize_intent(user_input)
        intent = intent_result['intent']

        try:
            if intent == 'add':
                task_description = intent_result['task_description']
                result = self.task_service.create_task(task_description)

                return {
                    'success': result['success'],
                    'message': result['message'],
                    'action_taken': 'add',
                    'mcp_response': result
                }

            elif intent == 'list':
                result = self.task_service.get_all_tasks()

                # Format the tasks for the response
                formatted_tasks = []
                if result['data']:
                    for task in result['data']:
                        formatted_tasks.append({
                            'id': task.id,
                            'description': task.description,
                            'completed': task.completed,
                            'created_at': task.created_at,
                            'updated_at': task.updated_at
                        })

                return {
                    'success': result['success'],
                    'message': result['message'],
                    'action_taken': 'list',
                    'tasks': formatted_tasks,
                    'mcp_response': result
                }

            elif intent == 'complete':
                task_identifier = intent_result['task_identifier']

                # First, get all tasks to enable fuzzy matching
                all_tasks_result = self.task_service.get_all_tasks()

                if all_tasks_result['success'] and all_tasks_result['data']:
                    # Try to find the task using fuzzy matching
                    matched_task = self._find_task_by_fuzzy_matching(task_identifier, all_tasks_result['data'])

                    if matched_task:
                        # Use the matched task's ID or description for the service call
                        result = self.task_service.mark_task_completed(matched_task.description)
                    else:
                        # If we couldn't match, try to suggest tasks
                        suggestions = self._suggest_possible_tasks(task_identifier, all_tasks_result['data'])

                        if suggestions:
                            suggested_list = ', '.join([f"'{s}'" for s in suggestions])
                            return {
                                'success': False,
                                'message': f"I couldn't find a task matching '{task_identifier}'. Did you mean one of these: {suggested_list}? Please be more specific.",
                                'action_taken': 'clarification_needed',
                                'mcp_response': None
                            }
                        else:
                            # No suggestions available, use the original identifier
                            result = self.task_service.mark_task_completed(task_identifier)
                else:
                    # No tasks available, use the original identifier
                    result = self.task_service.mark_task_completed(task_identifier)

                return {
                    'success': result['success'],
                    'message': result['message'],
                    'action_taken': 'complete',
                    'mcp_response': result
                }

            elif intent == 'delete':
                task_identifier = intent_result['task_identifier']

                # First, get all tasks to enable fuzzy matching
                all_tasks_result = self.task_service.get_all_tasks()

                if all_tasks_result['success'] and all_tasks_result['data']:
                    # Try to find the task using fuzzy matching
                    matched_task = self._find_task_by_fuzzy_matching(task_identifier, all_tasks_result['data'])

                    if matched_task:
                        result = self.task_service.remove_task(matched_task.description)
                    else:
                        # If we couldn't match, try to suggest tasks
                        suggestions = self._suggest_possible_tasks(task_identifier, all_tasks_result['data'])

                        if suggestions:
                            suggested_list = ', '.join([f"'{s}'" for s in suggestions])
                            return {
                                'success': False,
                                'message': f"I couldn't find a task matching '{task_identifier}'. Did you mean one of these: {suggested_list}? Please be more specific.",
                                'action_taken': 'clarification_needed',
                                'mcp_response': None
                            }
                        else:
                            # No suggestions available, use the original identifier
                            result = self.task_service.remove_task(task_identifier)
                else:
                    # No tasks available, use the original identifier
                    result = self.task_service.remove_task(task_identifier)

                return {
                    'success': result['success'],
                    'message': result['message'],
                    'action_taken': 'delete',
                    'mcp_response': result
                }

            elif intent == 'update':
                old_task_identifier = intent_result['old_task_identifier']
                new_description = intent_result['new_description']

                # First, get all tasks to enable fuzzy matching for the old task
                all_tasks_result = self.task_service.get_all_tasks()

                if all_tasks_result['success'] and all_tasks_result['data']:
                    # Try to find the old task using fuzzy matching
                    matched_task = self._find_task_by_fuzzy_matching(old_task_identifier, all_tasks_result['data'])

                    if matched_task:
                        result = self.task_service.modify_task(matched_task.description, new_description)
                    else:
                        # If we couldn't match, try to suggest tasks
                        suggestions = self._suggest_possible_tasks(old_task_identifier, all_tasks_result['data'])

                        if suggestions:
                            suggested_list = ', '.join([f"'{s}'" for s in suggestions])
                            return {
                                'success': False,
                                'message': f"I couldn't find a task matching '{old_task_identifier}'. Did you mean one of these: {suggested_list}? Please be more specific.",
                                'action_taken': 'clarification_needed',
                                'mcp_response': None
                            }
                        else:
                            # No suggestions available, use the original identifier
                            result = self.task_service.modify_task(old_task_identifier, new_description)
                else:
                    # No tasks available, use the original identifiers
                    result = self.task_service.modify_task(old_task_identifier, new_description)

                return {
                    'success': result['success'],
                    'message': result['message'],
                    'action_taken': 'update',
                    'mcp_response': result
                }

            else:
                # Unknown intent
                # First try to get available tasks to provide more helpful response
                tasks_result = self.task_service.get_all_tasks()

                if tasks_result['success'] and tasks_result['data']:
                    task_list = [task.description for task in tasks_result['data']]
                    if task_list:
                        task_summary = ', '.join([f"'{t}'" for t in task_list[:5]])  # Show first 5 tasks
                        if len(task_list) > 5:
                            task_summary += f", and {len(task_list) - 5} more"

                        return {
                            'success': False,
                            'message': f"I didn't understand '{user_input}'. Available commands: add, list, complete, delete, update. Your tasks: {task_summary}",
                            'action_taken': 'unknown',
                            'mcp_response': None
                        }

                return {
                    'success': False,
                    'message': f"Sorry, I didn't understand your request: '{user_input}'. Please try commands like 'add buy groceries', 'show my tasks', 'done with call mom'.",
                    'action_taken': 'unknown',
                    'mcp_response': None
                }

        except Exception as e:
            # Handle any unexpected errors
            return {
                'success': False,
                'message': f"An error occurred while processing your request: {str(e)}",
                'action_taken': 'error',
                'mcp_response': None
            }

    def enhance_intent_recognition_with_synonyms(self):
        """
        Enhance intent recognition with synonyms and variations.
        This method would typically load synonyms from a configuration or database.
        """
        return self.synonym_mappings