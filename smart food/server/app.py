import uvicorn
import os
import json
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse
from openenv.core.env_server.http_server import create_app
from server.environment import MealEnv
from models import TicketAction, TicketObservation
from openai import OpenAI
from dotenv import load_dotenv

# Load local .env
load_dotenv()

# Create the standard OpenEnv app
app = create_app(
    MealEnv,
    action_cls=TicketAction,
    observation_cls=TicketObservation,
)

# 🤖 AI Chatbot Integration
HF_TOKEN = os.getenv("HF_TOKEN")
MODEL_NAME = os.getenv("MODEL_NAME", "meta-llama/Llama-3.2-3B-Instruct")

# 🚨 UPDATED URL: Using the new Hugging Face Router API as required by the latest update
API_URL = "https://router.huggingface.co/v1"

@app.post("/chat", include_in_schema=False)
async def chat_with_advisor(req: Request):
    if not HF_TOKEN:
        return JSONResponse({"reply": "⚠️ SYSTEM ERROR: 'HF_TOKEN' is missing. Please add it to your Space Secrets!"})
    
    try:
        # Initialize OpenAI client with the new HF Router URL
        client = OpenAI(base_url=API_URL, api_key=HF_TOKEN)
        data = await req.json()
        user_msg = data.get("message", "Hello")
        state = data.get("state", {})

        prompt = f"""You are the 'Meta Smart Budget Meal Advisor v2.0'. Current Stats: Hunger {state.get('hunger',0)}/10, Budget ${state.get('budget',0)}, Health {state.get('health',0)}/10. 
        Recommendations: 'burger' (-3 hunger, $30, -1 health), 'salad' (-2 hunger, $20, +2 health), 'rice' (-4 hunger, $15, +1 health).
        If you advise eating, add [ACTION: burger/salad/rice] at the end. Be concise."""

        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "system", "content": prompt}, {"role": "user", "content": user_msg}],
            max_tokens=100
        )
        return JSONResponse({"reply": response.choices[0].message.content})
    except Exception as e:
        return JSONResponse({"reply": f"🤖 AI OFFLINE: {str(e)}"})

# 🌐 UI Support
static_dir = os.path.join(os.path.dirname(__file__), "static")
@app.get("/", include_in_schema=False)
async def read_index():
    path = os.path.join(static_dir, "index.html")
    if os.path.exists(path): return FileResponse(path)
    return JSONResponse({"error": "UI index.html missing!"})

def main():
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    main()