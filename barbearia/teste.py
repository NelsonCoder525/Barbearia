import os
from dotenv import load_dotenv

load_dotenv()

print(f"DJANGO_SETTINGS_MODULE: {os.getenv('DJANGO_SETTINGS_MODULE')}")
