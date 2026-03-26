"""
Career Intelligence Modules — 17 Specialized AI Generators
Each module is a specialized career advisor for a specific task.
Designed to run in PARALLEL for <30second total latency.

Built for: Shahzad Muhammad & Zara Irfan | Alfalah AI 2026
"""

from typing import Optional, Dict, List
from .career_engine import parse_resume
from .decision_engine import classify_level, country_fit_score, gap_analysis


# ══════════════════════════════════════════════════════════════════════════════
# MODULE PROMPTS (Each specialized for fast AI generation)
# ══════════════════════════════════════════════════════════════════════════════

MODULES = {
    "resume_score": {
        "name": "Tool 01: Resume Score",
        "description": "Algorithmic ATS score across 8 weighted dimensions",
        "prompt": """Evaluate this resume for ATS (Applicant Tracking System) and recruiter readiness.
Score 0-100 on these 8 dimensions:
1. Format compliance (fonts, structure, keywords) — 0-15 points
2. Contact info quality (email, phone, LinkedIn, portfolio) — 0-10 points
3. Keywords density (industry-specific terms, job description match) — 0-15 points
4. Quantification (metrics, numbers, percentages) — 0-15 points
5. Chronological clarity (dates, progression, gaps) — 0-10 points
6. Recency (recent experience, current skills) — 0-10 points
7. Achievement framing (action verbs, STAR method) — 0-15 points
8. Professional tone (clarity, grammar, no red flags) — 0-10 points

Return JSON:
{
  "score": 0-100,
  "rating": "WEAK|FAIR|GOOD|STRONG|EXCELLENT",
  "dimensions": {"format": 12, "contact": 8, ...},
  "top_strengths": ["strength 1", "strength 2"],
  "critical_weaknesses": ["weakness 1", "weakness 2"],
  "ats_keywords_found": 35,
  "ats_keywords_needed": ["keyword 1"],
  "verdict": "Your resume would be caught by ATS 70% of the time"
}""",
    },
    "recruiter_pov": {
        "name": "Tool 02: Recruiter Perspective",
        "description": "How a hiring manager evaluates your resume in 6 seconds",
        "prompt": """You are a recruiter with 200 applications on your desk. You scan each resume in 6 seconds.
What do you NOTICE vs MISS in this resume?

Simulate your 6-second skim:
- First visible: Contact/headline
- Second (2s): Recent role titles + companies
- Third (4s): Top 3 bullet achievements
- Stop (6s): Enough or skip?

Return JSON:
{
  "first_impression": "What grabs attention in 2 seconds",
  "second_glance": "What they read in seconds 2-4",
  "decision_at_6s": "STRONG PASS|PASS|MAYBE|SKIP",
  "what_stands_out": ["achievement 1", "credential 2"],
  "what_gets_missed": ["buried achievement 1", "unclear skill 2"],
  "quick_fixes_to_pop": ["Move X to top", "Add metric to Y"],
  "recruiter_comment": "What a recruiter would think but not say"
}""",
    },
    "skills_gap": {
        "name": "Tool 03: Skills Gap Analysis",
        "description": "Hard and soft skills matched against the job description",
        "prompt": """Compare candidate skills vs job description requirements.
Identify EXACT gaps.

Return JSON:
{
  "hard_skills_match": ["skill 1 FOUND", "skill 2 MISSING"],
  "soft_skills_assessment": {"leadership": "demonstrated", "mentoring": "not shown"},
  "certification_needs": ["CKA [HIGH]", "CISSP [MED]"],
  "ats_keywords_match": 88,
  "upskilling_roadmap": {
    "month_1": "Research + learn X",
    "month_2": "Complete certification Y",
    "month_3": "Build portfolio project Z"
  },
  "timeline_to_top_1_percent": "6 months",
  "training_resources": [{"name": "Course X", "cost": "free", "duration": "4 weeks"}]
}""",
    },
    "resume_rewrite": {
        "name": "Tool 04: Resume Rewrite",
        "description": "Diagnosis, measurable-win extraction, rebuilt resume",
        "prompt": """Rewrite this resume using TOP 1% standards.
STEP 1: Diagnose current issues
STEP 2: Extract every measurable win
STEP 3: Rebuild with impact-first bullets

Return JSON:
{
  "diagnosis": ["Issue 1: Missing metrics", "Issue 2: Weak verbs"],
  "measurable_wins_found": 5,
  "rewritten_bullets": [
    {"original": "Managed the platform", "rewritten": "Led 8-person team to ship 12 enterprise features, increasing ARR by $2.3M (35%)"},
  ],
  "before_after_comparison": {"before_word_count": 350, "after_word_count": 280},
  "improvement_summary": "Stronger, tighter, more metrics-driven"
}""",
    },
    "cover_letter": {
        "name": "Tool 05: Cover Letter",
        "description": "Role-specific cover letter with strong opening, 3 quantified achievements",
        "prompt": """Write a STRONG cover letter that gets opened.
Structure:
- Paragraph 1: Hook (why THIS role, THIS company)
- Paragraph 2: Achievement 1 + metric
- Paragraph 3: Achievement 2 + metric
- Paragraph 4: Achievement 3 + metric
- Paragraph 5: Call to action (bold, confident)

Return JSON:
{
  "opening_hook": "The first sentence that makes them read on",
  "achievement_1": {"story": "...", "metric": "35% increase"},
  "achievement_2": {"story": "...", "metric": "$2.3M revenue"},
  "achievement_3": {"story": "...", "metric": "90% efficiency"},
  "closing_cta": "Your confident call to action",
  "full_letter": "Complete letter text"
}""",
    },
    "interview_prep": {
        "name": "Tool 06: Interview Preparation",
        "description": "5 likely questions with model answers + strategic countequestions",
        "prompt": """Generate 5 interview questions likely for this role.
Include model answers using STAR method.
Plus: Strategic questions to ask THEM.

Return JSON:
{
  "likely_questions": [
    {
      "question": "Q1: Tell me about a time you faced a major challenge",
      "category": "BEHAVIORAL",
      "model_answer": "S: ... T: ... A: ... R: Achieved X",
      "tips": "Lead with metric, highlight leadership"
    }
  ],
  "questions_to_ask_them": [
    "What are the key success metrics for this role in 90 days?",
    "How does the team collaborate with product and design?"
  ]
}""",
    },
    "star_stories": {
        "name": "Tool 07: STAR Behavioural Stories",
        "description": "Three structured STAR examples with metrics",
        "prompt": """Extract and format 3 STAR stories from resume.
Each: Situation → Task → Action → Result

Return JSON:
{
  "story_1": {
    "title": "Biggest impact achievement",
    "situation": "Context and challenge...",
    "task": "What I was responsible for...",
    "action": "What I did specifically...",
    "result": "Metric: 99.99% uptime, $2M saved"
  },
  "story_2": {"title": "Leadership story", ...},
  "story_3": {"title": "Learning/growth story", ...}
}""",
    },
    "linkedin_about": {
        "name": "Tool 08: LinkedIn About Section",
        "description": "SEO-optimized LinkedIn summary for recruiter discovery",
        "prompt": """Write a LinkedIn About section that:
- Ranks for recruiter searches
- Includes top 5 keywords
- Opens with hook in first 2 sentences
- Includes call to action

Return JSON:
{
  "about_section": "Complete text for LinkedIn About (2000 chars)",
  "target_keywords": ["SRE", "Kubernetes", "Platform Engineering", "DevOps", "Cloud Architecture"],
  "seo_optimization_score": 92,
  "hook_first_2_sentences": "The opening that makes recruiters click"
}""",
    },
    "intro_scripts": {
        "name": "Tool 09: Professional Introduction Scripts",
        "description": "1-minute, 2-minute, 3-minute verbal introductions",
        "prompt": """Create 3 introduction scripts for different contexts.

Return JSON:
{
  "intro_30s": "My elevator pitch for hallway conversations",
  "intro_1m": "My introduction for networking events",
  "intro_3m": "My introduction for interviews or panels",
  "key_stories": ["story 1 to tell", "story 2 to tell"],
  "delivery_tips": ["Pace: 140 words/min", "Pause after key metrics", "End with question"]
}""",
    },
    "thank_you_email": {
        "name": "Tool 10: Post-Interview Thank You Email",
        "description": "Follow-up email that reinforces candidacy",
        "prompt": """Write a post-interview thank you email that:
- Reinforces top 2 achievements discussed
- Adds NEW insight they didn't know
- Shows you listened (reference specific comment)
- Clear call to action

Return JSON:
{
  "subject": "Subject line",
  "body": "Complete email text",
  "key_differentiator": "The specific insight that makes you memorable",
  "response_rate_tip": "Send within 2 hours of interview"
}""",
    },
    "salary_negotiation": {
        "name": "Tool 11: Salary Negotiation",
        "description": "Market salary ranges, negotiation scripts",
        "prompt": """Provide salary negotiation guidance.

Return JSON:
{
  "market_range": {"low": 120000, "market": 150000, "high": 180000, "currency": "USD"},
  "range_by_level": {
    "junior": "$90K-$120K",
    "mid": "$120K-$160K",
    "senior": "$150K-$200K"
  },
  "opening_script": "How to respond to 'What's your salary expectation?'",
  "counter_offer_script": "If they say 'We can only do $X'",
  "negotiation_phrases": [
    "Based on my research and experience, I'd like to explore $X",
    "I'm excited about the role. I was hoping for $X range"
  ],
  "benefits_to_negotiate": ["Stock options", "Signing bonus", "Remote work", "PTO"]
}""",
    },
    "action_plan_90": {
        "name": "Tool 12: 30-60-90 Day Action Plan",
        "description": "Structured onboarding plan with milestones",
        "prompt": """Create a 30-60-90 day job search / onboarding plan.

Return JSON:
{
  "month_1": {
    "week_1": "Goal: Find 5 target companies",
    "week_2": "Goal: Connect with 3 people at each company",
    "week_3": "Goal: Apply to roles, at least 1 interview secured",
    "week_4": "Goal: 2 interviews scheduled"
  },
  "month_2": {
    "focus": "Deepen relationships",
    "week_5": "Start informational interviews",
    "week_6": "Submit applications to target roles",
    "week_7": "Prep for interviews",
    "week_8": "Interview stretch goal: 2-3 offers"
  },
  "month_3": {
    "focus": "Close and onboard",
    "deliverables": "Accepted offer, start date set, prep for day 1"
  },
  "success_metrics": ["5 interviews by day 60", "1 offer by day 90"]
}""",
    },
    "cold_outreach": {
        "name": "Tool 13: Cold Outreach Templates",
        "description": "LinkedIn DM, cold email, follow-up sequence",
        "prompt": """Create 4 cold outreach templates personalized for this candidate.

Return JSON:
{
  "linkedin_connection_note": "Connection request message (160 chars)",
  "linkedin_dm": "First DM after they accept connection",
  "cold_email": "Email to hiring manager or recruiter",
  "follow_up_email": "Follow-up if no response after 5 days",
  "personalization_tips": [
    "Mention something specific from their profile",
    "Reference a recent company update or news"
  ],
  "response_rate_expectations": "Cold email: 5-10% response rate"
}""",
    },
    "career_pivot": {
        "name": "Tool 14: Career Pivot Analysis",
        "description": "Pivot difficulty score + 3 adjacent roles + 90-day roadmap",
        "prompt": """Analyze career pivot opportunity.

Return JSON:
{
  "pivot_difficulty_score": 6,
  "pivot_rating": "Moderately difficult (6/10)",
  "adjacent_roles_you_qualify_for": [
    {"role": "Platform Engineer", "fit_score": 85, "gap_months": 3},
    {"role": "DevOps Engineer", "fit_score": 92, "gap_months": 1},
    {"role": "Site Reliability Engineer", "fit_score": 88, "gap_months": 2}
  ],
  "transition_roadmap_90_days": {
    "week_1_2": "Learn X certification",
    "week_3_4": "Build portfolio project in Y",
    "week_5_8": "Apply to roles, network with Z people"
  },
  "skills_to_add": ["Skill 1", "Skill 2"],
  "success_probability": "92% chance of landing similar role within 6 months"
}""",
    },
    "labor_law": {
        "name": "Tool 15: Labour Law and Compliance",
        "description": "Jurisdiction-specific notice period, termination rights, non-compete",
        "prompt": """Provide labor law guidance for candidate's jurisdiction.

Return JSON:
{
  "country": "Canada",
  "province": "Ontario",
  "notice_period_required": "2 weeks minimum",
  "termination_rights": "Can be fired without cause with severance",
  "non_compete_enforceability": "Valid only if reasonable (time, geography, industry)",
  "resume_red_flags_by_law": ["Gap of 3+ years without explanation", "Frequent job-hopping"],
  "compliance_guidelines": ["Include actual dates", "Never claim experience you don't have"],
  "labor_standards_links": [{"name": "Ontario ESA", "url": "..."}]
}""",
    },
    "visa_pathway": {
        "name": "Tool 16: Visa and Immigration Pathways",
        "description": "In-country requirements + cross-border visa routes with URLs",
        "prompt": """Provide visa and immigration guidance.

Return JSON:
{
  "from_country": "Pakistan",
  "target_countries": [
    {
      "country": "Canada",
      "visa_type": "Express Entry / Skilled Worker",
      "processing_time": "6 months",
      "official_url": "https://immigration.canada.ca",
      "difficulty": "Moderate (points-based)",
      "requirements": ["Job offer (optional)", "Language test (IELTS/TOEFL)"]
    },
    {
      "country": "United States",
      "visa_type": "H-1B / EB-3",
      "processing_time": "12+ months",
      "official_url": "https://www.uscis.gov",
      "difficulty": "Hard (lottery, cap-dependent)""
    }
  ],
  "easiest_pathways": ["Canada: Express Entry", "Australia: Skilled Migration"],
  "fastest_visas": ["Germany: EU Blue Card (45 days)", "UAE: Work Visa (14 days)"]
}""",
    },
    "matching_jobs": {
        "name": "Tool 17: Matching Job Titles and Boards",
        "description": "Recommended job titles, target companies, regional job boards",
        "prompt": """Suggest job titles, companies, and where to find openings.

Return JSON:
{
  "job_titles_to_search": [
    "Site Reliability Engineer",
    "Platform Engineer",
    "DevOps Engineer",
    "Cloud Architect"
  ],
  "target_companies": [
    {"name": "Netflix", "industry": "Tech", "hiring_for": "SRE", "link": "netflix.com/jobs"},
    {"name": "Stripe", "industry": "Fintech", "hiring_for": "Platform Engineer"}
  ],
  "regional_job_boards": [
    {"country": "Canada", "board": "Workopolis", "url": "workopolis.com", "relevance": "high"},
    {"country": "Canada", "board": "LinkedIn", "url": "linkedin.com/jobs", "relevance": "very high"}
  ],
  "freelance_platforms": [
    {"platform": "Upwork", "hourly_rate_range": "$75-$150"},
    {"platform": "Toptal", "hourly_rate_range": "$100-$250"}
  ],
  "salary_expectations_by_board": "Workopolis: $120-160K | LinkedIn: $130-180K"
}""",
    },
    "live_jobs": {
        "name": "Tool 20: Live Job Openings",
        "description": "Real job listings posted in last 7 days",
        "prompt": """Search for recent job openings.

Return JSON:
{
  "jobs_found_last_7_days": 127,
  "top_matches": [
    {
      "title": "Senior SRE",
      "company": "Company X",
      "location": "Toronto, Canada",
      "posted": "2 days ago",
      "match_score": 95,
      "link": "https://..."
    }
  ],
  "search_filters_used": ["SRE role", "Canada location", "Last 7 days"],
  "shortcut_boards": {
    "google_jobs": "https://google.com/jobs/...",
    "linkedin": "https://linkedin.com/jobs/...",
    "indeed": "https://indeed.com/jobs/..."
  }
}""",
    },
}


# ══════════════════════════════════════════════════════════════════════════════
# FAST MODULE GENERATORS (each optimized for speed)
# ══════════════════════════════════════════════════════════════════════════════

async def generate_module(module_key: str, resume_text: str, job_description: str = "", 
                         country: str = "CA", industry: str = "Gen", ai_provider=None) -> Dict:
    """
    Generate one career module.
    Each module is a specialized AI call optimized for speed.
    """
    if module_key not in MODULES:
        return {"error": f"Module {module_key} not found"}

    module = MODULES[module_key]
    
    # Parse resume once
    parsed = parse_resume(resume_text)
    
    # Context
    context = f"""CANDIDATE PROFILE:
- Experience: {parsed.get('years_experience', 0)} years
- Skills: {', '.join(parsed.get('skills', [])[:5])}
- Education: {', '.join(parsed.get('education', [])[:2])}
- Certifications: {', '.join(parsed.get('certifications', [])[:3])}
- Country: {country}
- Industry: {industry}

RESUME:
{resume_text[:1500]}

{f'JOB DESCRIPTION:{job_description[:800]}' if job_description else ''}"""

    
    # Generate
    if ai_provider:
        result = await ai_provider.generate(
            system_prompt=f"You are a specialized {module['name']} advisor. {module['prompt']}",
            user_prompt=context
        )
        return {
            "module": module_key,
            "name": module["name"],
            "result": result.get("text", "ERROR generating result"),
            "confidence": 85,
        }
    
    return {"error": "No AI provider available"}
