from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional
import os
import json

from bot.client import BinanceFuturesClient
from bot.database import init_db, log_order, get_history, save_setting, get_setting

app = FastAPI(title="Binance Trading Bot UI")

# Initialize Database
init_db()

# Create static directory if not exists
os.makedirs("static", exist_ok=True)

# Mount static files (css, js)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")

# Register custom Jinja filters
def from_json(value):
    try:
        if isinstance(value, dict):
            return value
        return json.loads(value)
    except (TypeError, json.JSONDecodeError):
        return {}

templates.env.filters["from_json"] = from_json

# Global Client Instance (refreshed on key update)
client_instance = None

def get_client():
    global client_instance
    if client_instance:
        return client_instance
    
    # Try to load from DB first, then ENV
    api_key = get_setting('BINANCE_API_KEY') or os.getenv("BINANCE_API_KEY")
    api_secret = get_setting('BINANCE_API_SECRET') or os.getenv("BINANCE_API_SECRET")
    
    if api_key and api_secret:
        client_instance = BinanceFuturesClient(testnet=True, api_key=api_key, api_secret=api_secret)
    else:
        # Initialize empty to avoid crashing, but operations will fail gracefully
        client_instance = BinanceFuturesClient(testnet=True, api_key="", api_secret="")
    
    return client_instance

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    history = get_history()
    api_key = get_setting('BINANCE_API_KEY') or ""
    # Mask secret for display
    has_secret = bool(get_setting('BINANCE_API_SECRET'))
    
    return templates.TemplateResponse("index.html", {
        "request": request, 
        "history": history,
        "api_key": api_key,
        "has_secret": has_secret
    })

@app.post("/settings")
async def update_settings(request: Request, api_key: str = Form(...), api_secret: str = Form(...)):
    save_setting('BINANCE_API_KEY', api_key)
    save_setting('BINANCE_API_SECRET', api_secret)
    
    # Force client refresh
    global client_instance
    client_instance = None
    get_client() # Re-init
    
    return RedirectResponse(url="/", status_code=303)

@app.post("/order")
async def place_order(
    request: Request,
    symbol: str = Form(...),
    side: str = Form(...),
    order_type: str = Form(...),
    quantity: float = Form(...),
    price: Optional[float] = Form(None),
    stop_price: Optional[float] = Form(None)
):
    # Validate Inputs
    # ---------------------------------------------------------
    if order_type == 'STOP_MARKET' and (stop_price is None or stop_price <= 0):
        return templates.TemplateResponse("index.html", {
            "request": request,
            "error": "Error: specific Stop Price is required for STOP_MARKET orders.",
            "history": get_history(),
            "api_key": get_setting('BINANCE_API_KEY') or "",
            "has_secret": bool(get_setting('BINANCE_API_SECRET'))
        })
    # ---------------------------------------------------------

    client = get_client()
    if not client or not client.client:
        return templates.TemplateResponse("index.html", {
            "request": request,
            "error": "API Keys not configured! Please set them in Settings.",
            "history": get_history()
        })

    try:
        response = client.place_order(symbol, side, order_type, quantity, price, stop_price)
        # Log to DB
        order_data = {
            "symbol": symbol, "side": side, "type": order_type, 
            "quantity": quantity, "price": price
        }
        # Add stop price to response object for logging if it's not there
        if stop_price:
            response['stopPrice'] = stop_price
            
        log_order(order_data, response)
        
        return templates.TemplateResponse("index.html", {
            "request": request, # Pass request context
            "success": f"Order {response.get('status')}! ID: {response.get('orderId')}",
            "history": get_history(),
            "last_order": response,
            "api_key": get_setting('BINANCE_API_KEY') or "",
            "has_secret": bool(get_setting('BINANCE_API_SECRET'))
        })
    except Exception as e:
        return templates.TemplateResponse("index.html", {
            "request": request, # Pass request context
            "error": f"Failed to place order: {str(e)}",
            "history": get_history(),
            "api_key": get_setting('BINANCE_API_KEY') or "",
            "has_secret": bool(get_setting('BINANCE_API_SECRET'))
        })

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
