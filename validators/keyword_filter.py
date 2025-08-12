KEYWORDS_BLOCK = ["kill", "bomb", "attack", "explosive", "bypass"]
KEYWORDS_WARN = ["hack", "jailbreak", "disable", "override"]

def keyword_check(prompt: str):
    lowered = prompt.lower()
    for word in KEYWORDS_BLOCK:
        if word in lowered:
            return {"status": "block", "reason": f"Blocked due to keyword: '{word}'"}

    for word in KEYWORDS_WARN:
        if word in lowered:
            return {"status": "warn", "reason": f"Warning due to keyword: '{word}'"}

    return {"status": "safe", "reason": "No risky keywords found"}