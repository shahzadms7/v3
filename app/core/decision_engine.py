"""
GovRAG V3 — DECISION ENGINE
The brain that decides. The mirror that shows naked truth.

This engine takes a person's ENTIRE profile and decides:
1. WHERE they stand globally (percentile ranking)
2. WHAT they're missing (hidden gaps they don't know)
3. WHERE they should go (country + industry + role match)
4. HOW to get there (exact steps, certifications, visa pathway)
5. WHAT they'll earn (salary reality, not fantasy)
6. WHEN they'll be ready (timeline based on gaps)

Rules are STRICT. No flattery. No hope without evidence.
If someone needs 2 years of training, we say 2 years.
If a visa is impossible, we say impossible.
If a career is dying, we say it's dying.

Built for 8 billion humans. East to West. Age 10 to 100.
"""

import re
from typing import Optional


# ══════════════════════════════════════════════════════════════════════════════
# EXPERIENCE LEVEL CLASSIFIER
# ══════════════════════════════════════════════════════════════════════════════
def classify_level(years: int) -> dict:
    """Classify candidate level with salary multiplier and expectations."""
    if years <= 0:
        return {"level": "Student/Fresh", "code": "L0", "multiplier": 0.5,
                "expectation": "Entry roles only. Internships. Need portfolio not experience."}
    elif years <= 2:
        return {"level": "Junior", "code": "L1", "multiplier": 0.7,
                "expectation": "Guided work. Learning on the job. 1-2 technical skills minimum."}
    elif years <= 5:
        return {"level": "Mid-Level", "code": "L2", "multiplier": 1.0,
                "expectation": "Independent contributor. Own projects end-to-end. 5+ skills."}
    elif years <= 8:
        return {"level": "Senior", "code": "L3", "multiplier": 1.3,
                "expectation": "Lead others. Architecture decisions. Mentoring. 10+ skills."}
    elif years <= 12:
        return {"level": "Staff/Lead", "code": "L4", "multiplier": 1.6,
                "expectation": "Cross-team impact. Strategy. Technical vision. Industry expertise."}
    elif years <= 20:
        return {"level": "Principal/Director", "code": "L5", "multiplier": 2.0,
                "expectation": "Organization-wide impact. Budget ownership. Executive communication."}
    else:
        return {"level": "Executive/C-Suite", "code": "L6", "multiplier": 2.5,
                "expectation": "Company-wide strategy. Board-level reporting. Industry thought leader."}


# ══════════════════════════════════════════════════════════════════════════════
# COUNTRY-ROLE FIT SCORER
# ══════════════════════════════════════════════════════════════════════════════
COUNTRY_INDUSTRY_DEMAND = {
    # Format: (country, industry) → demand_level 1-10
    ("CA", "IT"): 9, ("CA", "Healthcare"): 10, ("CA", "Finance"): 7, ("CA", "Engineering"): 8,
    ("US", "IT"): 10, ("US", "Healthcare"): 9, ("US", "Finance"): 9, ("US", "Engineering"): 8,
    ("GB", "IT"): 8, ("GB", "Healthcare"): 10, ("GB", "Finance"): 9, ("GB", "Legal"): 8,
    ("DE", "IT"): 9, ("DE", "Engineering"): 10, ("DE", "Healthcare"): 8, ("DE", "Manufacturing"): 9,
    ("AU", "IT"): 8, ("AU", "Healthcare"): 9, ("AU", "Mining"): 8, ("AU", "Construction"): 8,
    ("IN", "IT"): 10, ("IN", "Healthcare"): 7, ("IN", "Finance"): 6, ("IN", "Education"): 5,
    ("AE", "IT"): 8, ("AE", "Finance"): 9, ("AE", "Construction"): 8, ("AE", "Hospitality"): 7,
    ("SG", "IT"): 9, ("SG", "Finance"): 10, ("SG", "Logistics"): 8, ("SG", "Biotech"): 7,
    ("NZ", "IT"): 7, ("NZ", "Healthcare"): 9, ("NZ", "Agriculture"): 8, ("NZ", "Tourism"): 6,
    ("IE", "IT"): 9, ("IE", "Finance"): 8, ("IE", "Pharma"): 9, ("IE", "Healthcare"): 7,
    ("NL", "IT"): 8, ("NL", "Finance"): 8, ("NL", "Logistics"): 9, ("NL", "Agriculture"): 7,
    ("JP", "IT"): 8, ("JP", "Engineering"): 9, ("JP", "Healthcare"): 8, ("JP", "Manufacturing"): 7,
    ("KR", "IT"): 9, ("KR", "Engineering"): 8, ("KR", "Manufacturing"): 8, ("KR", "Entertainment"): 7,
    ("PK", "IT"): 7, ("PK", "Healthcare"): 5, ("PK", "Textile"): 6, ("PK", "Agriculture"): 5,
    ("NG", "IT"): 6, ("NG", "Finance"): 5, ("NG", "Oil"): 7, ("NG", "Agriculture"): 5,
    ("ZA", "IT"): 6, ("ZA", "Mining"): 8, ("ZA", "Finance"): 6, ("ZA", "Healthcare"): 7,
}


def country_fit_score(country_code: str, industry: str, skills: list, years: int) -> dict:
    """Score how well a candidate fits a specific country's job market."""
    key = (country_code.upper(), industry)
    demand = COUNTRY_INDUSTRY_DEMAND.get(key, 5)

    level = classify_level(years)

    # Visa difficulty
    easy_visa = {"CA", "AU", "NZ", "DE", "NL", "IE", "SG"}
    medium_visa = {"GB", "AE", "JP", "KR", "SE", "NO", "DK", "CH"}
    hard_visa = {"US", "CN", "RU"}

    if country_code.upper() in easy_visa:
        visa_score = 80
        visa_note = "Relatively accessible visa pathways for skilled workers"
    elif country_code.upper() in medium_visa:
        visa_score = 55
        visa_note = "Visa possible but competitive or employer-dependent"
    elif country_code.upper() in hard_visa:
        visa_score = 30
        visa_note = "Difficult visa process — lottery, quotas, or restrictions"
    else:
        visa_score = 50
        visa_note = "Check specific visa requirements"

    # Skills match (how relevant are their skills for this market)
    hot_skills_by_country = {
        "CA": {"python", "aws", "azure", "kubernetes", "react", "sql", "agile", "machine learning"},
        "US": {"python", "java", "aws", "azure", "kubernetes", "react", "machine learning", "ai"},
        "GB": {"python", "azure", "aws", "sql", "agile", "finance", "compliance"},
        "DE": {"python", "java", "kubernetes", "sap", "engineering", "manufacturing"},
        "AU": {"python", "aws", "azure", "react", "sql", "mining", "healthcare"},
        "AE": {"python", "azure", "finance", "construction", "hospitality", "sales"},
        "SG": {"python", "java", "finance", "compliance", "data science", "ai"},
        "IN": {"python", "java", "react", "sql", "aws", "machine learning"},
    }
    hot = hot_skills_by_country.get(country_code.upper(), set())
    skill_overlap = len(set(s.lower() for s in skills) & hot)
    skill_score = min(100, (skill_overlap / max(len(hot), 1)) * 100)

    composite = round((demand * 8 + visa_score * 0.3 + skill_score * 0.3) / 1.6)
    composite = min(100, max(0, composite))

    return {
        "country": country_code,
        "industry": industry,
        "demand_level": f"{demand}/10",
        "visa_difficulty": visa_score,
        "visa_note": visa_note,
        "skill_match": round(skill_score),
        "composite_fit": composite,
        "level": level,
        "verdict": "STRONG FIT" if composite > 70 else "POSSIBLE" if composite > 45 else "DIFFICULT",
    }


# ══════════════════════════════════════════════════════════════════════════════
# GAP ANALYSIS ENGINE — What's missing between YOU and the JOB
# ══════════════════════════════════════════════════════════════════════════════
def gap_analysis(candidate_skills: list, candidate_certs: list, candidate_years: int,
                 target_role: str = "", target_industry: str = "", target_country: str = "") -> dict:
    """Find every gap between where you are and where you want to be."""

    gaps = []
    recommendations = []
    timeline_months = 0

    candidate_skills_lower = set(s.lower() for s in candidate_skills)
    candidate_certs_lower = set(c.lower() for c in candidate_certs)

    # Industry-specific requirements
    industry_reqs = {
        "IT": {
            "must_have": {"python", "git", "sql", "linux", "agile"},
            "should_have": {"aws", "docker", "kubernetes", "cicd", "react"},
            "nice_to_have": {"machine learning", "terraform", "graphql", "typescript"},
            "certs": {"aws solutions architect", "azure administrator", "kubernetes"},
        },
        "Healthcare": {
            "must_have": {"patient care", "clinical", "hipaa", "ehr"},
            "should_have": {"nursing", "compliance", "data analysis"},
            "nice_to_have": {"telehealth", "ai", "health informatics"},
            "certs": {"nclex", "bls", "acls", "cpc"},
        },
        "Finance": {
            "must_have": {"excel", "sql", "accounting", "compliance"},
            "should_have": {"python", "power bi", "risk management", "audit"},
            "nice_to_have": {"machine learning", "blockchain", "esg"},
            "certs": {"cpa", "cfa", "frm", "acca"},
        },
        "Engineering": {
            "must_have": {"project management", "communication", "problem solving"},
            "should_have": {"python", "data analysis", "six sigma"},
            "nice_to_have": {"ai", "digital twin", "sustainability"},
            "certs": {"pmp", "prince2", "six sigma", "p.eng"},
        },
        "Marketing": {
            "must_have": {"social media", "content marketing", "seo", "analytics"},
            "should_have": {"python", "sql", "crm", "data analysis"},
            "nice_to_have": {"ai", "machine learning", "video production"},
            "certs": {"google analytics", "hubspot", "meta blueprint"},
        },
    }

    reqs = industry_reqs.get(target_industry, industry_reqs.get("IT", {}))

    # Check must-have skills
    must_missing = reqs.get("must_have", set()) - candidate_skills_lower
    if must_missing:
        for skill in must_missing:
            gaps.append({"type": "CRITICAL_SKILL", "item": skill, "severity": "HIGH",
                         "message": f"MISSING: {skill} is REQUIRED for {target_industry}. Without it, 80% rejection."})
            recommendations.append(f"Learn {skill} immediately — online course 2-4 weeks")
            timeline_months = max(timeline_months, 1)

    # Check should-have skills
    should_missing = reqs.get("should_have", set()) - candidate_skills_lower
    if should_missing:
        for skill in should_missing:
            gaps.append({"type": "IMPORTANT_SKILL", "item": skill, "severity": "MEDIUM",
                         "message": f"MISSING: {skill} is expected for competitive roles. Limits salary by 10-20%."})
            recommendations.append(f"Add {skill} to your toolkit — 1-2 months learning")
            timeline_months = max(timeline_months, 2)

    # Check certifications
    cert_reqs = reqs.get("certs", set())
    cert_missing = cert_reqs - candidate_certs_lower
    if cert_missing and len(candidate_certs) == 0:
        gaps.append({"type": "CERTIFICATION", "item": "None found", "severity": "HIGH",
                     "message": "ZERO certifications. Certified candidates earn 15% more. Get at least one."})
        timeline_months = max(timeline_months, 3)

    # Experience gaps
    level = classify_level(candidate_years)
    if candidate_years < 2 and target_role and "senior" in target_role.lower():
        gaps.append({"type": "EXPERIENCE", "item": f"{candidate_years} years", "severity": "CRITICAL",
                     "message": f"Only {candidate_years} years experience. Senior roles need 5+. Apply for mid-level instead."})

    # Readiness assessment
    critical_count = sum(1 for g in gaps if g["severity"] in ("HIGH", "CRITICAL"))
    if critical_count == 0:
        readiness = "READY — Apply now"
        readiness_score = 90
    elif critical_count <= 2:
        readiness = f"ALMOST READY — Fix {critical_count} critical gaps first ({timeline_months} months)"
        readiness_score = 65
    elif critical_count <= 5:
        readiness = f"NOT READY — {critical_count} critical gaps. Need {timeline_months} months preparation."
        readiness_score = 35
    else:
        readiness = f"MAJOR GAPS — {critical_count} critical issues. Consider a different target or intensive training."
        readiness_score = 15

    return {
        "gaps": gaps,
        "gap_count": {"critical": sum(1 for g in gaps if g["severity"] in ("HIGH","CRITICAL")),
                      "medium": sum(1 for g in gaps if g["severity"] == "MEDIUM"),
                      "total": len(gaps)},
        "recommendations": recommendations[:10],
        "readiness": readiness,
        "readiness_score": readiness_score,
        "estimated_months_to_ready": timeline_months,
        "level": level,
    }


# ══════════════════════════════════════════════════════════════════════════════
# CAREER PIVOT ADVISOR — Where should you go next?
# ══════════════════════════════════════════════════════════════════════════════
CAREER_PIVOTS = {
    # (from_industry, from_skill) → [(to_role, transferability%, additional_training)]
    ("IT", "python"): [
        ("Data Engineer", 85, "Learn Spark, Airflow — 2 months"),
        ("ML Engineer", 75, "Learn TensorFlow/PyTorch — 3 months"),
        ("DevOps Engineer", 70, "Learn Kubernetes, Terraform — 2 months"),
        ("Cloud Architect", 65, "Get AWS/Azure cert — 3 months"),
    ],
    ("IT", "java"): [
        ("Backend Architect", 85, "Learn microservices, cloud — 2 months"),
        ("Android Developer", 75, "Learn Kotlin — 1 month"),
        ("Technical Lead", 80, "Develop leadership skills"),
    ],
    ("Finance", "accounting"): [
        ("Financial Analyst", 80, "Learn Power BI, SQL — 2 months"),
        ("Compliance Officer", 75, "Learn RegTech — 1 month"),
        ("Data Analyst", 60, "Learn Python, SQL — 3 months"),
        ("FinTech Product Manager", 50, "Learn product management — 4 months"),
    ],
    ("Healthcare", "nursing"): [
        ("Health Informatics", 65, "Learn EHR systems, data — 3 months"),
        ("Clinical Research", 70, "Learn research methodology — 2 months"),
        ("Healthcare Admin", 60, "Get FACHE — 6 months"),
        ("Telehealth Specialist", 80, "Already qualified, learn platforms — 1 month"),
    ],
    ("Marketing", "seo"): [
        ("Growth Hacker", 80, "Learn analytics, A/B testing — 1 month"),
        ("Content Strategist", 75, "Develop editorial skills"),
        ("Product Marketing Manager", 65, "Learn product management — 3 months"),
        ("Data Analyst (Marketing)", 55, "Learn Python, SQL — 3 months"),
    ],
    ("Engineering", "project management"): [
        ("Product Manager", 75, "Learn product frameworks — 2 months"),
        ("Program Manager", 85, "Scale current skills"),
        ("Agile Coach", 70, "Get SAFe/Scrum cert — 1 month"),
        ("Technical Project Manager (IT)", 60, "Learn SDLC, Jira — 2 months"),
    ],
}


def suggest_pivots(current_industry: str, skills: list, years: int) -> list:
    """Suggest career pivots based on transferable skills."""
    pivots = []
    for skill in skills:
        key = (current_industry, skill.lower())
        if key in CAREER_PIVOTS:
            for role, transfer, training in CAREER_PIVOTS[key]:
                pivots.append({
                    "target_role": role,
                    "transferability": f"{transfer}%",
                    "from_skill": skill,
                    "additional_training": training,
                    "salary_change": "+10-25%" if transfer > 70 else "+0-15%" if transfer > 50 else "variable",
                })
    # Deduplicate by role
    seen = set()
    unique = []
    for p in pivots:
        if p["target_role"] not in seen:
            seen.add(p["target_role"])
            unique.append(p)
    return sorted(unique, key=lambda x: int(x["transferability"].rstrip("%")), reverse=True)[:5]


# ══════════════════════════════════════════════════════════════════════════════
# FULL DECISION — The complete picture
# ══════════════════════════════════════════════════════════════════════════════
def full_decision(parsed_resume: dict, job_desc: str = "", country: str = "",
                  industry: str = "", target_role: str = "") -> dict:
    """The COMPLETE career decision — every dimension analyzed."""
    from .career_engine import naked_truth_score, ats_score

    truth = naked_truth_score(parsed_resume, job_desc, country, industry)
    ats = ats_score(parsed_resume["raw_text"], job_desc) if job_desc else {}

    skills = parsed_resume.get("tech_skills", [])
    certs = parsed_resume.get("certifications", [])
    years = parsed_resume.get("experience_years", 0)

    gaps = gap_analysis(skills, certs, years, target_role, industry, country)
    level = classify_level(years)

    # Country fit
    country_code = ""
    if country:
        # Simple country name to code mapping
        name_to_code = {
            "canada": "CA", "usa": "US", "united states": "US", "uk": "GB",
            "united kingdom": "GB", "germany": "DE", "australia": "AU",
            "india": "IN", "uae": "AE", "singapore": "SG", "pakistan": "PK",
            "new zealand": "NZ", "ireland": "IE", "netherlands": "NL",
            "japan": "JP", "south korea": "KR", "nigeria": "NG", "south africa": "ZA",
        }
        country_code = name_to_code.get(country.lower(), country.upper()[:2])

    fit = country_fit_score(country_code, industry, skills, years) if country_code else {}
    pivots = suggest_pivots(industry, skills, years) if industry else []

    return {
        "resume_score": truth,
        "ats_match": ats,
        "experience_level": level,
        "gap_analysis": gaps,
        "country_fit": fit,
        "career_pivots": pivots,
        "decision_summary": {
            "score": truth["composite_score"],
            "readiness": gaps["readiness"],
            "top_strength": truth["strengths"][0] if truth["strengths"] else "None identified",
            "top_weakness": truth["weaknesses"][0] if truth["weaknesses"] else "None identified",
            "hidden_truth": truth["hidden_issues"][0] if truth["hidden_issues"] else "No hidden issues",
            "months_to_ready": gaps["estimated_months_to_ready"],
        },
    }
