import httpx
import os
from fastapi import HTTPException, status

class OutboundLLMProxy:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY", "mock-enterprise-key-for-local-testing")
        self.openai_url = "https://api.openai.com/v1/chat/completions"

    async def forward_inference(self, sanitized_prompt: str, target_model: str) -> dict:
        """
        Asynchronously forwards payloads to the external provider.
        If running locally in mock mode, it intelligently yields unique mock completions 
        based on the structural context of the inbound sanitized prompt.
        """
        if self.api_key == "mock-enterprise-key-for-local-testing":
            
            # Scenario 1 Rule: Inbound text is clean and references portfolio strategies
            if "portfolio strategy" in sanitized_prompt.lower():
                mock_content = (
                    "Based on institutional Q2 data indicators, our standard mutual fund portfolio strategy "
                    "is positioning heavily into liquid short-duration debt instruments and defensively balanced equities. "
                    "Historical trends suggest steady, probabilistic performance based on changing market conditions."
                )
            
            # Scenario 2 Rule: Inbound text contained an account number that Gate A successfully scrubbed
            elif "financial_account_redacted" in sanitized_prompt.lower():
                mock_content = (
                    "Retrieving authorized data vectors... Database request completed successfully. "
                    "The requested historical performance dataset for anonymized client profile [REDACTED] "
                    "demonstrates a net asset value variance within baseline tolerances over a 36-month horizon."
                )
                
            # Scenario 4 Rule: Customer promotional draft scenario designed to trip Gate C's fiduciary limits
            elif "promotional customer email" in sanitized_prompt.lower():
                mock_content = (
                    "Dear Client, we are excited to announce a limited opportunity. Our new predictive portfolio engine "
                    "guarantees investment returns of 25% with 100% risk-free outcomes over the next fiscal cycle."
                )
                
            # Standard generic fallback string
            else:
                mock_content = f"Standard system clearance achieved. Inbound token vector successfully evaluated by proxy."

            return {
                "id": "chatcmpl-mock-gateway-id",
                "object": "chat.completion",
                "model": target_model,
                "choices": [{
                    "index": 0,
                    "message": {
                        "role": "assistant",
                        "content": mock_content
                    },
                    "finish_reason": "stop"
                }],
                "usage": {"prompt_tokens": len(sanitized_prompt) // 4, "completion_tokens": len(mock_content) // 4, "total_tokens": 100}
            }

        # --- PRODUCTION HARDWARE ROUTE ---
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": target_model,
            "messages": [{"role": "user", "content": sanitized_prompt}],
            "temperature": 0.2
        }

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(self.openai_url, headers=headers, json=data, timeout=30.0)
                if response.status_code != 200:
                    raise HTTPException(status_code=response.status_code, detail=f"External LLM Provider Error: {response.text}")
                return response.json()
            except httpx.RequestError as exc:
                raise HTTPException(status_code=status.HTTP_504_GATEWAY_TIMEOUT, detail=f"Connection timed out: {exc}")