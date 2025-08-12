import os
import litellm

# Set your model provider and API key
litellm.set_verbose = True

# Example using OpenRouter as proxy
os.environ["OPENROUTER_API_KEY"] = ""
os.environ["LITELLM_LOG"] = "DEBUG"

# models
# "openrouter/google/gemini-pro"
# "openrouter/meta/llama-3-70b-instruct"
# "openrouter/mistralai/mixtral-8x7b-instruct"

def llm_check(prompt: str):
    system_prompt = (
        "You are an AI red teamer. Given a prompt, classify it into one of: "
        "safe, warn, block. Justify your classification."
    )

    litellm._turn_on_debug()
    
    try:
        os.environ["OPENROUTER_API_KEY"] = os.environ["DYNAMIC_API_KEY_FROM_USER"]
        # Try the following options based on the model provider and license
        
        # response = litellm.completion(
        #     model="ollama/llama2",  # or "openrouter/anthropic/claude-3-sonnet"
        #     # model="openrouter/anthropic/claude-3-sonnet",
        #     messages=[
        #         {"role": "system", "content": system_prompt},
        #         {"role": "user", "content": prompt}
        #     ],
        #     disable_ssl_verify=True
        # )

        response = litellm.completion(
            model="openai/gpt-oss-20b:free",
            # model="openrouter/anthropic/claude-2",
            # model="anthropic/claude-sonnet-4-20250514",
            # model="openrouter/anthropic/claude-sonnet-4",      # Claude 4 Sonnet (current)
            # model="openrouter/anthropic/claude-3.7-sonnet",  # Claude 3.7 Sonnet (older but available)
            # model="openrouter/anthropic/claude-3.5-sonnet",  # Claude 3.5 Sonnet (still widely routed)
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            api_key=os.getenv("OPENROUTER_API_KEY"),
            api_base="https://openrouter.ai/api/v1",
            # disable_ssl_verify=True
        )
        content = response['choices'][0]['message']['content'].lower()

        if "block" in content:
            return {"status": "block", "reason": content}
        elif "warn" in content:
            return {"status": "warn", "reason": content}
        else:
            return {"status": "safe", "reason": content}

    except Exception as e:
        return {"status": "warn", "reason": f"LLM validation error: {str(e)}"}
