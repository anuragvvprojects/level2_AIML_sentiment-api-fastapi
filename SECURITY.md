# Security Policy

## Reporting a Vulnerability
Report suspected vulnerabilities privately to **security@example.com** with
steps to reproduce, logs (redacted), and impact. Do **not** open a public issue.

## Scope
- API endpoints and model inference logic
- Container and deployment artifacts
- Dependency stack and configuration

## Hardening Summary
- Input validation & payload size limits
- Structured logging without PII
- Rate limiting (gateway) & auth (optional)
- Dependency scanning (Dependabot), image scanning (Trivy)
- Readiness/liveness probes and rolling deploys
