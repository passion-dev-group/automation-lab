from functions import get_teams, get_spaces, get_folders, get_lists_by_space, get_lists_by_folder, get_tasks, get_custom_fields, update_task, set_custom_field
from datetime import datetime, timezone
import sys

def find_incoming_tasks_list():
    """
    Find the 'Incoming Tasks' list by traversing the ClickUp hierarchy.
    
    Returns:
        str: The list ID of 'Incoming Tasks', or None if not found
    """
    # Get all teams
    teams_response = get_teams()
    if 'teams' not in teams_response:
        print("Error: Could not retrieve teams")
        return None
    
    # Iterate through teams
    for team in teams_response['teams']:
        team_id = team['id']
        
        # Get spaces for this team
        spaces_response = get_spaces(team_id)
        if 'spaces' not in spaces_response:
            continue
        
        # Iterate through spaces
        for space in spaces_response['spaces']:
            space_id = space['id']
            
            # Check lists directly in space
            lists_response = get_lists_by_space(space_id)
            if 'lists' in lists_response:
                for list_item in lists_response['lists']:
                    if list_item.get('name') == 'Incoming Tasks':
                        return list_item['id']
            
            # Check folders in space
            folders_response = get_folders(space_id)
            if 'folders' not in folders_response:
                continue
            
            # Iterate through folders
            for folder in folders_response['folders']:
                folder_id = folder['id']
                
                # Get lists in folder
                lists_response = get_lists_by_folder(folder_id)
                if 'lists' in lists_response:
                    for list_item in lists_response['lists']:
                        if list_item.get('name') == 'Incoming Tasks':
                            return list_item['id']
    
    return None


def is_created_today(task):
    """
    Check if a task was created today.
    
    Args:
        task (dict): Task object from ClickUp API
        
    Returns:
        bool: True if task was created today, False otherwise
    """
    # Get the date_created timestamp (in milliseconds)
    date_created_ms = task.get('date_created', 0)
    
    # Handle case where date_created might be None or empty
    if not date_created_ms:
        return False
    
    # Convert string to int/float if needed (ClickUp API returns it as string)
    try:
        date_created_ms = int(date_created_ms)
    except (ValueError, TypeError):
        return False
    
    # Convert to datetime
    date_created = datetime.fromtimestamp(date_created_ms / 1000, tz=timezone.utc)
    
    # Get today's date in UTC
    today = datetime.now(timezone.utc).date()
    
    # Compare dates
    return date_created.date() == today


def find_type_field_id(list_id):
    """Find the Type custom field ID."""
    try:
        fields = get_custom_fields(list_id)
        if 'fields' in fields:
            for field in fields['fields']:
                if field.get('name') == 'Type':
                    return field['id']
    except:
        pass
    return None


def apply_rules(task, type_field_id):
    """Apply processing rules to a task."""
    task_id = task.get('id')
    title = task.get('name', '')
    description = task.get('description', '')
    
    # Rule 1: If title starts with "Lead:", set Type = Lead
    if title.startswith('Lead:'):
        if type_field_id:
            try:
                set_custom_field(task_id, type_field_id, 'Lead')
                print(f"  ✓ Set Type = Lead")
            except Exception as e:
                print(f"  ✗ Error setting Type: {e}")
    
    # Rule 2: If title starts with "Bug:", set Type = Bug and priority = High
    elif title.startswith('Bug:'):
        if type_field_id:
            try:
                set_custom_field(task_id, type_field_id, 'Bug')
                print(f"  ✓ Set Type = Bug")
            except Exception as e:
                print(f"  ✗ Error setting Type: {e}")
        
        try:
            update_task(task_id, {'priority': 2})  # 2 = High priority
            print(f"  ✓ Set priority = High")
        except Exception as e:
            print(f"  ✗ Error setting priority: {e}")
    
    # Rule 3: If description contains "urgent", add tag urgent
    if description and 'urgent' in description.lower():
        current_tags = task.get('tags', [])
        tag_names = [tag.get('name', tag) if isinstance(tag, dict) else str(tag) for tag in current_tags]
        
        if 'urgent' not in [name.lower() for name in tag_names]:
            try:
                updated_tags = tag_names + ['urgent']
                update_task(task_id, {'tags': updated_tags})
                print(f"  ✓ Added tag 'urgent'")
            except Exception as e:
                print(f"  ✗ Error adding tag: {e}")


def main():
    # Find the 'Incoming Tasks' list
    print("Searching for 'Incoming Tasks' list...")
    list_id = find_incoming_tasks_list()
    
    if not list_id:
        print("Error: Could not find 'Incoming Tasks' list")
        sys.exit(1)
    
    print(f"Found 'Incoming Tasks' list (ID: {list_id})")
    
    # Find Type custom field ID
    print("Finding Type custom field...")
    type_field_id = find_type_field_id(list_id)
    if type_field_id:
        print(f"Found Type field (ID: {type_field_id})")
    else:
        print("Warning: Type field not found")
    
    print("\nFetching tasks...")
    
    # Get all tasks from the list
    tasks_response = get_tasks(list_id)
    
    if 'tasks' not in tasks_response:
        print("Error: Could not retrieve tasks")
        sys.exit(1)
    
    # Filter tasks created today
    today_tasks = [task for task in tasks_response['tasks'] if is_created_today(task)]
    
    if not today_tasks:
        print("\nNo tasks created today in 'Incoming Tasks' list.")
        return
    
    # Process tasks
    print(f"\nFound {len(today_tasks)} task(s) created today:\n")
    print("-" * 80)
    print(f"{'ID':<20} {'Name':<40} {'Status':<20}")
    print("-" * 80)
    
    for task in today_tasks:
        task_id = task.get('id', 'N/A')
        task_name = task.get('name', 'N/A')
        status = task.get('status', {})
        status_name = status.get('status', 'N/A') if isinstance(status, dict) else str(status)
        
        print(f"{task_id:<20} {task_name:<40} {status_name:<20}")
        
        # Apply processing rules
        apply_rules(task, type_field_id)
    
    print("-" * 80)
    print("\nDone!")


if __name__ == "__main__":
    main()

