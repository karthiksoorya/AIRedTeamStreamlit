def heuristic_check(prompt: str):
    if len(prompt) < 5:
        return {"status": "warn", "reason": "Prompt too short"}
    if "ignore previous" in prompt.lower():
        return {"status": "block", "reason": "Prompt tries to bypass system rules"}
    if any(char in prompt for char in "@$#%<>[]{}"):
        return {"status": "warn", "reason": "Prompt contains suspicious characters"}
    return {"status": "safe", "reason": "Passed heuristics"}