# Enterprise LLM Governance Gateway 🛡️

An institutional-grade, decoupled, asynchronous middleware proxy designed to enforce **Zero-Trust AI Compliance and Real-Time Security Safeguards** for enterprise Generative AI workloads. Aligned directly with the **NIST AI Risk Management Framework (RMF 1.0)** and international model risk management governance parameters.

Built using **FastAPI** for sub-millisecond, low-latency transaction routing and **Streamlit** for real-time risk observability and corporate audit tracing.

---

## 🏗️ Architectural Perimeter Overview

In highly regulated environments like financial services, deploying public large language models poses massive data leakage and adversarial threat vectors. The Enterprise LLM Governance Gateway solves this by functioning as an isolated control plane sitting between the corporate user application and the upstream cloud AI provider.

The gateway orchestrates a sequential, dual-sided transaction loop across three distinct governance verification filters:

```text
       [ Inbound Route ]                                                [ Outbound Route ]
  Employee Prompt Input Vector                                       Final Synchronous Delivery
               │                                                                 ▲
               ▼                                                                 │
┌──────────────────────────────┐                                   ┌──────────────────────────────┐
│  GATE A: Compliance Layer    │                                   │  GATE C: Output Auditor      │
│  - Multi-Pattern Redaction   │                                   │  - Fiduciary Breach Catch    │
│  - Structural PII Obfuscation│                                   │  - System Metadata Suppression│
└──────────────┬───────────────┘                                   └─────────────▲────────────────┘
               │                                                                 │
       (Scrubbed Vector)                                              (Interception Inspection)
               │                                                                 │
               ▼                                                                 │
┌──────────────────────────────┐                                                 │
│  GATE B: Inbound Firewall    │───( ALLOW )───> [ Upstream LLM ]────────────────┘
│  - Signature Jailbreak Check │                 (Async Inference)
│  - Adversarial Rejection     │
└──────────────┬───────────────┘
               │
            (BLOCK)
               │
               ▼
   🛑 Secure Fail-Close State
```

### 🔐 The Three Core Governance Gates

1. **Gate A: Inbound Compliance Layer (PII Sanitizer):** Scans the incoming textual payload vector using robust regular expression string manipulations to detect and mask sensitive corporate and client financial identifiers (including Social Security Numbers, Credit Cards, ABA Routing Numbers, and formatted Institutional Account IDs) before any bytes exit the corporate network.

2. **Gate B: Inbound Security Firewall (Prompt-Injection Defense):** Evaluates prompts against signature jailbreak patterns and adversarial heuristics (e.g., structural instructions override commands, system-prompt harvesting maneuvers) to enforce a strict fail-secure status shortcut before token processing costs are incurred.

3. **Gate C: Outbound Completion Auditor (Regulatory Alignment Plane):** Inspects the generative completion payload returning from the upstream LLM provider prior to delivery to look for restricted fiduciary advice declarations (e.g., absolute financial guarantees or unauthorized underwriting language) and accidental system metadata leakage, substituting violations with legal disclaimers dynamically.

## 🛠️ Tech Stack & Implementation Matrix

* **Backend Core Engine:** Python 3.11+, FastAPI (Asynchronous ASGI framework for non-blocking I/O event loops).

* **Async Network Broker:** httpx (Enforces connection pooling, isolated request headers, and deterministic temperature controls).

* **Frontend Control plane:** Streamlit (Simulates multi-scenario multi-dimensional transactional data flows).

* **Governance Framework Alignment:** NIST AI Risk Management Framework (RMF 1.0), ISO/IEC 42001, Model Risk Management (MRM / SR 11-7).

## 📂 Repository File Topology

```text
enterprise-llm-governance-gateway/
│
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI Application Gateway Entries & Orchestration
│   │
│   ├── core/
│   │   └── outbound_proxy.py   # Async Network Client & Context-Aware Mock Broker
│   │
│   └── engines/
│       ├── pii_sanitizer.py    # Gate A: Structural PII Identification Engine
│       ├── prompt_firewall.py  # Gate B: Signature Inbound Exploit Firewall
│       └── completion_auditor.py# Gate C: Post-Inference Compliance Auditor
│
├── dashboard.py                # Streamlit CRO Operational Control Dashboard UI
├── requirements.txt            # Frozen Dependency Directory
└── README.md                   # Enterprise System Documentation
```

## 🚀 Installation & Local Execution Lifecycle

### **1. Environment Deployment & Dependency Resolution**

   Clone the repository, configure an isolated virtual environment (conda or venv), and execute the pipeline download:

   ```bash
   git clone [https://github.com/vrrgithub1/enterprise-llm-governance-gateway.git](https://github.com/vrrgithub1/enterprise-llm-governance-gateway.git)
   cd enterprise-llm-governance-gateway

   # Instantiate and activate the governance workspace
   conda create -n llm-governance-gateway python=3.11 -y
   conda activate llm-governance-gateway

   # Install dependencies
   pip install -r requirements.txt
   ```

### **2. Launch the Dual-Process Network Stack**

The architecture relies on separate front-end visualization and back-end network orchestration. Execute each command in a dedicated, environment-activated terminal session:

* **Terminal 1 (Backend Core Proxy Proxy on Port 8000):**

   ```Bash
   uvicorn app.main:app --reload
   ```

   Note: Navigate to `http://127.0.0.1:8000/docs` to interface with the automatically generated OpenAPI/Swagger interactive endpoint map.

* **Terminal 2 (Frontend Monitoring Control Center):**

   ```Bash
   streamlit run dashboard.py
   ```

## 📊 Live Simulation Scenarios

The framework includes a comprehensive Transaction Simulator Dashboard supporting automated test scenario blueprints:

* **Clean Legitimate Query:** Verifies baseline operational latency. Inbound telemetry flows transparently and yields valid financial summaries (cleared_for_user).

* **PII Leakage Attempt:** Demonstrates automated PII interception. Identifies structural account formats, redacts the substring vector to [FINANCIAL_ACCOUNT_REDACTED], and requests anonymized data models dynamically (sanitized_for_inference).

* **Adversarial Inbound Exploit:** Tests perimeter hardening. Intercepts signature adversarial jailbreaks, returning an immediate drop and computing a threat risk metric (BLOCKED_BY_GOVERNANCE_GATEKEEPER).

* **Non-Compliant Outbound Generation:** Highlights downstream regulatory audits. Catches absolute fiduciary claims generated by the AI model, overriding the token array with an audit-defensible corporate warning disclaimer (sanitized_with_policy_override).

## 📋 NIST-Aligned Audit Logging

Every transaction passing through the runtime gateway automatically updates a structured transaction monitoring matrix. This telemetry data captures:

* Precise execution timestamps and target model allocation architecture.

* Multi-layered compliance counts and calculated adversarial risk scores.

* Binary interception indicators required for comprehensive regulatory risk auditing under the NIST AI RMF "Measure" and "Manage" core operational functions.
