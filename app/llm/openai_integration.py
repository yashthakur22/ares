import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def generate_response(prompt: str):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant for educational purposes."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150  # Adjust this as needed
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"An error occurred while generating the response: {str(e)}"

def test_openai_connection():
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Hello, are you working?"}],
            max_tokens=10
        )
        print("OpenAI connection successful!")
        return True
    except Exception as e:
        print(f"Error connecting to OpenAI: {str(e)}")
        return False