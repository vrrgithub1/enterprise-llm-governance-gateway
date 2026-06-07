from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from app.engines.pii_sanitizer import PIISanitizer
from app.engines.prompt_firewall import PromptFirewall
from app.engines.completion_auditor import CompletionAuditor  # New Engine Import
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
auditor_engine = CompletionAuditor()  # Initialize Gate C
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
        # ---- GATE A: INBOUND COMPLIANCE FILTER (PII REDACTION) ----
        sanitized_prompt, pii_telemetry = pii_engine.sanitize(payload.prompt)
        was_redacted = any(count > 0 for count in pii_telemetry.values())
        
        # ---- GATE B: INBOUND SECURITY FIREWALL ----
        is_security_violation, firewall_telemetry = firewall_engine.evaluate_payload(sanitized_prompt)
        
        # Immediate shortcut block if inbound firewall triggers
        if is_security_violation:
            governance_metadata = {
                "user_id": payload.user_id,
                "target_model": payload.target_model,
                "compliance_telemetry": pii_telemetry,
                "security_telemetry": firewall_telemetry,
                "outbound_auditor_telemetry": None,
                "policy_violation_intercepted": True
            }
            return {
                "status": "BLOCKED_BY_GOVERNANCE_GATEKEEPER",
                "message": "Security Violation: Inbound payload matched known adversarial injection patterns.",
                "governance_audit": governance_metadata,
                "llm_response": None
            }
        
        # ---- INFERENCE HANDSHAKE ----
        llm_response_payload = await llm_proxy.forward_inference(sanitized_prompt, payload.target_model)
        raw_completion_text = llm_response_payload["choices"][0]["message"]["content"]
        
        # ---- GATE C: OUTBOUND COMPLETION AUDITOR ----
        # Evaluate the text *returned* by the model before delivering it to the user
        is_outbound_violation, finalized_completion, auditor_telemetry = auditor_engine.audit_completion(raw_completion_text)
        
        # Master consolidated audit ledger metadata (NIST AI RMF Aligned)
        governance_metadata = {
            "user_id": payload.user_id,
            "target_model": payload.target_model,
            "compliance_telemetry": pii_telemetry,
            "security_telemetry": firewall_telemetry,
            "outbound_auditor_telemetry": auditor_telemetry,
            "policy_violation_intercepted": was_redacted or is_outbound_violation
        }
        
        return {
            "status": "cleared_for_user" if not governance_metadata["policy_violation_intercepted"] else "sanitized_with_policy_override",
            "governance_audit": governance_metadata,
            "llm_response": finalized_completion,
            "token_telemetry": llm_response_payload.get("usage", {})
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Governance Gateway processing error: {str(e)}"
        )