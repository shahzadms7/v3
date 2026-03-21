# Security Incident Response SOP
**Version: 2.0 | Effective: January 15, 2026 | Owner: CISO**

## 1. Severity Levels
| Level | Name | Response Time | Examples |
|-------|------|---------------|----------|
| SEV-1 | Critical | 15 minutes | Ransomware, active breach, mass data leak |
| SEV-2 | High | 1 hour | Unauthorized access, malware, phishing success |
| SEV-3 | Medium | 4 hours | Brute force attempts, policy violation |
| SEV-4 | Low | 24 hours | Vulnerability disclosed, audit finding |

## 2. Response Phases
1. **Detection** (0-15min): Report via security hotline ext.9911. Do NOT power off systems.
2. **Triage** (15-60min): SOC acknowledges, assigns severity, activates Incident Commander.
3. **Containment** (1-4h): Isolate systems, block IPs, disable compromised accounts.
4. **Eradication** (4-48h): Root cause, remove malware, patch vulnerabilities, reset credentials.
5. **Recovery** (1-7d): Restore from clean backups, staged system recovery, 72h monitoring.
6. **Post-Incident** (5 business days): Blameless post-mortem, lessons learned, update playbooks.

## 3. Regulatory Notification
| Regulation | Trigger | Deadline |
|-----------|---------|----------|
| GDPR | Personal data breach | 72 hours |
| HIPAA | PHI breach 500+ | 60 days |
| PCI-DSS | Cardholder data | Immediately |
| SOX | Material weakness | Next quarterly filing |

## 4. Evidence Handling
- Chain of custody documentation required
- Forensic images: bit-for-bit with SHA-256 hash
- Retention: Minimum 7 years
