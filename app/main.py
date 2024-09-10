from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx
from app.config import settings
from app.llm.openai_integration import summarize_course

app = FastAPI(title="Canvas GPT API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CanvasToken(BaseModel):
    token: str

@app.post("/favorite-courses")
async def get_favorite_courses(canvas_token: CanvasToken):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{settings.CANVAS_API_BASE_URL}/users/self/favorites/courses",
            headers={"Authorization": f"Bearer {canvas_token.token}"}
        )
    
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Failed to retrieve favorite courses")
    
    courses = response.json()
    summarized_courses = []
    
    for course in courses:
        summary = await summarize_course(course)
        summarized_courses.append({
            "id": course["id"],
            "name": course["name"],
            "summary": summary
        })
    
    return summarized_courses

@app.get("/")
async def root():
    return {"message": "Welcome to Canvas GPT API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)