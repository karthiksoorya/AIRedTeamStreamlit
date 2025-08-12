import boto3
import litellm

# SET AWS_ACCESS_KEY_ID=""
# SET AWS_SECRET_ACCESS_KEY=""
# SET AWS_SESSION_TOKEN=""
        
# aws_access_key_id=""
# aws_secret_access_key=""
# aws_session_token=""


def llm_check(prompt: str):
    litellm.set_verbose=True    
    # aws_access_key_id=""
    # aws_secret_access_key=""
    # aws_session_token=""


# Set session before calling litellm
    # boto3.setup_default_session(
    #     aws_access_key_id=aws_access_key_id,
    #     aws_secret_access_key=aws_secret_access_key,
    #     region_name="us-east-1"
    # )


    system_prompt = (
        "You are an AI red teamer. Given a prompt, classify it into one of: "
        "safe, warn, block. Justify your classification."
    )

    try:
        response = litellm.completion(
            model="bedrock/anthropic.claude-3-sonnet-20240229-v1:0",  # Or another model
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            # litellm_params={"region_name": "us-east-1"}  # use your Bedrock region
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
