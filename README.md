# SOC 2 Cloud Control Mapping (AWS) — Demonstration

A self-contained, single-page demonstration mapping **SOC 2 Trust Services
Criteria (CC1–CC9)** to concrete **AWS** implementations, with evidence
artifacts and **automated evidence collection as code**:

- **TSC coverage** and a filterable, expandable **control matrix** — 14 controls
  with implementation details, configuration steps, and evidence for each.
- **Automated evidence collection & controls testing (code)** — the same checks
  in **Bash (AWS CLI)**, **Python (boto3)**, and **PowerShell**, plus **Athena
  SQL** log analytics over CloudTrail (root usage, access-denied patterns,
  non-MFA logins).
- **Evidence collection summary** — the artifact types an auditor receives in a
  SOC 2 Type II examination.

Criteria from the **AICPA Trust Services Criteria**; configurations follow the
**AWS Well-Architected Security Pillar**.

## 🔗 Live demo

**https://smittystuff.github.io/soc2-cloud-control-mapping-demo/**

## About

The environment, configurations, and evidence are **fictional** and included
only to demonstrate methodology and deliverables.

## Tech

A single `index.html` — no build step, no dependencies. All styling and
interactivity (TSC filter, expandable control rows, code tabs) are inline
vanilla HTML/CSS/JS, so it deploys anywhere static files are served.

## Run locally

```bash
python3 -m http.server 8080
# then visit http://localhost:8080
```

---

Part of the portfolio of Steven Smith — Information Security Consultant.
