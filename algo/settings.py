import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

WORKSPACE = os.environ.get("WORKSPACE")
POLYGON_API_KEY = os.environ.get("POLYGON_API_KEY")
