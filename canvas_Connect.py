import os
import requests
from dotenv import load_dotenv

load_dotenv()

CANVAS_ACCESS_TOKEN = os.getenv("CANVAS_ACCESS_TOKEN")
CANVAS_API_URL = os.getenv("CANVAS_API_URL")

def test_canvas_connection():
    if not CANVAS_ACCESS_TOKEN or not CANVAS_API_URL:
        print("Error: CANVAS_ACCESS_TOKEN or CANVAS_API_URL is missing in .env file")
        return False

    headers = {"Authorization": f"Bearer {CANVAS_ACCESS_TOKEN}"}
    try:
        # Test connection by fetching user info
        response = requests.get(f"{CANVAS_API_URL}/api/v1/users/self", headers=headers)
        
        if response.status_code == 200:
            user_info = response.json()
            print(f"Connection successful! Logged in as: {user_info['name']}")
            return True
        else:
            print(f"Error: Received status code {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except requests.RequestException as e:
        print(f"Error connecting to Canvas: {str(e)}")
        return False

if __name__ == "__main__":
    test_canvas_connection()