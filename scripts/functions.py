# Import required libraries
from dotenv import dotenv_values, load_dotenv  # For loading environment variables from .env file
import requests  # For making HTTP requests to ClickUp API
import json  # For JSON data handling (if needed)

# Load environment variables from .env file
config = dotenv_values("../.env")
# Retrieve ClickUp API key from environment variables
CLICKUP_API_KEY = config.get("CLICKUP_API_KEY", "")

# ClickUp API base URL (v2 endpoint)
CLICKUP_BASE_URL = "https://api.clickup.com/api/v2"

# Set up HTTP headers for API authentication
# ClickUp API requires the API key in the Authorization header
headers = {
    "Authorization": CLICKUP_API_KEY
}


def get_teams():
    """
    Retrieve all teams associated with the authenticated user.
    
    Returns:
        dict: JSON response containing all teams
    """
    response = requests.get(f"{CLICKUP_BASE_URL}/team", headers=headers)
    return response.json()


def get_spaces(team_id):
    """
    Retrieve all spaces within a specific team.
    
    Args:
        team_id (str): The ID of the team
        
    Returns:
        dict: JSON response containing all spaces in the team
    """
    response = requests.get(f"{CLICKUP_BASE_URL}/team/{team_id}/space", headers=headers)
    return response.json()


def get_folders(space_id):
    """
    Retrieve all folders within a specific space.
    
    Args:
        space_id (str): The ID of the space
        
    Returns:
        dict: JSON response containing all folders in the space
    """
    response = requests.get(f"{CLICKUP_BASE_URL}/space/{space_id}/folder", headers=headers)
    return response.json()


def get_lists_by_space(space_id):
    """
    Retrieve all lists within a specific space.
    
    Args:
        space_id (str): The ID of the space
        
    Returns:
        dict: JSON response containing all lists in the space
    """
    response = requests.get(f"{CLICKUP_BASE_URL}/space/{space_id}/list", headers=headers)
    return response.json()


def get_lists_by_folder(folder_id):
    """
    Retrieve all lists within a specific folder.
    
    Args:
        folder_id (str): The ID of the folder
        
    Returns:
        dict: JSON response containing all lists in the folder
    """
    response = requests.get(f"{CLICKUP_BASE_URL}/folder/{folder_id}/list", headers=headers)
    return response.json()


def get_tasks(list_id):
    """
    Retrieve all tasks within a specific list.
    
    Args:
        list_id (str): The ID of the list
        
    Returns:
        dict: JSON response containing all tasks in the list
    """
    response = requests.get(f"{CLICKUP_BASE_URL}/list/{list_id}/task", headers=headers)
    return response.json()

