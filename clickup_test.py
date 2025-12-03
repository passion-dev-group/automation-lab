from dotenv import dotenv_values, load_dotenv

config = dotenv_values(".env")

clickup_api_key = config.get("CLICKUP_API", "")

print(clickup_api_key)