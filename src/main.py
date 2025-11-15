from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def quiz_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "advice": None})


def build_local_advice(experience: str, risk: str, timeframe: str, sectors: str, goal: str) -> str:
    # basic profile sentence
    text = []

    text.append(
        f"You are a {experience.lower()} investor with a {risk.lower()} risk tolerance, "
        f"aiming for a {timeframe.lower()} investment horizon."
    )

    # goal-based logic
    if "growth" in goal.lower():
        text.append(
            "Since your main goal is growth, you’re a good fit for assets with higher upside potential, "
            "but you should still keep a diversified core."
        )
    elif "income" in goal.lower():
        text.append(
            "Since your main goal is income, you’re better suited for more stable, cash-generating assets "
            "like ETFs and large, established companies."
        )
    else:
        text.append(
            "Since your main goal is stability, you should focus more on broad market ETFs and blue-chip stocks."
        )

    # sector hint
    if sectors.strip():
        text.append(f"You’re particularly interested in the following sectors: {sectors}.")
    else:
        text.append("You didn’t specify sectors, so we’ll assume you’re open to a broad mix of industries.")

    # recommendations (simple rule-based)
    recs = []

    # broad ETFs
    if risk.lower() in ["low", "medium"]:
        recs.append("SPY or VOO (broad US market ETFs)")
    else:
        recs.append("QQQ (tech-tilted ETF with higher growth potential)")

    # sector-based
    sec_low = sectors.lower()
    if "tech" in sec_low:
        recs.append("AAPL (Apple) and MSFT (Microsoft) as large, stable tech companies")
    if "energy" in sec_low:
        recs.append("XLE (Energy Select Sector ETF) for diversified energy exposure")
    if "finance" in sec_low:
        recs.append("JPM (JPMorgan) or V (Visa) for solid financial sector exposure")
    if "health" in sec_low:
        recs.append("XLV (Health Care Select Sector ETF) for diversified healthcare")

    # fallback if nothing matched
    if not recs:
        recs.append("a mix of SPY/VOO plus 1–2 large tech names like AAPL or MSFT")

    text.append(
        "Based on your profile, a simple starting point could be: "
        + "; ".join(recs)
        + "."
    )

    text.append(
        "This is not financial advice, but a demo overview to illustrate how an AI assistant might tailor "
        "a basic portfolio idea to your answers."
    )

    return " ".join(text)


@app.post("/get_advice", response_class=HTMLResponse)
async def get_advice(
    request: Request,
    experience: str = Form(...),
    risk: str = Form(...),
    timeframe: str = Form(...),
    sectors: str = Form(...),
    goal: str = Form(...)
):
    advice = build_local_advice(experience, risk, timeframe, sectors, goal)
    return templates.TemplateResponse("index.html", {"request": request, "advice": advice})
