# Import functions from functions.py
from functions import (
    get_teams,
    get_spaces,
    get_folders,
    get_lists_by_space,
    get_lists_by_folder,
    get_tasks
)

# Main execution: Loop through teams, spaces, folders, lists, and tasks
# Step 1: Get all teams
teams_data = get_teams()

# Step 2: Loop through teams and spaces
# Iterate through each team to access its spaces
for team in teams_data["teams"]:
    team_id = team["id"]
    # Get all spaces within the current team
    spaces_data = get_spaces(team_id)
    
    # Iterate through each space to access its lists
    for space in spaces_data["spaces"]:
        space_id = space["id"]
        print(f"Space: {space['name']}")
        
        # Get all lists within the current space
        lists_data = get_lists_by_space(space_id)
              
        # Iterate through each list to access its tasks
        for list in lists_data["lists"]:
            print(f"  List: {list['name']}")
            list_id = list["id"]
            # Get all tasks within the current list
            tasks_data = get_tasks(list_id)
            
            # Iterate through each task and print its name
            for task in tasks_data["tasks"]:
                print(f"      Task: {task['name']}")
                
        # Get all folders within the current space
        folders_data = get_folders(space_id)
        
        # Iterate through each folder and print its name
        for folder in folders_data["folders"]:
            print(f"  Folder: {folder['name']}")
            folder_id = folder["id"]
            # Get all lists within the current folder
            lists_data = get_lists_by_folder(folder_id)
            # Iterate through each list and print its name
            for list in lists_data["lists"]:
                print(f"    List: {list['name']}")
                list_id = list["id"]
                # Get all tasks within the current list
                tasks_data = get_tasks(list_id)
                # Iterate through each task and print its name
                for task in tasks_data["tasks"]:
                    print(f"      Task: {task['name']}")