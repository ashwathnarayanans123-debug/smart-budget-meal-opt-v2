def grade_easy(final_state):
    # Success: Score based on hunger reduction (0–10 scale)
    hunger = final_state.get("hunger", 10)
    return float(max(0, 10 - hunger))

def grade_medium(final_state):
    # Success: Balance hunger + health (0–10 scale)
    hunger = final_state.get("hunger", 10)
    health = final_state.get("health", 0)
    hunger_score = max(0, 10 - hunger)
    return float((hunger_score + health) / 2)

def grade_hard(final_state):
    # Success: Optimize hunger + health + budget (0–10 scale)
    hunger = final_state.get("hunger", 10)
    health = final_state.get("health", 0)
    budget = final_state.get("budget", 0)
    
    hunger_score = max(0, 10 - hunger)
    budget_score = budget / 10 # 0–100 -> 0–10
    
    return float((hunger_score + health + budget_score) / 3)