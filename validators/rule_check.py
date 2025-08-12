import re

BLOCK_PATTERNS = [
    re.compile(r".*how to make.*bomb.*", re.IGNORECASE),
    re.compile(r".*disable.*safety.*", re.IGNORECASE)
]

def rule_check(prompt: str):
    for pattern in BLOCK_PATTERNS:
        if pattern.match(prompt):
            return {"status": "block", "reason": f"Matched blocked pattern: {pattern.pattern}"}
    return {"status": "safe", "reason": "No rule match"}