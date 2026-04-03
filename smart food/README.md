# 🥗 Smart Budget Meal Optimization - OpenEnv Environment

This environment simulates a real-world decision-making scenario where an AI agent must manage daily food choices under multiple constraints: **Hunger**, **Budget**, and **Health**.

The goal is to optimize meal selection such that hunger is minimized while health is maximized and the budget is used efficiently.

---

## 🌍 Real-World Motivation
In everyday life, people constantly balance the need to eat affordable meals, maintain their health, and manage limited budgets. This environment provides a practical platform for training agents in:
- Personal diet and budget planning.
- Health-aware resource management.
- Multi-objective optimization.

---

## 🧱 Environment Specification

### 📊 Observation Space (Pydantic Model)
- **hunger**: `int` (0–10, lower is better - 0 is the goal).
- **budget**: `int` (0–100, higher is better).
- **health**: `int` (0–10, higher is better).

### 🎮 Action Space
Choose a meal each step:
- `"burger"` 🍔 (Hunger -3, Budget -30, Health -1)
- `"salad"` 🥗 (Hunger -2, Budget -20, Health +2)
- `"rice"` 🍚 (Hunger -4, Budget -15, Health +1)

### 🎯 Reward Function
The reward signal provides incremental progress feedback:
`reward = (10 - hunger) * 0.5 + health * 0.3 + budget * 0.1`

- If **episode terminated** (e.g., Hunger=0 reached), additional terminal adjustments apply.
- If **episode failed** (e.g., Health=0 or Budget=0), a `-5` penalty is applied.

---

## 🛑 Episode Termination
The episode ends when:
1.  **hunger == 0** (Goal reached ✅)
2.  **budget == 0** (Out of money ❌)
3.  **health == 0** (Bad health decisions ❌)

---

## 🧪 Tasks & Graders
1. **Task 1: Easy (Hunger Reduction)**
   - Focus: Reducing hunger efficiently. Score: 0–10.
2. **Task 2: Medium (Balance Hunger + Health)**
   - Focus: Minimizing hunger without sacrificing health. Score: 0–10.
3. **Task 3: Hard (Full Constraint Optimization)**
   - Focus: Optimal long-term health, hunger, and budget balance. Score: 0–10.

---

## 🛠 Setup & Usage

### ⚙ Installation
```bash
pip install -r requirements.txt
```

### 🐳 Docker Deployment
```bash
docker build -t meal-optimization-env .
docker run -p 8000:8000 meal-optimization-env
```

### 🤖 Run Baseline Agent
Ensure `OPENAI_API_KEY` is set:
```bash
python inference.py
```

---

## 📉 Example Output
```
[START]
Step 1: {'hunger': 8, 'budget': 70, 'health': 9, 'reward': 1.2, 'done': False}
Step 2: ...

--- FINAL SCORING ---
Episode Score → Easy: 7.0, Medium: 8.2, Hard: 6.5
Final Episode Score: 7.23
```
