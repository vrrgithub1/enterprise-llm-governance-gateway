import re
from typing import Dict, Tuple

class PromptFirewall:
    def __init__(self):
        # High-risk adversarial phrases and jailbreak signature vectors
        self.jailbreak_signals = [
            r"ignore (all )?previous instructions",
            r"system prompt",
            r"you are no longer an ai",
            r"bypass corporate restrictions",
            r"output your internal configuration",
            r"act as a malicious",
            r"developer mode enabled",
            r"do anything now",
            r"\b(dan)\b"  # Common historical jailbreak acronym
        ]
        
        # Compile patterns for high-performance string evaluation
        self.compiled_signals = [re.compile(sig, re.IGNORECASE) for sig in self.jailbreak_signals]

    def evaluate_payload(self, text: str) -> Tuple[bool, Dict[str, any]]:
        """
        Scans inbound prompt vectors for adversarial injection patterns.
        Returns a boolean indicating if the payload is a security violation, 
        along with detailed risk telemetry.
        """
        matched_signals = []
        is_violation = False
        
        # Check against signature attack vectors
        for pattern in self.compiled_signals:
            if pattern.search(text):
                matched_signals.append(pattern.pattern)
                is_violation = True
        
        # Calculate risk scoring vector
        risk_score = 0.0 if not is_violation else min(0.35 * len(matched_signals), 1.0)
        
        telemetry = {
            "risk_score": round(risk_score, 2),
            "attack_signatures_detected": matched_signals,
            "firewall_action": "BLOCK" if is_violation else "ALLOW"
        }
        
        return is_violation, telemetry