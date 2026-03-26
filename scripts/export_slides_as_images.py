"""
Export all PPTX slides as PNG images into docs/screenshots/
Uses PowerPoint COM automation (Windows only).
Run: python scripts/export_slides_as_images.py
"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

import os
from pathlib import Path
import win32com.client

BASE       = Path(__file__).parent.parent
PPTX_FILE  = BASE / "Alfalah_AI_2026_V3.pptx"
OUT_DIR    = BASE / "docs" / "screenshots"
OUT_DIR.mkdir(parents=True, exist_ok=True)

print(f"Opening: {PPTX_FILE}")
print(f"Saving to: {OUT_DIR}")

powerpoint = win32com.client.Dispatch("PowerPoint.Application")
powerpoint.Visible = True

try:
    prs = powerpoint.Presentations.Open(str(PPTX_FILE.resolve()), ReadOnly=True, Untitled=False, WithWindow=False)

    total = prs.Slides.Count
    print(f"Slides found: {total}")

    for i in range(1, total + 1):
        slide = prs.Slides(i)
        out_path = OUT_DIR / f"slide_{i:02d}.png"
        # Export at 1920x1080 resolution (ppExportAsPNG = 32)
        slide.Export(str(out_path.resolve()), "PNG", 1920, 1080)
        print(f"  Slide {i:02d} → {out_path.name}")

    prs.Close()
    print(f"\nDone. {total} slides saved to docs/screenshots/")

finally:
    powerpoint.Quit()
