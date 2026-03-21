# HIPAA Compliance Guide — Healthcare Data Protection
**Effective: January 1, 2026 | Classification: Confidential | Owner: Privacy Officer**

## 1. Protected Health Information (PHI)
PHI includes ANY individually identifiable health information: patient names, SSN, medical records, diagnosis, treatment, billing, lab results, imaging reports.

## 2. Privacy Rule
- Minimum Necessary Standard: Access only minimum PHI needed for job function
- Authorization required for uses beyond Treatment, Payment, Operations (TPO)
- De-identification: Safe Harbor method (remove 18 identifiers)

## 3. Security Rule — Technical Safeguards
- Access Control: Unique user IDs, emergency access, automatic logoff, encryption
- Audit Controls: Record all access to ePHI
- Transmission Security: TLS 1.2 minimum for ePHI in transit
- Storage Encryption: AES-256 for all ePHI at rest

## 4. Breach Notification
- Individual notice: Written within 60 days of discovery
- HHS notice: Within 60 days for 500+ individuals affected
- Media notice: Required for 500+ in single state

## 5. Penalties
| Tier | Description | Per Violation | Annual Cap |
|------|-------------|---------------|------------|
| 1 | Did not know | $100-$50,000 | $25,000 |
| 2 | Reasonable cause | $1,000-$50,000 | $100,000 |
| 3 | Willful neglect, corrected | $10,000-$50,000 | $250,000 |
| 4 | Willful neglect, uncorrected | $50,000+ | $1,500,000 |

## 6. System Requirements
- Multi-factor authentication for PHI access
- Session timeout: 15 minutes inactivity
- Terminated employee access disabled within 4 hours
- Quarterly access reviews by department managers

## 7. Business Associates
- BAA required before sharing any PHI
- Report breaches within 24 hours
- Return/destroy all PHI on contract termination
