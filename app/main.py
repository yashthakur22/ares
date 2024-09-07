from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.auth.canvas_auth import verify_token, test_canvas_connection, get_favorite_courses, get_user_courses, get_detailed_course_info
from app.llm.openai_integration import generate_response, test_openai_connection
from app.ai_agents import process_courses
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    if not test_canvas_connection():
        logger.error("Failed to connect to Canvas.")
        raise RuntimeError("Failed to connect to Canvas. Please check your .env file and network connection.")
    if not test_openai_connection():
        logger.warning("Failed to connect to OpenAI. The /ask endpoint may not work correctly.")
    yield

app = FastAPI(lifespan=lifespan)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/user")
async def get_user():
    user_info = verify_token()
    return {"user": user_info["name"]}

@app.get("/courses")
async def courses(all_courses: bool = Query(False, description="Set to true to fetch all courses instead of just favorites")):
    try:
        if all_courses:
            logger.info("Fetching all courses from Canvas...")
            courses_data = get_user_courses()
        else:
            logger.info("Fetching favorite courses from Canvas...")
            courses_data = get_favorite_courses()
        
        logger.info(f"Successfully retrieved {len(courses_data)} courses from Canvas")
        
        detailed_courses = []
        for course in courses_data:
            detailed_course = get_detailed_course_info(course['id'])
            if detailed_course:
                detailed_courses.append(detailed_course)
            else:
                logger.warning(f"Could not fetch detailed info for course {course['id']}. Using basic info.")
                detailed_courses.append(course)
        
        logger.info("Processing and summarizing courses...")
        summarized_courses = await process_courses(detailed_courses)
        logger.info(f"Successfully processed and summarized {len(summarized_courses)} courses")
        
        return summarized_courses
    except Exception as e:
        logger.error(f"Unexpected error in /courses: {str(e)}")
        return {"error": f"An unexpected error occurred: {str(e)}"}

@app.get("/ask")
async def ask_gpt(prompt: str):
    try:
        user_info = verify_token()
        response = await generate_response(prompt)
        return {"user": user_info["name"], "prompt": prompt, "response": response}
    except Exception as e:
        logger.error(f"Error in /ask: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)