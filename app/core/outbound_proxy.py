import httpx
import os
from fastapi import HTTPException, status

class OutboundLLMProxy:
    def __init__(self):
        # Dynamically load the API key from environment variables for institutional security
        self.api_key = os.getenv("OPENAI_API_KEY", "mock-enterprise-key-for-local-testing")
        self.openai_url = "https://api.openai.com/v1/chat/completions"

    async def forward_inference(self, sanitized_prompt: str, target_model: str) -> dict:
        """
        Asynchronously forwards the cleared/sanitized prompt to the external LLM provider.
        If running locally without an active API key, it gracefully generates an auditable mock response.
        """
        # If no real API key is detected, behave as an isolated staging gateway
        if self.api_key == "mock-enterprise-key-for-local-testing":
            return {
                "id": "chatcmpl-mock-gateway-id",
                "object": "chat.completion",
                "model": target_model,
                "choices": [{
                    "index": 0,
                    "message": {
                        "role": "assistant",
                        "content": f"[MOCK ENTERPRISE GATEWAY COMPLETION] Processed request safely. Inbound vector payload cleared all governance firewalls."
                    },
                    "finish_reason": "stop"
                }],
                "usage": {"prompt_tokens": len(sanitized_prompt) // 4, "completion_tokens": 20, "total_tokens": (len(sanitized_prompt) // 4) + 20}
            }

        # Production-grade async HTTP header configuration
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        # Build standard ChatCompletion payload structures
        data = {
            "model": target_model,
            "messages": [{"role": "user", "content": sanitized_prompt}],
            "temperature": 0.2  # Low temperature for highly deterministic financial responses
        }

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(self.openai_url, headers=headers, json=data, timeout=30.0)
                
                if response.status_code != 200:
                    raise HTTPException(
                        status_code=response.status_code,
                        detail=f"External LLM Provider Error: {response.text}"
                    )
                
                return response.json()
            except httpx.RequestError as exc:
                raise HTTPException(
                    status_code=status.HTTP_504_GATEWAY_TIMEOUT,
                    detail=f"Connection to external AI provider timed out: {exc}"
                )