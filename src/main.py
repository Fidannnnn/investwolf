from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import openai
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

openai.api_key = os.getenv("OPENAI_API_KEY")

@app.get("/", response_class=HTMLResponse)
def quiz_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "advice": None})

@app.post("/get_advice", response_class=HTMLResponse)
async def get_advice(
    request: Request,
    experience: str = Form(...),
    risk: str = Form(...),
    timeframe: str = Form(...),
    sectors: str = Form(...),
    goal: str = Form(...)
):
    prompt = f"""
    User Profile:
    Experience: {experience}
    Risk tolerance: {risk}
    Timeframe: {timeframe}
    Interested sectors: {sectors}
    Goal: {goal}

    Provide a simple, beginner-friendly investment overview and suggestions.
    """
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=400
    )
    advice = response.choices[0].message.content
    return templates.TemplateResponse("index.html", {"request": request, "advice": advice})
