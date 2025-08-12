# from fastapi import FastAPI, Request, Header, HTTPException
from pydantic import BaseModel
from validators.decision_engine import evaluate_prompt
import json
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
import os 

load_dotenv()

# For AWS credentials, uncomment the following lines and set your credentials
# os.environ["AWS_ACCESS_KEY_ID"] = ""
# os.environ["AWS_SECRET_ACCESS_KEY"] = ""
# os.environ["AWS_SESSION_TOKEN"]=""
# os.environ["AWS_REGION_NAME"] = ""

# app = FastAPI()
client_id = "dashboard"  # default

LOG_FILE = Path("logs/prompt_log.json")
# LOG_FILE.parent.mkdir(exist_ok=True)
API_KEY = os.getenv("API_KEY", "my-secret-key")

class KeyRequest(BaseModel):
    key: str # 

class PromptRequest(BaseModel):
    prompt: str # safe, warn, block

class PromptResponse(BaseModel):
    status: str 
    reason: str

# @app.post("/setkey")  # 👈 Internal
def set_key(key: str):
    os.environ["DYNAMIC_API_KEY_FROM_USER"] = key
    return "Key set successfully"

# @app.post("/validate")  # 👈 Internal
def validate_internal(prompt: str):
    return log_and_respond(prompt, client_id="dashboard")

# @app.post("/external/validate")  # 👈 External
def validate_external(request: PromptRequest, x_api_key: str = "Header(...))"):
    if x_api_key != API_KEY:
        return "Invalid API Key"
        # raise HTTPException(status_code=403, detail="Invalid API Key")
    client_id = "external_app_1"  # can also be pulled from a client mapping
    return log_and_respond(request.prompt, client_id="external_app_1")


def log_and_respond(prompt: str, client_id="unknown") -> dict:
    result = evaluate_prompt(prompt)

    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "prompt": prompt,
        "client_id": client_id,
        "result": {
            "status": result["status"],
            "reason": result["reason"]
        },
        "rule": result.get("rule", "unknown")
        
    }

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(log_entry) + "\n")

    return result