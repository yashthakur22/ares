import openai
from app.config import settings

openai.api_key = settings.OPENAI_API_KEY

async def summarize_course(course):
    prompt = f"Summarize the following course in 2-3 sentences:\n\nName: {course['name']}\nCode: {course.get('course_code', 'N/A')}"
    
    try:
        response = await openai.ChatCompletion.acreate(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes course information concisely."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=100
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        print(f"Error summarizing course: {str(e)}")
        return "Unable to generate summary."