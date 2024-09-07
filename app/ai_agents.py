from openai import OpenAI
from typing import List, Dict
import asyncio
import logging
import os

logger = logging.getLogger(__name__)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def summarize_course(course: Dict) -> Dict:
    try:
        assignments = course.get('assignments', [])
        modules = course.get('modules', [])
        
        prompt = f"""Summarize the following course in 3-4 sentences, highlighting key aspects of the coursework:

Name: {course['name']}
Code: {course.get('course_code', 'N/A')}
Description: {course.get('description', 'No description available.')}

Assignments: {', '.join([a['name'] for a in assignments[:5]])}  # List up to 5 assignments

Modules: {', '.join([m['name'] for m in modules[:5]])}  # List up to 5 modules

Focus on the course content, main topics covered, and types of assessments."""

        response = await asyncio.to_thread(
            client.chat.completions.create,
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes course information concisely and accurately."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=200
        )
        
        summary = response.choices[0].message.content.strip()
        
        logger.info(f"Successfully summarized course: {course['name']}")
        
        return {
            "id": course['id'],
            "name": course['name'],
            "code": course.get('course_code', 'N/A'),
            "summary": summary
        }
    except Exception as e:
        logger.error(f"Error summarizing course {course['name']}: {str(e)}")
        return {
            "id": course['id'],
            "name": course['name'],
            "code": course.get('course_code', 'N/A'),
            "summary": f"Error generating summary: {str(e)}"
        }

async def process_courses(courses: List[Dict]) -> List[Dict]:
    summarized_courses = []
    for course in courses:
        try:
            summarized_course = await summarize_course(course)
            summarized_courses.append(summarized_course)
        except Exception as e:
            logger.error(f"Error processing course {course.get('name', 'Unknown')}: {str(e)}")
            summarized_courses.append({
                "id": course.get('id', 'N/A'),
                "name": course.get('name', 'Unknown Course'),
                "code": course.get('course_code', 'N/A'),
                "summary": f"Error processing course: {str(e)}"
            })
    return summarized_courses