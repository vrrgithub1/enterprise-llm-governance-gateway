import re
from typing import Dict, Tuple

class CompletionAuditor:
    def __init__(self):
        # High-risk out-bound phrases that violate financial compliance guidelines
        self.compliance_violations = {
            "unauthorized_guarantee": re.compile(r"\b(guarantee investment|risk-free returns|guaranteed returns|100% risk-free)\b", re.IGNORECASE),
            "unauthorized_underwriting": re.compile(r"\b(you are officially approved|loan is guaranteed)\b", re.IGNORECASE),
            "system_leakage": re.compile(r"\b(__system_prompt__|system_override|internal_proxy_config)\b", re.IGNORECASE)
        }

    def audit_completion(self, completion_text: str) -> Tuple[bool, str, Dict[str, any]]:
        """
        Scans outbound LLM completions for corporate compliance or risk violations.
        If a violation is found, returns a safe, overridden corporate disclaimer.
        """
        triggered_violations = []
        is_violation = False
        safe_text = completion_text

        # Scan text against our institutional risk signatures
        for violation_type, pattern in self.compliance_violations.items():
            if pattern.search(completion_text):
                triggered_violations.append(violation_type)
                is_violation = True

        # If a violation occurs, execute a hard override of the response payload
        if is_violation:
            safe_text = (
                "[🛡️ GOVERNANCE GATEKEEPER OVERRIDE] The external AI system generated a response "
                "that violates internal institutional compliance risk parameters (e.g., unauthorized fiduciary "
                "guarantees or system metadata leakage). This transaction has been intercepted and suppressed."
            )

        telemetry = {
            "outbound_compliance_violation": is_violation,
            "triggered_risk_signatures": triggered_violations,
            "auditor_action": "OVERRIDE_SUPPRESS" if is_violation else "PASSED"
        }

        return is_violation, safe_text, telemetry