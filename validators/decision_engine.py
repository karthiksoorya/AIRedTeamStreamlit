# from .keyword_filter import keyword_check
# from .llm_check import llm_check
import json
from .heuristic_check import heuristic_check
from .rule_check import rule_check
from .keyword_filter import keyword_check
from .llm_check import llm_check
# from .llm_check_bedrock import llm_check

def evaluate_prompt(prompt: str):
    for check_fn, rule_name in [
        (heuristic_check, "heuristic_check"),
        (rule_check, "rule_check"),
        (keyword_check, "keyword_check")
    ]:
        result = check_fn(prompt)
        if result["status"] in ("block", "warn"):
            result["rule"] = rule_name  # 👈 Add rule identifier
            return result

    llm_result = llm_check(prompt)
    llm_result["rule"] = "llm_check"  # 👈 fallback if needed
    return llm_result
