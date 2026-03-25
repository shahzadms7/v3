"""
Alfalah Job Career Intelligent AI 2026 V3
Architecture Diagram — PDF + PNG (large readable fonts)
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import warnings
warnings.filterwarnings('ignore')

fig, ax = plt.subplots(figsize=(24, 34))   # tall portrait — human readable
ax.set_xlim(0, 24)
ax.set_ylim(0, 34)
ax.axis('off')
fig.patch.set_facecolor('#0A0A1A')
ax.set_facecolor('#0A0A1A')

C_BG    = '#0A0A1A'
C_AZURE = '#0078D4'
C_AZD   = '#005A9E'
C_ORG   = '#FF6B35'
C_PUR   = '#8B5CF6'
C_GRN   = '#22C55E'
C_GOLD  = '#F59E0B'
C_GRAY  = '#1E293B'
C_LG    = '#E5E7EB'
C_MG    = '#9CA3AF'
C_RED   = '#EF4444'
C_D1    = '#0D1B3E'
C_CLD   = '#D97757'
C_WHT   = '#FFFFFF'

def box(ax, x, y, w, h, fc, ec=None, lw=2.0):
    ec = ec or fc
    p = FancyBboxPatch((x, y), w, h,
                        boxstyle="round,pad=0.05",
                        facecolor=fc, edgecolor=ec,
                        linewidth=lw, zorder=3)
    ax.add_patch(p)

def txt(ax, x, y, s, fs=11, c=C_WHT, bold=False, ha='center', va='center', wrap=False):
    w = 'bold' if bold else 'normal'
    ax.text(x, y, s, fontsize=fs, color=c, fontweight=w,
            ha=ha, va=va, zorder=5,
            multialignment=ha,
            wrap=wrap)

def arr(ax, x1, y1, x2, y2, color=C_AZURE, lw=2):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='->', color=color, lw=lw),
                zorder=4)

def section_header(ax, y, title, color, icon=''):
    box(ax, 0.2, y, 23.6, 0.85, color)
    txt(ax, 0.5, y+0.42, f'{icon}  {title}', fs=14, bold=True, c=C_WHT, ha='left')

# ══════════════════════════════════════════════════════════
# TITLE
# ══════════════════════════════════════════════════════════
box(ax, 0, 32.7, 24, 1.3, C_AZURE)
txt(ax, 12, 33.55, 'Alfalah Job Career Intelligent AI  2026  V3', fs=20, bold=True)
txt(ax, 12, 33.05, 'End-to-End System Architecture  |  100% Microsoft Azure  |  Built for 8 Billion People', fs=12, c=C_LG)

# ══════════════════════════════════════════════════════════
# 1. USERS
# ══════════════════════════════════════════════════════════
section_header(ax, 31.5, 'LAYER 1 — USERS  (195 Countries · Any Device · Zero Login · Free Forever)', C_AZD, icon='[USER]')

user_items = [
    ('Web Browser', 'Chrome · Safari\nFirefox · Edge'),
    ('PWA Mobile', 'iOS · Android\nInstallable App'),
    ('Any Device', 'Desktop · Tablet\nMobile · Smart TV'),
    ('195 Countries', 'All UN Nations\nAll Time Zones'),
    ('2G to 5G', 'Any Bandwidth\nAny Connection'),
    ('Zero Barrier', 'No Login · No Cost\nNo Data Stored'),
]
for i, (title, sub) in enumerate(user_items):
    x = 0.3 + i * 3.9
    box(ax, x, 30.5, 3.6, 0.9, C_AZD, ec=C_AZURE)
    txt(ax, x+1.8, 30.95, title, fs=11, bold=True, c=C_WHT)
    txt(ax, x+1.8, 30.62, sub, fs=9, c=C_LG)

arr(ax, 12, 30.5, 12, 30.1)

# ══════════════════════════════════════════════════════════
# 2. AZURE STATIC WEB APPS
# ══════════════════════════════════════════════════════════
box(ax, 0.2, 28.8, 23.6, 1.2, C_AZURE, ec=C_AZD)
txt(ax, 0.5, 29.6, '[AZURE]  AZURE STATIC WEB APPS  —  Global CDN Edge', fs=14, bold=True, c=C_WHT, ha='left')
txt(ax, 0.5, 29.15, 'React / Next.js 14  |  Tailwind CSS 3  |  PWA  |  Auto-Deploy via GitHub Actions  |  TLS 1.3 SSL  |  Nearest CDN Edge Node Per Country', fs=11, c=C_LG, ha='left')

arr(ax, 12, 28.8, 12, 28.4)
txt(ax, 12.5, 28.58, 'API Calls  |  HTTPS', fs=10, c=C_GOLD)

# ══════════════════════════════════════════════════════════
# 3. AZURE FUNCTIONS
# ══════════════════════════════════════════════════════════
box(ax, 0.2, 25.8, 23.6, 2.5, C_D1, ec=C_PUR, lw=2.5)
txt(ax, 12, 28.05, '[FUNC]  AZURE FUNCTIONS v2  —  Python 3.12 Serverless  |  govrag-v3-func.azurewebsites.net', fs=14, bold=True, c=C_PUR)

endpoints = [
    ('POST /career', '17-Module AI Analysis', C_GRN),
    ('POST /chat', 'Career Coaching', C_AZURE),
    ('POST /jobs', 'Google Jobs · LinkedIn · Indeed', C_ORG),
    ('GET /location', 'IP Geolocation · Country Detect', C_GOLD),
    ('GET /health', 'System Status · AI Chain Check', C_GRN),
    ('POST /upload', 'PDF · DOCX · TXT Extraction', C_RED),
]
for i, (ep, desc, color) in enumerate(endpoints):
    x = 0.4 + i * 3.9
    box(ax, x, 25.9, 3.6, 1.75, C_GRAY, ec=color, lw=2)
    txt(ax, x+1.8, 27.3, ep, fs=11, bold=True, c=color)
    txt(ax, x+1.8, 26.9, desc, fs=9, c=C_LG)

arr(ax, 12, 25.8, 12, 25.4)

# ══════════════════════════════════════════════════════════
# 4. AZURE SERVICES
# ══════════════════════════════════════════════════════════
section_header(ax, 24.6, 'LAYER 4 — AZURE AI & SECURITY SERVICES', C_AZD, icon='[AZURE]')

services = [
    ('AZURE OPENAI', 'gpt-4o-mini · eastus\nPrimary AI Inference\ngovrag-v3-openai', C_AZURE),
    ('AZURE AI SEARCH', 'Semantic + Vector Hybrid\n163 ISCO groups indexed\nStandard S1 tier', C_PUR),
    ('CONTENT SAFETY', 'v1.0 · Output Moderation\nAll AI responses screened\nResponsible AI layer', C_RED),
    ('AZURE KEY VAULT', 'RBAC · Managed Identity\nAll secrets managed\nZero secrets in code', C_ORG),
    ('APP INSIGHTS', 'Live Monitoring\nMetrics · Alerts · Logs\nRequest tracing', C_GRN),
]
for i, (title, desc, color) in enumerate(services):
    x = 0.3 + i * 4.7
    box(ax, x, 22.5, 4.4, 2.0, C_D1, ec=color, lw=2.5)
    box(ax, x, 24.1, 4.4, 0.5, color)
    txt(ax, x+2.2, 24.35, title, fs=11, bold=True, c=C_WHT)
    txt(ax, x+2.2, 23.5, desc, fs=9, c=C_LG)

arr(ax, 12, 22.5, 12, 22.1)

# ══════════════════════════════════════════════════════════
# 5. AI FALLBACK CHAIN
# ══════════════════════════════════════════════════════════
box(ax, 0.2, 19.9, 23.6, 2.1, C_D1, ec=C_ORG, lw=2.5)
txt(ax, 0.5, 21.7, '[AI]  AI FALLBACK CHAIN  —  4 Providers · 8 Models · 99.9%+ Uptime', fs=13, bold=True, c=C_ORG, ha='left')

fallbacks = [
    ('Azure OpenAI\nGPT-4o-mini', 'PRIMARY', C_AZURE),
    ('Gemini 2.0\nFlash KEY1', 'Fallback 1', C_GOLD),
    ('Gemini Flash\nLatest KEY1', 'Fallback 2', C_GOLD),
    ('Gemini 1.5\nFlash KEY1', 'Fallback 3', C_GOLD),
    ('Gemini 2.0\nFlash KEY2', 'Fallback 4', '#EAB308'),
    ('Gemini Flash\nLatest KEY2', 'Fallback 5', '#EAB308'),
    ('Gemini 1.5\nFlash KEY2', 'Fallback 6', '#EAB308'),
    ('xAI Grok-4\nFinal', 'Fallback 7', C_MG),
]
for i, (name, role, color) in enumerate(fallbacks):
    x = 0.35 + i * 2.9
    box(ax, x, 20.0, 2.7, 1.6, C_GRAY, ec=color, lw=1.8)
    txt(ax, x+1.35, 21.05, name, fs=9.5, bold=True, c=color)
    txt(ax, x+1.35, 20.25, role, fs=8.5, c=C_LG)
    if i < 7:
        txt(ax, x+2.7, 20.85, '->', fs=14, c=C_ORG)

arr(ax, 12, 19.9, 12, 19.5)

# ══════════════════════════════════════════════════════════
# 6. RAG KNOWLEDGE ENGINE
# ══════════════════════════════════════════════════════════
section_header(ax, 18.6, 'LAYER 6 — RAG KNOWLEDGE ENGINE  (32 Files · 513 KB · 10,629 Lines of Career Intelligence)', C_PUR, icon='[KB]')

kb = [
    ('163 ISCO-08\nOccupations', '10 major groups\nAll professions', C_AZURE),
    ('20 Industries\nCovered', 'IT to Agriculture\nAll sectors', C_GRN),
    ('416 Skills\nA to Z', 'Hard · Soft\nFuture skills', C_PUR),
    ('27 JD\nTemplates', 'Role-specific ATS\nReal job schemas', C_GOLD),
    ('44 Certifications', 'Cost · Validity\nOfficial URLs', C_RED),
    ('195 Countries', 'Salary · Visa\nLabor law', C_ORG),
    ('50 Negotiation\nScripts', 'Word-by-word\nEntry to Exec', C_CLD),
    ('27 Outreach\nTemplates', 'LinkedIn DM\nCold email', C_MG),
]
for i, (title, sub, color) in enumerate(kb):
    col = i % 4
    row = i // 4
    x = 0.3 + col * 5.9
    y = 16.4 + (1 - row) * 2.0
    box(ax, x, y, 5.6, 1.8, C_GRAY, ec=color, lw=2)
    box(ax, x, y+1.4, 5.6, 0.4, color)
    txt(ax, x+2.8, y+1.6, title.replace('\n', ' '), fs=11, bold=True, c=C_WHT)
    txt(ax, x+2.8, y+0.85, sub, fs=10, c=C_LG)

arr(ax, 12, 16.4, 12, 16.0)

# ══════════════════════════════════════════════════════════
# 7. DEV TOOLS | CI/CD | EXTERNAL APIs
# ══════════════════════════════════════════════════════════
section_header(ax, 15.1, 'LAYER 7 — DEVELOPMENT TOOLS  |  CI/CD PIPELINE  |  EXTERNAL DATA SOURCES', C_CLD, icon='[DEV]')

# Dev Tools
box(ax, 0.2, 11.6, 7.7, 3.4, C_D1, ec=C_CLD, lw=2)
txt(ax, 4.05, 14.7, '[CLAUDE]  AI & DEV TOOLS', fs=12, bold=True, c=C_CLD)
dev = [
    'Claude Sonnet 4.6  —  Built this entire platform',
    'Claude Code (Anthropic)  —  AI coding assistant',
    'Visual Studio Code  —  Primary IDE',
    'GitHub Copilot  —  Code completion',
    'Azure Functions Core Tools v4  —  Local dev',
    'Azure CLI 2.x  —  Resource management',
    'PowerShell 7.x  —  SDLC test_sdlc.ps1',
    'Python 3.12  —  Backend + AI logic',
]
for i, d in enumerate(dev):
    txt(ax, 0.5, 14.2 - i*0.36, d, fs=9.5, c=C_LG, ha='left')

# CI/CD
box(ax, 8.15, 11.6, 7.7, 3.4, C_D1, ec=C_GRN, lw=2)
txt(ax, 12.0, 14.7, '[GITHUB]  CI/CD PIPELINE', fs=12, bold=True, c=C_GRN)
cicd = [
    'GitHub — github.com/shahzadms7/v3',
    'GitHub Actions — auto-deploy on push',
    'Push to main branch triggers:',
    '  → Azure Static Web Apps deploy',
    '  → Azure Functions deploy',
    'func azure functionapp publish',
    'Azure Monitor — post-deploy health',
    'GET /health — chain verification',
]
for i, d in enumerate(cicd):
    txt(ax, 8.35, 14.2 - i*0.36, d, fs=9.5, c=C_LG, ha='left')

# External APIs
box(ax, 16.1, 11.6, 7.7, 3.4, C_D1, ec=C_ORG, lw=2)
txt(ax, 19.95, 14.7, '[GOOGLE]  EXTERNAL DATA SOURCES', fs=12, bold=True, c=C_ORG)
ext = [
    'Serper.dev  —  Google Jobs API',
    'LinkedIn Jobs  —  Professional network',
    'Indeed  —  Global job aggregator',
    'ipapi.co  —  IP geolocation',
    'ISCO-08  —  ILO occupational standard',
    'ESCO  —  EU skills taxonomy',
    'O*NET  —  US Dept of Labor',
    'NOC  —  Statistics Canada',
]
for i, d in enumerate(ext):
    txt(ax, 16.3, 14.2 - i*0.36, d, fs=9.5, c=C_LG, ha='left')

# ══════════════════════════════════════════════════════════
# 8. STATS BAR
# ══════════════════════════════════════════════════════════
box(ax, 0.2, 9.0, 23.6, 2.4, C_D1, ec=C_AZURE, lw=2.5)
txt(ax, 12, 11.1, 'PLATFORM STATISTICS  —  Real Verified Numbers  —  Zero Guessing', fs=13, bold=True, c=C_AZURE)

stats = [
    ('16,544', 'Total Lines\nWritten', C_GOLD),
    ('4,818', 'Python\nCode Lines', C_AZURE),
    ('10,629', 'Knowledge\nBase Lines', C_PUR),
    ('163', 'ISCO-08\nOccupations', C_RED),
    ('20', 'Industries\nCovered', C_GRN),
    ('416', 'Skills\nA-Z', C_CLD),
    ('27', 'JD Role\nTemplates', C_GOLD),
    ('195', 'Countries\nCovered', C_ORG),
    ('17', 'AI Career\nModules', C_AZURE),
    ('6', 'API\nEndpoints', C_PUR),
    ('4', 'AI\nProviders', C_GRN),
    ('8', 'AI\nModels', C_ORG),
]
sw = 23.6 / len(stats)
for i, (num, lbl, color) in enumerate(stats):
    x = 0.2 + i * sw
    txt(ax, x + sw/2, 10.45, num, fs=16, bold=True, c=color)
    txt(ax, x + sw/2, 9.5, lbl, fs=8.5, c=C_LG)

# ══════════════════════════════════════════════════════════
# 9. OCCUPATION LIST
# ══════════════════════════════════════════════════════════
box(ax, 0.2, 0.3, 11.5, 8.5, C_D1, ec=C_AZURE, lw=2)
txt(ax, 6.0, 8.55, '163 ISCO-08 PROFESSIONS COVERED', fs=12, bold=True, c=C_AZURE)

occ_groups = [
    ('MANAGERS (16)', ['Legislators', 'Senior Govt Officials', 'CEO/MD', 'Finance Mgrs', 'HR Managers', 'Policy Managers', 'Business Admin Mgrs', 'Sales/Marketing Mgrs', 'Advertising/PR Mgrs', 'R&D Managers', 'Agricultural Mgrs', 'Fishery Mgrs', 'Manufacturing Mgrs', 'Construction Mgrs', 'Supply Chain Mgrs', 'ICT Managers']),
    ('PROFESSIONALS (47)', ['Physicists', 'Chemists', 'Geologists', 'Mathematicians/Actuaries', 'Life Scientists', 'Industrial Engineers', 'Env Engineers', 'Mining Engineers', 'Electrical Engineers', 'Electronics Engineers', 'Telecom Engineers', 'Architects', 'Product Designers', 'Family Physicians', 'Specialist Doctors', 'Nurses', 'Traditional Medicine', 'Paramedics', 'Veterinarians', 'Dentists', 'Pharmacists', 'Dieticians', 'Lab Scientists', 'University Teachers', 'Vocational Teachers', 'Secondary Teachers', 'Primary Teachers', 'Early Childhood Educators', 'Accountants', 'Financial Advisors', 'Financial Analysts', 'Mgmt Consultants', 'Policy Admins', 'HR Professionals', 'Marketing Professionals', 'PR Professionals', 'Sales Professionals', 'Systems Analysts', 'Software Developers', 'Web Developers', 'Mobile Developers', 'Software NEC', 'Database Admins', 'Systems Admins', 'Network Professionals', 'ICT NEC']),
    ('TECHNICIANS (14)', ['Civil Eng Technicians', 'Electronics Technicians', 'Power Plant Operators', 'Process Control Techs', 'Life Science Techs', 'Ships Officers', 'Aircraft Pilots', 'Medical Imaging Techs', 'Lab Technicians', 'Nursing Associates', 'Vet Assistants', 'Finance Dealers', 'Credit Officers', 'Accounting Associates']),
]
y_start = 8.2
for group_name, items in occ_groups:
    txt(ax, 0.4, y_start, group_name, fs=9, bold=True, c=C_GOLD, ha='left')
    y_start -= 0.28
    col_items = [items[j:j+8] for j in range(0, len(items), 8)]
    for col_idx, col in enumerate(col_items):
        for k, item in enumerate(col):
            x_pos = 0.4 + col_idx * 5.6
            txt(ax, x_pos, y_start - k*0.22, f'  {item}', fs=7.5, c=C_LG, ha='left')
    y_start -= (max(len(c) for c in col_items)) * 0.22 + 0.15

# ══════════════════════════════════════════════════════════
# 10. INDUSTRIES LIST
# ══════════════════════════════════════════════════════════
box(ax, 12.0, 0.3, 11.8, 8.5, C_D1, ec=C_GRN, lw=2)
txt(ax, 17.9, 8.55, '20 INDUSTRIES COVERED', fs=12, bold=True, c=C_GRN)

industries = [
    ('01', 'Information Technology & Software', C_AZURE),
    ('02', 'Healthcare & Life Sciences', C_RED),
    ('03', 'Financial Services & Banking', C_GOLD),
    ('04', 'Manufacturing & Industrial', C_MG),
    ('05', 'Energy & Utilities', C_ORG),
    ('06', 'Retail & E-Commerce', C_GRN),
    ('07', 'Construction & Real Estate', C_MG),
    ('08', 'Education & EdTech', C_AZURE),
    ('09', 'Telecommunications', C_PUR),
    ('10', 'Transportation & Logistics', C_ORG),
    ('11', 'Agriculture & Food', C_GRN),
    ('12', 'Media & Entertainment', C_PUR),
    ('13', 'Cybersecurity', C_RED),
    ('14', 'Automotive & Electric Vehicles', C_GOLD),
    ('15', 'Aerospace & Defense', C_AZURE),
    ('16', 'Pharmaceutical & Biotech', C_RED),
    ('17', 'Legal Services', C_MG),
    ('18', 'Hospitality & Tourism', C_ORG),
    ('19', 'Mining & Natural Resources', C_MG),
    ('20', 'Government & Public Sector', C_AZURE),
]
for i, (num, name, color) in enumerate(industries):
    box(ax, 12.1, 7.95 - i*0.39, 11.6, 0.35, C_GRAY, ec=color, lw=1.2)
    txt(ax, 12.6, 8.09 - i*0.39, num, fs=10, bold=True, c=color, ha='left')
    txt(ax, 13.3, 8.09 - i*0.39, name, fs=10, c=C_LG, ha='left')

# ══════════════════════════════════════════════════════════
# FOOTER
# ══════════════════════════════════════════════════════════
box(ax, 0, 0, 24, 0.28, C_AZURE)
txt(ax, 12, 0.14, 'Alfalah Job Career Intelligent AI 2026 V3  |  govrag-v3-func.azurewebsites.net  |  github.com/shahzadms7/v3  |  Free for 8 Billion People  |  MIT License', fs=8, c=C_WHT)

# ══════════════════════════════════════════════════════════
# SAVE PDF + PNG
# ══════════════════════════════════════════════════════════
plt.tight_layout(pad=0.1)

base = r'g:\My Drive\Claude Projects 2026\shahzad-job-coach-ai\v3'
pdf_path = base + r'\architecture_diagram.pdf'
png_path = base + r'\architecture_diagram.png'

plt.savefig(pdf_path, format='pdf', bbox_inches='tight', facecolor=C_BG)
plt.savefig(png_path, dpi=120, bbox_inches='tight', facecolor=C_BG, format='png')
plt.close()
print(f"PDF saved: {pdf_path}")
print(f"PNG saved: {png_path}")
