from fastapi import FastAPI, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from contextlib import asynccontextmanager
from app.auth.canvas_auth import verify_token, test_canvas_connection, get_user_courses
from app.llm.openai_integration import generate_response, test_openai_connection
import time
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    if not test_canvas_connection():
        raise RuntimeError("Failed to connect to Canvas. Please check your .env file and network connection.")
    if not test_openai_connection():
        logger.warning("Failed to connect to OpenAI. The /ask endpoint may not work correctly.")
    yield

app = FastAPI(lifespan=lifespan)

# Mount the static directory
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root():
    return FileResponse("static/index.html")

@app.get("/user")
async def get_user():
    user_info = verify_token()
    return {"user": user_info["name"]}

@app.get("/courses")
async def courses():
    try:
        courses_data = get_user_courses()
        logger.info(f"Successfully retrieved {len(courses_data)} courses")
        return courses_data
    except HTTPException as he:
        logger.error(f"HTTP error in /courses: {he.detail}")
        raise he
    except Exception as e:
        logger.error(f"Unexpected error in /courses: {str(e)}")
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

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