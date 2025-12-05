# Day 11 - Python: classify & update tasks

1. Added task update functions to `functions.py`
   - `get_custom_fields(list_id)` - Retrieves custom fields for a list
   - `update_task(task_id, data)` - Updates task properties (priority, tags, etc.)
   - `set_custom_field(task_id, field_id, value)` - Sets custom field values

2. Implemented processing rules in `process_tasks.py`
   - Created `find_type_field_id()` function to locate the Type custom field
   - Created `apply_rules()` function to classify and update tasks based on rules:
     - **Rule 1:** If title starts with "Lead:", sets Type custom field = Lead
     - **Rule 2:** If title starts with "Bug:", sets Type custom field = Bug and priority = High
     - **Rule 3:** If description contains word "urgent", adds tag "urgent"

3. Integrated rule processing into main workflow
   - Script now automatically finds Type custom field before processing tasks
   - Each task is analyzed based on its title (name) and description
   - Rules are applied sequentially with error handling for each operation
   - Provides visual feedback (✓/✗) for each action taken

4. Simplified implementation approach
   - Direct use of task title (name field) and description from ClickUp API
   - Straightforward rule matching without complex logic
   - Clear separation between rule checking and task updates

