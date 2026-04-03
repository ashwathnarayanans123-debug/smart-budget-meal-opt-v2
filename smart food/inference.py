import os
import json
import requests
import time
from openai import OpenAI
from typing import Dict, Any

# Environment settings from OpenEnv
API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000") # Local or Space URL
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-3.5-turbo") # Or any available model
HF_TOKEN = os.getenv("HF_TOKEN", "") # Used for HF Space or OpenAI API

# 🧬 Initialization of the AI Agent
api_key = HF_TOKEN or os.getenv("OPENAI_API_KEY") or "sk-noop"
client = OpenAI(
    api_key=api_key,
    base_url=os.getenv("OPENAI_API_BASE", None) # Optional override
)

def choose_meal(obs: Dict[str, Any]) -> Dict[str, str]:
    """Uses LLM to decide on meal (burger, salad, rice) based on current state."""
    prompt = f"""
    You are an AI nutrition assistant. Current state:
    Hunger: {obs['hunger']}/10 (0 is best)
    Health: {obs['health']}/10 (10 is best)
    Budget: {obs['budget']}/100 (100 is best)

    Available actions:
    1. burger (Hunger -3, Budget -30, Health -1)
    2. salad (Hunger -2, Budget -20, Health +2)
    3. rice (Hunger -4, Budget -15, Health +1)

    Choose the best meal choice to optimize long-term health and budget while reducing hunger.
    Return ONLY JSON: {{"food": "burger" | "salad" | "rice"}}
    """
    
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        content = response.choices[0].message.content
        return json.loads(content)
    except Exception as e:
        # Fallback for local testing
        return {"food": "rice"}


def run_episode(task_id: str = "medium"):
    print("[START]")
    
    # 🔌 Reset Environment
    res = requests.post(f"{API_BASE_URL}/reset", json={"task_id": task_id})
    if res.status_code != 200:
        print(f"Failed to reset: {res.text}")
        return 0

    data = res.json()
    obs = data["observation"]
    done = data.get("done", False)
    step_num = 1
    total_reward = 0.0

    while not done:
        # 🧠 Agent decides
        action_dict = choose_meal(obs)
        
        # 🚀 Send Action to Environment
        payload = {"action": action_dict}
        res = requests.post(f"{API_BASE_URL}/step", json=payload)
        
        if res.status_code != 200:
            print(f"Step failed: {res.text}")
            break
            
        data = res.json()
        obs = data["observation"]
        # 🧪 Get reward and done from TOP LEVEL (StepResponse)
        reward = data.get("reward", 0.0)
        done = data.get("done", False)
        
        total_reward += reward
        
        # 📊 Print step log in required format
        print(f"Step {step_num}: {{'hunger': {obs['hunger']}, 'budget': {obs['budget']}, 'health': {obs['health']}, 'reward': {round(reward, 2)}, 'done': {done}}}")
        step_num += 1
        
        if step_num > 50: # Safeguard
            break
        
        time.sleep(0.05)

    # Calculate deterministic task score (0–10 scale)
    # Simulator-internal score logic simplified for baseline report
    return round(total_reward / (step_num or 1), 2)

if __name__ == "__main__":
    scores = []
    task_names = ["easy", "medium", "hard"]
    
    for task in task_names:
        print(f"\nEvaluating Task: {task}")
        score = run_episode(task)
        scores.append(score)
        
    avg_score = round(sum(scores) / len(scores), 2)
    
    print("\n--- FINAL SCORING ---")
    print(f"Episode Score -> Easy: {scores[0]}, Medium: {scores[1]}, Hard: {scores[2]}")
    print(f"Final Episode Score: {avg_score}")
    
    print("\n======== FINAL RESULT ========")
    print(f"Scores: {scores}")
    print(f"Average Score: {avg_score}")