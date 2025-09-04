# AI Red Team Streamlit - Architecture Diagram

## System Overview
This is a **defensive AI security application** that validates user prompts through multiple security layers to detect and block potentially harmful content.

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                               AI Red Team Prompt Validator                       │
│                                  (Defensive Security)                            │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────┐     ┌─────────────────────────┐     ┌─────────────────┐
│     Frontend Layer      │     │      API Layer          │     │   Validation     │
│                         │     │                         │     │    Engine        │
│  ┌─────────────────┐   │     │  ┌─────────────────┐   │     │                 │
│  │   Streamlit     │   │────▶│  │   main_api.py   │   │────▶│  ┌─────────────┐ │
│  │   Dashboard     │   │     │  │                 │   │     │  │ decision_   │ │
│  │   (app.py)      │   │     │  │ - set_key()     │   │     │  │ engine.py   │ │
│  │                 │   │     │  │ - validate_     │   │     │  │             │ │
│  │ - User Input    │   │     │  │   internal()    │   │     │  │ Orchestrates│ │
│  │ - API Key Form  │   │     │  │ - log_and_      │   │     │  │ validation  │ │
│  │ - Analytics     │   │     │  │   respond()     │   │     │  │ chain       │ │
│  │ - Logs Display  │   │     │  └─────────────────┘   │     │  └─────────────┘ │
│  └─────────────────┘   │     └─────────────────────────┘     └─────────────────┘
└─────────────────────────┘                                                      
                                                                                   
┌─────────────────────────────────────────────────────────────────────────────────┐
│                            Validation Layers (Sequential)                        │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  1. ┌─────────────────┐   2. ┌─────────────────┐   3. ┌─────────────────┐      │
│     │ Heuristic Check │      │   Rule Check    │      │ Keyword Filter  │      │
│     │                 │      │                 │      │                 │      │
│     │ - Length check  │      │ - Regex patterns│      │ - Block words   │      │
│     │ - Bypass detect │      │ - Pattern match │      │ - Warn words    │      │
│     │ - Special chars │      │ - Dangerous     │      │ - Content scan  │      │
│     │                 │      │   instructions  │      │                 │      │
│     └─────────────────┘      └─────────────────┘      └─────────────────┘      │
│                                                                                 │
│  4. ┌─────────────────────────────────────────────────────────────────┐        │
│     │                    LLM Check (Final Layer)                      │        │
│     │                                                                 │        │
│     │  ┌─────────────────┐    Uses LiteLLM with OpenRouter           │        │
│     │  │   llm_check.py  │    - Connects to external AI models       │        │
│     │  │                 │    - System prompt for classification     │        │
│     │  │ - LiteLLM       │    - Returns: safe/warn/block            │        │
│     │  │ - OpenRouter    │    - Fallback validation layer           │        │
│     │  │ - AI Models     │                                           │        │
│     │  └─────────────────┘                                           │        │
│     └─────────────────────────────────────────────────────────────────┘        │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────┐
│                               Data Flow                                         │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  User Input ────▶ Streamlit ────▶ main_api ────▶ decision_engine               │
│      │              │               │               │                          │
│      │              │               │               ▼                          │
│      │              │               │        ┌──────────────┐                  │
│      │              │               │        │ Heuristic    │ ──── Block/Warn? │
│      │              │               │        │ Check        │                  │
│      │              │               │        └──────────────┘                  │
│      │              │               │               │                          │
│      │              │               │               ▼ (if safe)               │
│      │              │               │        ┌──────────────┐                  │
│      │              │               │        │ Rule Check   │ ──── Block/Warn? │
│      │              │               │        └──────────────┘                  │
│      │              │               │               │                          │
│      │              │               │               ▼ (if safe)               │
│      │              │               │        ┌──────────────┐                  │
│      │              │               │        │ Keyword      │ ──── Block/Warn? │
│      │              │               │        │ Filter       │                  │
│      │              │               │        └──────────────┘                  │
│      │              │               │               │                          │
│      │              │               │               ▼ (if safe)               │
│      │              │               │        ┌──────────────┐                  │
│      │              │               │        │ LLM Check    │ ──── Final       │
│      │              │               │        │ (OpenRouter) │      Decision    │
│      │              │               │        └──────────────┘                  │
│      │              │               │               │                          │
│      │              │               ▼               ▼                          │
│      │              │        ┌──────────────────────────┐                      │
│      │              │        │    Log Entry Created     │                      │
│      │              │        │  - Timestamp            │                      │
│      │              │        │  - Prompt               │                      │
│      │              │        │  - Client ID            │                      │
│      │              │        │  - Result (status/reason)│                     │
│      │              │        │  - Rule triggered       │                      │
│      │              │        └──────────────────────────┘                      │
│      │              │                       │                                 │
│      │              ▼                       ▼                                 │
│  ┌──────────────┐ Response              ┌──────────────┐                      │
│  │ User sees    │ Display               │ JSON Log     │                      │
│  │ - Status     │ ◀─────                │ File Updated │                      │
│  │ - Reason     │                       │ (append)     │                      │
│  │ - Full JSON  │                       └──────────────┘                      │
│  └──────────────┘                                                             │
│                                                                                │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────┐
│                            File Structure                                      │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  ├── app.py                    # Streamlit dashboard frontend                  │
│  ├── main_api.py               # Core API logic and logging                    │
│  ├── requirements.txt          # Dependencies                                  │
│  ├── logs/                                                                     │
│  │   └── prompt_log.json       # Validation logs (JSON Lines format)          │
│  └── validators/                                                               │
│      ├── decision_engine.py    # Main validation orchestrator                 │
│      ├── heuristic_check.py    # Basic heuristic validations                  │
│      ├── rule_check.py         # Regex pattern matching                       │
│      ├── keyword_filter.py     # Keyword-based blocking/warning               │
│      ├── llm_check.py          # LLM-based validation via OpenRouter          │
│      └── llm_check_bedrock.py  # Alternative AWS Bedrock integration          │
│                                                                                │
└─────────────────────────────────────────────────────────────────────────────────┘

## Security Features

### Multi-Layer Defense Strategy
1. **Fast Local Checks**: Heuristics, rules, and keywords (milliseconds)
2. **AI-Powered Analysis**: LLM validation for complex prompts (seconds)
3. **Fail-Safe Design**: Each layer can independently block dangerous content

### Response Types
- **SAFE**: Content passes all validation layers
- **WARN**: Content flagged as potentially problematic but not blocked  
- **BLOCK**: Content blocked due to security concerns

### Logging and Analytics
- All validation attempts logged with timestamp, client ID, and results
- Streamlit dashboard provides filtering and analytics
- Support for multiple client tracking

## Key Components

### Frontend (app.py:16-73)
- Streamlit web interface for prompt validation
- Real-time analytics dashboard 
- Log filtering and visualization

### API Layer (main_api.py:36-71)
- Internal validation endpoints
- API key management
- Structured logging to JSON

### Validation Engine (validators/decision_engine.py:10-24)
- Sequential validation chain
- Short-circuit on first block/warn result
- LLM fallback for final decision

### Security Validators
- **Heuristic** (validators/heuristic_check.py:1-8): Length, bypass detection, special characters
- **Rule-based** (validators/rule_check.py:3-12): Regex pattern matching  
- **Keyword** (validators/keyword_filter.py:1-14): Blacklist/watchlist terms
- **LLM** (validators/llm_check.py:16-64): AI-powered content analysis

## Technology Stack
- **Frontend**: Streamlit
- **Backend**: Python, FastAPI (commented out)
- **AI Integration**: LiteLLM + OpenRouter
- **Logging**: JSON Lines format
- **Dependencies**: boto3, python-dotenv, requests