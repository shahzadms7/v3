"""
Alfalah Job Career Intelligent AI 2026 V3
Architecture Diagram Generator — Produces PNG image
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import matplotlib.patheffects as pe

# ── Canvas ─────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(28, 18))
ax.set_xlim(0, 28)
ax.set_ylim(0, 18)
ax.axis('off')
fig.patch.set_facecolor('#0A0A1A')
ax.set_facecolor('#0A0A1A')

# ── Color palette ──────────────────────────────────────────────────
C_BG       = '#0A0A1A'
C_AZURE    = '#0078D4'
C_AZURE_D  = '#005A9E'
C_ORANGE   = '#FF6B35'
C_PURPLE   = '#8B5CF6'
C_GREEN    = '#22C55E'
C_GOLD     = '#F59E0B'
C_GRAY     = '#374151'
C_LGRAY    = '#E5E7EB'
C_MGRAY    = '#9CA3AF'
C_RED      = '#EF4444'
C_DARK1    = '#0D1B3E'
C_DARK2    = '#0D1B1B'
C_CLAUDE   = '#D97757'

def box(ax, x, y, w, h, fc, ec=None, radius=0.3, alpha=1.0):
    ec = ec or fc
    p = FancyBboxPatch((x, y), w, h,
                        boxstyle=f"round,pad=0",
                        facecolor=fc, edgecolor=ec,
                        linewidth=1.5, alpha=alpha,
                        zorder=3)
    ax.add_patch(p)
    return p

def label(ax, x, y, txt, fs=8, color='white', bold=False, ha='center', va='center', zorder=5):
    weight = 'bold' if bold else 'normal'
    ax.text(x, y, txt, fontsize=fs, color=color, fontweight=weight,
            ha=ha, va=va, zorder=zorder,
            fontfamily='DejaVu Sans')

def arrow(ax, x1, y1, x2, y2, color=C_AZURE, lw=1.5, style='->', zorder=4):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle=style, color=color,
                                lw=lw, connectionstyle='arc3,rad=0.0'),
                zorder=zorder)

# ══════════════════════════════════════════════════════════════════
# TITLE BAR
# ══════════════════════════════════════════════════════════════════
box(ax, 0, 16.8, 28, 1.2, C_AZURE)
label(ax, 14, 17.6, 'Alfalah Job Career Intelligent AI  2026  V3', fs=16, bold=True, color='white')
label(ax, 14, 17.1, 'End-to-End System Architecture  ·  100% Microsoft Azure  ·  Built for 8 Billion People', fs=10, color=C_LGRAY)

# ══════════════════════════════════════════════════════════════════
# ROW 1 — USERS
# ══════════════════════════════════════════════════════════════════
box(ax, 0.3, 14.8, 27.4, 1.7, C_DARK1, ec=C_AZURE)
label(ax, 14, 16.1, 'USERS — 195 Countries · Any Device · Zero Installation Required', fs=9, bold=True, color=C_AZURE)

users = [
    ('Web Browser\nChrome · Safari\nFirefox · Edge', 1.5),
    ('Progressive\nWeb App (PWA)\niOS · Android', 5.5),
    ('Any Device\nDesktop · Mobile\nTablet · TV', 9.5),
    ('Any Country\n195 UN Nations\nAll Time Zones', 13.5),
    ('Any Connection\nBroadband · 3G\n2G Capable', 17.5),
    ('Zero Barrier\nNo Login · No Cost\nNo Data Stored', 21.5),
]
for txt, x in users:
    box(ax, x, 14.85, 3.5, 1.4, C_AZURE_D, radius=0.2)
    label(ax, x+1.75, 15.55, txt, fs=7.5, color=C_LGRAY)

# ══════════════════════════════════════════════════════════════════
# ARROW DOWN
# ══════════════════════════════════════════════════════════════════
arrow(ax, 14, 14.8, 14, 14.15, color=C_GOLD, lw=2)
label(ax, 14.4, 14.45, 'HTTPS · TLS 1.3', fs=7, color=C_GOLD)

# ══════════════════════════════════════════════════════════════════
# ROW 2 — AZURE STATIC WEB APPS
# ══════════════════════════════════════════════════════════════════
box(ax, 0.3, 13.0, 27.4, 1.0, C_AZURE, ec=C_AZURE_D)
label(ax, 0.8, 13.62, 'AZURE STATIC WEB APPS', fs=9, bold=True, color='white', ha='left')
label(ax, 0.8, 13.18, 'Global CDN Edge · React / Next.js 14 · Tailwind CSS · PWA · Auto-Deploy via GitHub Actions · SSL/TLS · Nearest Edge Node per Country', fs=7.5, color=C_LGRAY, ha='left')
label(ax, 26.5, 13.62, 'CDN', fs=8, bold=True, color=C_GOLD, ha='right')
label(ax, 26.5, 13.18, 'govrag-v3-static', fs=7, color=C_LGRAY, ha='right')

# ARROW
arrow(ax, 14, 13.0, 14, 12.35, color=C_GOLD, lw=2)
label(ax, 14.4, 12.62, 'API Calls', fs=7, color=C_GOLD)

# ══════════════════════════════════════════════════════════════════
# ROW 3 — AZURE FUNCTIONS
# ══════════════════════════════════════════════════════════════════
box(ax, 0.3, 10.5, 27.4, 1.7, C_DARK1, ec=C_PURPLE)
label(ax, 14, 11.9, 'AZURE FUNCTIONS v2  —  Python 3.12 Serverless Backend  ·  govrag-v3-func.azurewebsites.net', fs=9, bold=True, color=C_PURPLE)

endpoints = [
    ('POST /career\n17-Module Analysis', C_GREEN),
    ('POST /chat\nCareer Coaching', C_AZURE),
    ('POST /jobs\nLive Job Search', C_ORANGE),
    ('GET /location\nIP Geolocation', C_GOLD),
    ('GET /health\nSystem Status', C_GREEN),
    ('POST /upload\nFile Extraction', C_RED),
]
ep_x = [0.5, 5.0, 9.5, 14.0, 18.5, 23.0]
for (txt, color), x in zip(endpoints, ep_x):
    box(ax, x, 10.55, 4.2, 1.2, C_GRAY, ec=color, radius=0.2)
    label(ax, x+2.1, 11.15, txt, fs=7.5, color=color)

# ══════════════════════════════════════════════════════════════════
# ARROWS DOWN TO SERVICES
# ══════════════════════════════════════════════════════════════════
for xa in [3.5, 8.5, 13.5, 18.5, 23.5]:
    arrow(ax, xa, 10.5, xa, 9.85, color=C_MGRAY, lw=1.2)

# ══════════════════════════════════════════════════════════════════
# ROW 4 — AZURE AI SERVICES (5 boxes)
# ══════════════════════════════════════════════════════════════════
azure_services = [
    ('AZURE OPENAI\ngpt-4o-mini · eastus\nPrimary AI Inference', C_AZURE, 'govrag-v3-openai'),
    ('AZURE AI SEARCH\nSemantic + Vector\n163 ISCO groups indexed', C_PURPLE, 'Standard S1 · Hybrid'),
    ('AZURE CONTENT\nSAFETY v1.0\nOutput Moderation', C_RED, 'All AI outputs screened'),
    ('AZURE KEY VAULT\nRBAC · Managed ID\nAll Secrets Managed', C_ORANGE, 'govrag-v3-kv'),
    ('APPLICATION\nINSIGHTS\nLive Monitoring', C_GREEN, 'Metrics · Alerts · Logs'),
]
svc_x = [0.4, 5.7, 11.0, 16.3, 21.6]
for (txt, color, sub), x in zip(azure_services, svc_x):
    box(ax, x, 8.3, 5.0, 1.5, C_DARK1, ec=color, radius=0.2)
    box(ax, x, 9.4, 5.0, 0.4, color)
    label(ax, x+2.5, 9.6, txt.split('\n')[0], fs=7.5, bold=True, color='white')
    label(ax, x+2.5, 9.1, txt.split('\n')[1], fs=7, color=C_LGRAY)
    label(ax, x+2.5, 8.65, txt.split('\n')[2], fs=7, color=C_LGRAY)
    label(ax, x+2.5, 8.38, sub, fs=6.5, color=color)

# ══════════════════════════════════════════════════════════════════
# AI FALLBACK CHAIN (horizontal)
# ══════════════════════════════════════════════════════════════════
box(ax, 0.3, 6.9, 27.4, 1.2, C_DARK1, ec=C_ORANGE)
label(ax, 0.8, 7.82, 'AI FALLBACK CHAIN  —  4 Providers · 8 Models · 99.9%+ Uptime', fs=9, bold=True, color=C_ORANGE, ha='left')

fallbacks = [
    ('Azure OpenAI\nGPT-4o-mini\nPRIMARY', C_AZURE),
    ('Google Gemini\n2.0 Flash KEY1\nFallback 1', C_GOLD),
    ('Gemini Flash\nLatest KEY1\nFallback 2', C_GOLD),
    ('Gemini 1.5\nFlash KEY1\nFallback 3', C_GOLD),
    ('Google Gemini\n2.0 Flash KEY2\nFallback 4', '#EAB308'),
    ('Gemini Flash\nLatest KEY2\nFallback 5', '#EAB308'),
    ('Gemini 1.5\nFlash KEY2\nFallback 6', '#EAB308'),
    ('xAI Grok-4\ngrok-4-latest\nFinal Fallback', C_MGRAY),
]
fb_x = [0.4, 3.85, 7.3, 10.75, 14.2, 17.65, 21.1, 24.55]
for (txt, color), x in zip(fallbacks, fb_x):
    box(ax, x, 6.95, 3.1, 0.95, C_GRAY, ec=color, radius=0.15)
    label(ax, x+1.55, 7.42, txt, fs=6.5, color=color)
    if x < 24.55:
        arrow(ax, x+3.1, 7.42, x+3.1+0.05, 7.42, color=C_ORANGE, lw=1, style='->')

# ══════════════════════════════════════════════════════════════════
# ROW 5 — RAG KNOWLEDGE ENGINE
# ══════════════════════════════════════════════════════════════════
box(ax, 0.3, 4.5, 27.4, 2.2, C_DARK1, ec=C_PURPLE)
label(ax, 14, 6.42, 'RAG KNOWLEDGE ENGINE  —  32 Career Files · 513 KB · 16,544 Lines Written · 99% Structured Data · 1% LLM Formatting', fs=9, bold=True, color=C_PURPLE)

kb_items = [
    ('ISCO-08 Occupations\n163 Unit Groups\n990 lines', C_AZURE),
    ('Skills Database\n416 Named Skills\nA-Z Hard+Soft+Future', C_GREEN),
    ('195 Countries\nSalary · Visa\nLabor Law', C_ORANGE),
    ('27 JD Templates\nRole-specific ATS\nKeyword schemas', C_GOLD),
    ('44 Certifications\nCost · Validity\nOfficial URLs', C_RED),
    ('50 Negotiation\nScripts word-by-word\nEntry to Executive', C_PURPLE),
    ('27 Cold Outreach\nLinkedIn DM\nEmail templates', C_CLAUDE),
    ('28 Industry\nTrend Sections\n1,276 lines', C_MGRAY),
    ('Future Jobs\n2026-2125\nEmerging roles', C_GREEN),
]
kb_x = [0.45, 3.45, 6.45, 9.45, 12.45, 15.45, 18.45, 21.45, 24.45]
for (txt, color), x in zip(kb_items, kb_x):
    box(ax, x, 4.55, 2.72, 1.65, C_GRAY, ec=color, radius=0.15)
    label(ax, x+1.36, 5.37, txt, fs=6.5, color=color)

# ══════════════════════════════════════════════════════════════════
# ROW 6 — DEV TOOLS + CI/CD + EXTERNAL APIs
# ══════════════════════════════════════════════════════════════════
# Dev Tools
box(ax, 0.3, 2.5, 8.8, 1.8, C_DARK1, ec=C_CLAUDE)
label(ax, 4.7, 4.05, 'AI & DEV TOOLS', fs=8, bold=True, color=C_CLAUDE)
dev_tools = [
    'Claude Sonnet 4.6 — Built this platform',
    'Claude Code — AI coding assistant (VS Code)',
    'Visual Studio Code — Primary IDE',
    'GitHub Copilot — Code completion',
    'Azure Functions Core Tools v4',
    'PowerShell 7.x — SDLC test_sdlc.ps1',
]
for i, t in enumerate(dev_tools):
    label(ax, 0.6, 3.72 - i*0.2, t, fs=6.5, color=C_LGRAY, ha='left')

# CI/CD
box(ax, 9.4, 2.5, 9.2, 1.8, C_DARK1, ec=C_GREEN)
label(ax, 14.0, 4.05, 'CI/CD PIPELINE', fs=8, bold=True, color=C_GREEN)
cicd = [
    'GitHub — github.com/shahzadms7/v3',
    'GitHub Actions — auto-deploy on git push',
    'Azure CLI 2.x — resource management',
    'func azure functionapp publish',
    'git push origin main → auto-deploys both',
    'Static Web Apps + Functions simultaneously',
]
for i, t in enumerate(cicd):
    label(ax, 9.6, 3.72 - i*0.2, t, fs=6.5, color=C_LGRAY, ha='left')

# External APIs
box(ax, 18.9, 2.5, 9.1, 1.8, C_DARK1, ec=C_ORANGE)
label(ax, 23.45, 4.05, 'EXTERNAL APIs & DATA SOURCES', fs=8, bold=True, color=C_ORANGE)
ext = [
    'Serper.dev — Google Jobs live listings',
    'LinkedIn Jobs — professional network',
    'Indeed — global job aggregator',
    'ipapi.co — IP geolocation · country detect',
    'ISCO-08 ILO · ESCO EU · O*NET US BLS',
    'NOC Canada · SOC US Bureau Labor Stats',
]
for i, t in enumerate(ext):
    label(ax, 19.1, 3.72 - i*0.2, t, fs=6.5, color=C_LGRAY, ha='left')

# ══════════════════════════════════════════════════════════════════
# ROW 7 — BOTTOM STATS BAR
# ══════════════════════════════════════════════════════════════════
box(ax, 0.3, 0.3, 27.4, 2.0, C_DARK1, ec=C_AZURE)
label(ax, 14, 2.05, 'PLATFORM STATISTICS  —  Real Facts · Verified Counts · Naked Truth', fs=9, bold=True, color=C_AZURE)

stats = [
    ('16,544', 'Total Lines\nWritten', C_GOLD),
    ('4,818', 'Python\nBackend', C_AZURE),
    ('10,629', 'Markdown\nKnowledge Base', C_PURPLE),
    ('32', 'Career\nKB Files', C_GREEN),
    ('513 KB', 'Knowledge\nBase Size', C_ORANGE),
    ('163', 'ISCO-08\nOccupations', C_RED),
    ('416', 'Named\nSkills A-Z', C_CLAUDE),
    ('17', 'Career AI\nModules', C_GOLD),
    ('195', 'Countries\nCovered', C_GREEN),
    ('6', 'API\nEndpoints', C_AZURE),
    ('4', 'AI\nProviders', C_PURPLE),
    ('8', 'AI\nModels', C_ORANGE),
    ('0', 'Data\nStored', C_GREEN),
    ('0', 'Login\nRequired', C_GOLD),
]
stat_w = 27.4 / len(stats)
for i, (num, lbl, color) in enumerate(stats):
    x = 0.3 + i * stat_w
    label(ax, x + stat_w/2, 1.52, num, fs=11, bold=True, color=color)
    label(ax, x + stat_w/2, 0.95, lbl, fs=6, color=C_LGRAY)

# ══════════════════════════════════════════════════════════════════
# VERTICAL SIDE LABEL
# ══════════════════════════════════════════════════════════════════
# Left side — PYTHON
box(ax, 0, 4.5, 0.25, 6.5, C_AZURE_D)
# Right side — AZURE
box(ax, 27.75, 4.5, 0.25, 6.5, C_AZURE)

# ══════════════════════════════════════════════════════════════════
# SAVE
# ══════════════════════════════════════════════════════════════════
plt.tight_layout(pad=0)
out = r'g:\My Drive\Claude Projects 2026\shahzad-job-coach-ai\v3\architecture_diagram.png'
plt.savefig(out, dpi=150, bbox_inches='tight',
            facecolor=C_BG, edgecolor='none')
plt.close()
print(f"Diagram saved: {out}")
