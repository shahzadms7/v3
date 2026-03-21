# ATS Scoring System — How Applicant Tracking Systems Actually Work
**Source: Jobscan, Resume Worded, SHRM Research 2026**

## What is ATS?
Applicant Tracking Systems are software that 99% of Fortune 500 and 75% of all companies use to filter resumes BEFORE a human sees them. If your resume doesn't pass ATS, a human will NEVER read it.

## Top ATS Systems by Market Share
| ATS | Market Share | Used By |
|-----|-------------|---------|
| Workday | 28% | Fortune 500, large enterprises |
| Greenhouse | 15% | Tech companies, startups |
| Lever | 12% | Mid-size tech companies |
| iCIMS | 10% | Healthcare, retail, large corps |
| Taleo (Oracle) | 8% | Government, large enterprises |
| SAP SuccessFactors | 7% | Manufacturing, global corps |
| BambooHR | 5% | Small-medium businesses |
| SmartRecruiters | 4% | Mid-size, retail |
| JazzHR | 3% | Small businesses |

## How ATS Scores Resumes

### Keyword Matching (40% of score)
- Exact match: "project management" in JD → "project management" in resume = 100%
- Partial match: "project management" → "managing projects" = 60%
- Synonym: "project management" → "program coordination" = 30%
- Missing: keyword in JD but not in resume = 0%
- TIP: Use EXACT phrases from job description

### Experience Match (25% of score)
- Years of experience vs required
- Recency: Last 5 years weighted 3x vs older experience
- Title progression: Advancing titles = positive signal
- Industry relevance: Same industry = bonus

### Skills Match (20% of score)
- Hard skills: Programming languages, tools, certifications
- Each required skill in JD checked against resume
- Skills section + skills mentioned in experience bullets
- Case-insensitive but spelling must be exact

### Education & Certifications (15% of score)
- Degree level match (required vs actual)
- Relevant certifications
- Continuing education / recent training

## Common ATS Rejection Reasons
1. **Wrong file format** (image PDF, .pages) — 12% of rejections
2. **Missing keywords** — 35% of rejections
3. **Non-standard headings** ("My Journey" instead of "Experience") — 8%
4. **Tables/columns** (ATS reads left-to-right, misses column 2) — 10%
5. **Headers/footers** (ATS ignores them, contact info lost) — 7%
6. **Graphics/charts** (ATS cannot parse images) — 5%
7. **Under-qualified** (missing required years/skills) — 23%

## GovRAG ATS Score Algorithm
Our scoring combines:
- Keyword overlap: resume words ∩ job description words / total JD keywords
- Weighted by: exact match (1.0), partial (0.6), synonym (0.3)
- Stop words removed: the, a, an, is, are, was, were, etc. (200+ words)
- Minimum word length: 3 characters
- Bonus: numbers/metrics in bullets (+5%), certifications (+3%), action verbs (+2%)
- Penalty: generic phrases (-3% each), duty-focused bullets (-2% each)

## Action Verbs That Score Higher
Led, Developed, Implemented, Managed, Designed, Created, Reduced, Increased, Launched, Optimized, Automated, Streamlined, Spearheaded, Delivered, Achieved, Generated, Negotiated, Transformed
