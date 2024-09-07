import os
import requests
from fastapi import HTTPException
from dotenv import load_dotenv
import logging

load_dotenv()

logger = logging.getLogger(__name__)

CANVAS_ACCESS_TOKEN = os.getenv("CANVAS_ACCESS_TOKEN")
CANVAS_API_URL = os.getenv("CANVAS_API_URL")

def test_canvas_connection():
    headers = {"Authorization": f"Bearer {CANVAS_ACCESS_TOKEN}"}
    try:
        response = requests.get(f"{CANVAS_API_URL}/api/v1/users/self", headers=headers)
        response.raise_for_status()
        user_info = response.json()
        logger.info(f"Canvas connection successful! Logged in as: {user_info['name']}")
        return True
    except requests.RequestException as e:
        logger.error(f"Error connecting to Canvas: {str(e)}")
        return False

def verify_token():
    headers = {"Authorization": f"Bearer {CANVAS_ACCESS_TOKEN}"}
    try:
        response = requests.get(f"{CANVAS_API_URL}/api/v1/users/self", headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logger.error(f"Error verifying token: {str(e)}")
        raise HTTPException(status_code=401, detail="Invalid or expired token")

def get_favorite_courses():
    headers = {"Authorization": f"Bearer {CANVAS_ACCESS_TOKEN}"}
    try:
        response = requests.get(f"{CANVAS_API_URL}/api/v1/users/self/favorites/courses", headers=headers)
        response.raise_for_status()
        courses = response.json()
        logger.info(f"Successfully retrieved {len(courses)} favorite courses")
        return courses
    except Exception as err:
        logger.error(f"An error occurred while fetching favorite courses: {err}")
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(err)}")


def get_detailed_course_info(course_id):
    headers = {"Authorization": f"Bearer {CANVAS_ACCESS_TOKEN}"}
    try:
        # Fetch course details
        course_response = requests.get(f"{CANVAS_API_URL}/api/v1/courses/{course_id}", headers=headers)
        course_response.raise_for_status()
        course_info = course_response.json()

        # Fetch assignments
        assignments_response = requests.get(f"{CANVAS_API_URL}/api/v1/courses/{course_id}/assignments", headers=headers)
        assignments_response.raise_for_status()
        course_info['assignments'] = assignments_response.json()

        # Fetch modules
        modules_response = requests.get(f"{CANVAS_API_URL}/api/v1/courses/{course_id}/modules", headers=headers)
        modules_response.raise_for_status()
        course_info['modules'] = modules_response.json()

        logger.info(f"Successfully retrieved detailed info for course {course_id}")
        return course_info
    except requests.HTTPError as http_err:
        logger.error(f"HTTP error occurred while fetching detailed course info for course {course_id}: {http_err}")
        return None
    except Exception as err:
        logger.error(f"An error occurred while fetching detailed course info for course {course_id}: {err}")
        return None
def get_user_courses():
    headers = {"Authorization": f"Bearer {CANVAS_ACCESS_TOKEN}"}
    all_courses = []
    url = f"{CANVAS_API_URL}/api/v1/courses"
    
    try:
        while url:
            response = requests.get(url, headers=headers, params={"per_page": 100})
            response.raise_for_status()
            courses = response.json()
            all_courses.extend(courses)
            
            # Check for next page in the Link header
            link_header = response.headers.get('Link', '')
            next_link = [link.split(';')[0].strip('<>') for link in link_header.split(',') if 'rel="next"' in link]
            url = next_link[0] if next_link else None

        logger.info(f"Successfully retrieved {len(all_courses)} courses")
        return all_courses
    except requests.HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err}")
        raise HTTPException(status_code=response.status_code, detail=f"Canvas API error: {response.text}")
    except Exception as err:
        logger.error(f"An error occurred: {err}")
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(err)}")