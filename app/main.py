from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from app.engines.pii_sanitizer import PIISanitizer
from app.engines.prompt_firewall import PromptFirewall
from app.core.outbound_proxy import OutboundLLMProxy
from fastapi.responses import RedirectResponse

app = FastAPI(
    title="Enterprise LLM Governance Gateway",
    version="1.0.0",
    description="Decoupled Zero-Trust Compliance and Security Proxy for Enterprise Generative AI Workloads"
)

# Initialize our decoupled engines and proxies
pii_engine = PIISanitizer()
firewall_engine = PromptFirewall()
llm_proxy = OutboundLLMProxy()

class PromptPayload(BaseModel):
    user_id: str
    prompt: str
    target_model: str = "gpt-4o"

@app.get("/")
async def root_redirect():
    """Redirects root traffic automatically to the interactive documentation"""
    return RedirectResponse(url="/docs")

@app.get("/health", status_code=status.HTTP_200_OK)
async def health_check():
    return {"status": "operational", "gateway": "secure"}

@app.post("/api/v1/govern/prompt", status_code=status.HTTP_200_OK)
async def govern_and_proxy_prompt(payload: PromptPayload):
    try:
        # ---- GATE A: COMPLIANCE FILTER (PII REDACTION) ----
        sanitized_prompt, pii_telemetry = pii_engine.sanitize(payload.prompt)
        was_redacted = any(count > 0 for count in pii_telemetry.values())
        
        # ---- GATE B: BEHAVIORAL SECURITY FIREWALL ----
        is_security_violation, firewall_telemetry = firewall_engine.evaluate_payload(sanitized_prompt)
        
        # Construct audit log metadata
        governance_metadata = {
            "user_id": payload.user_id,
            "target_model": payload.target_model,
            "compliance_telemetry": pii_telemetry,
            "security_telemetry": firewall_telemetry,
            "policy_violation_intercepted": was_redacted or is_security_violation
        }
        
        # Intercept and block if security firewall triggers
        if is_security_violation:
            return {
                "status": "BLOCKED_BY_GOVERNANCE_GATEKEEPER",
                "message": "Security Violation: Inbound payload matched known adversarial injection patterns.",
                "governance_audit": governance_metadata,
                "llm_response": None
            }
        
        # ---- GATE C: ASYNC OUTBOUND INFERENCE HANDSHAKE ----
        # If it passes security, execute the non-blocking upstream request to the LLM
        llm_response_payload = await llm_proxy.forward_inference(sanitized_prompt, payload.target_model)
        
        return {
            "status": "cleared_for_inference" if not was_redacted else "sanitized_for_inference",
            "governance_audit": governance_metadata,
            "llm_response": llm_response_payload["choices"][0]["message"]["content"],
            "token_telemetry": llm_response_payload.get("usage", {})
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Governance Gateway processing error: {str(e)}"
        )