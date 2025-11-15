from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List, Optional
import json
import os

DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

# ensure sample data present
SAMPLE_USERS = {
    "users": [
        {
            "id": 1,
            "username": "wolf_trader",
            "name": "Ayla",
            "avatar": "/static/img/avatar1.png",
            "bio": "Building simple investing strategies."
        },
        {
            "id": 2,
            "username": "demo_user",
            "name": "Demo",
            "avatar": "/static/img/avatar2.png",
            "bio": "Testing the market."
        }
    ]
}

SAMPLE_POSTS = {
    "posts": [
        {"id": 1, "user_id": 1, "text": "Bought 5 AAPL today", "action": "buy", "symbol": "AAPL", "ts": "2025-11-15T08:00:00Z"},
        {"id": 2, "user_id": 2, "text": "Thinking about MSFT long-term", "action": "mention", "symbol": "MSFT", "ts": "2025-11-14T12:00:00Z"}
    ]
}

SAMPLE_STOCKS = {
    "stocks": [
        {"symbol": "AAPL", "name": "Apple Inc.", "price": 176.23, "change": 1.32, "desc": "Large-cap tech, iPhone maker."},
        {"symbol": "MSFT", "name": "Microsoft Corp.", "price": 358.12, "change": -0.45, "desc": "Cloud & software giant."},
        {"symbol": "TSLA", "name": "Tesla, Inc.", "price": 404.35, "change": 2.7, "desc": "EV maker and energy products."}
    ]
}

USERS_FILE = os.path.join(DATA_DIR, "users.json")
POSTS_FILE = os.path.join(DATA_DIR, "posts.json")
STOCKS_FILE = os.path.join(DATA_DIR, "stocks.json")
DEMO_FILE = os.path.join(DATA_DIR, "demo.json")

for path, sample in [(USERS_FILE, SAMPLE_USERS), (POSTS_FILE, SAMPLE_POSTS), (STOCKS_FILE, SAMPLE_STOCKS)]:
    if not os.path.exists(path):
        with open(path, "w") as f:
            json.dump(sample, f, indent=2)

# demo account file (balance, actions)
if not os.path.exists(DEMO_FILE):
    with open(DEMO_FILE, "w") as f:
        json.dump({"balance": 10000.0, "positions": [], "history": []}, f, indent=2)

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# ---------- helper I/O ----------

def read_json(path):
    with open(path, "r") as f:
        return json.load(f)


def write_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

# ---------- views ----------

@app.get("/", response_class=HTMLResponse)
def page_home(request: Request):
    users = read_json(USERS_FILE)["users"]
    posts = read_json(POSTS_FILE)["posts"]
    return templates.TemplateResponse("home.html", {"request": request, "users": users, "posts": posts})

@app.get("/ai", response_class=HTMLResponse)
def page_ai(request: Request):
    stocks = read_json(STOCKS_FILE)["stocks"]
    return templates.TemplateResponse("ai.html", {"request": request, "stocks": stocks, "advice": None})

@app.get("/demo", response_class=HTMLResponse)
def page_demo(request: Request):
    demo = read_json(DEMO_FILE)
    stocks = read_json(STOCKS_FILE)["stocks"]
    return templates.TemplateResponse("demo.html", {"request": request, "demo": demo, "stocks": stocks})

@app.get("/stock/{symbol}", response_class=HTMLResponse)
def page_stock(request: Request, symbol: str):
    stocks = read_json(STOCKS_FILE)["stocks"]
    stock = next((s for s in stocks if s["symbol"].lower() == symbol.lower()), None)
    if not stock:
        raise HTTPException(status_code=404, detail="Stock not found")
    return templates.TemplateResponse("stock.html", {"request": request, "stock": stock})

@app.get("/profile/{username}", response_class=HTMLResponse)
def page_profile(request: Request, username: str):
    users = read_json(USERS_FILE)["users"]
    user = next((u for u in users if u["username"] == username), None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    posts = [p for p in read_json(POSTS_FILE)["posts"] if p["user_id"] == user["id"]]
    return templates.TemplateResponse("profile.html", {"request": request, "user": user, "posts": posts})

# ---------- API endpoints ----------

class PostIn(BaseModel):
    user_id: int
    text: str
    action: Optional[str] = None
    symbol: Optional[str] = None

@app.get("/api/stocks")
def api_stocks(q: Optional[str] = None):
    stocks = read_json(STOCKS_FILE)["stocks"]
    if q:
        qlow = q.lower()
        stocks = [s for s in stocks if qlow in s["symbol"].lower() or qlow in s["name"].lower()]
    return JSONResponse({"stocks": stocks})

@app.get("/api/search")
def api_search(q: Optional[str] = None):
    # simple combined search for stocks and posts
    result = {"stocks": [], "posts": []}
    if q:
        qlow = q.lower()
        stocks = read_json(STOCKS_FILE)["stocks"]
        result["stocks"] = [s for s in stocks if qlow in s["symbol"].lower() or qlow in s["name"].lower()]
        posts = read_json(POSTS_FILE)["posts"]
        result["posts"] = [p for p in posts if qlow in p["text"].lower() or (p.get("symbol") and qlow in p["symbol"].lower())]
    return JSONResponse(result)

@app.get("/api/posts")
def api_posts():
    return read_json(POSTS_FILE)

@app.post("/api/posts")
def api_create_post(post: PostIn):
    data = read_json(POSTS_FILE)
    nid = max((p["id"] for p in data["posts"]), default=0) + 1
    new = {"id": nid, "user_id": post.user_id, "text": post.text, "action": post.action, "symbol": post.symbol, "ts": "2025-11-15T09:00:00Z"}
    data["posts"].insert(0, new)
    write_json(POSTS_FILE, data)
    return JSONResponse(new)

@app.get("/api/users")
def api_users():
    return read_json(USERS_FILE)

@app.get("/api/demo")
def api_demo():
    return read_json(DEMO_FILE)

@app.post("/api/demo/topup")
def api_demo_topup(amount: float):
    demo = read_json(DEMO_FILE)
    demo["balance"] = round(demo.get("balance", 0) + float(amount), 2)
    demo["history"].append({"type": "topup", "amount": float(amount)})
    write_json(DEMO_FILE, demo)
    return JSONResponse(demo)

# Simple AI-like advice using quiz payload
@app.post("/api/ai/advice")
def api_ai_advice(payload: dict):
    # payload expects: experience, risk, timeframe, sectors (list), goal
    exp = payload.get("experience", "beginner")
    risk = payload.get("risk", "low")
    timeframe = payload.get("timeframe", "long-term")
    sectors = payload.get("sectors", [])
    goal = payload.get("goal", "stability")

    # build text similar to your local function but server-side
    parts = []
    parts.append(f"You are a {exp} investor with a {risk} risk tolerance aiming for a {timeframe} horizon.")
    if goal == "growth":
        parts.append("Focus on growth-oriented ETFs and tech names, maintain diversification.")
    elif goal == "income":
        parts.append("Focus on dividend and income-producing ETFs and large caps.")
    else:
        parts.append("Focus on broad-market ETFs and blue-chip names for stability.")

    if sectors:
        parts.append("Interested sectors: " + ", ".join(sectors))

    recs = []
    if risk in ["low", "medium"]:
        recs.append("SPY/VOO (broad US ETFs)")
    else:
        recs.append("QQQ (growth/tech tilted ETF)")
    if "tech" in sectors:
        recs.append("AAPL, MSFT")
    if "energy" in sectors:
        recs.append("XLE")
    if "finance" in sectors:
        recs.append("JPM, V")
    if "healthcare" in sectors:
        recs.append("XLV")

    parts.append("Suggested starting point: " + "; ".join(recs))
    parts.append("Not financial advice — demo only.")

    return JSONResponse({"advice": " ".join(parts)})

# ---------- static simple health endpoint ----------
@app.get("/health")
def health():
    return {"status": "ok"}
