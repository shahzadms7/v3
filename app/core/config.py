"""
GovRAG V3 — Central Configuration
Created: March 21, 2026 | Microsoft Hackathon

HOW IT WORKS (for Shahzad & Zara):
This file is the CONTROL PANEL. Every setting lives here.
- API keys loaded from environment variables (never hardcoded)
- AI model settings (temperature, tokens)
- Safety thresholds (when to block, when to warn)
- Azure resource names
Change a setting here → affects the entire app.
"""

import os
from pathlib import Path
from pydantic_settings import BaseSettings

# Project root directory
PROJECT_ROOT = Path(__file__).parent.parent.parent


class Settings(BaseSettings):
    """All app settings — loaded from .env file or environment variables."""

    # ── Project Info ──────────────────────────────────────────────────────────
    APP_NAME: str = "GovRAG V3 — Grounded Knowledge Assistant"
    APP_VERSION: str = "3.0.0"
    APP_DESCRIPTION: str = "Governed RAG for compliance + career intelligence | 8 billion humans"
    ENVIRONMENT: str = "development"

    # ── AI Provider (100% Microsoft Azure Stack) ────────────────────────────────
    # Alfalah AI 2026: Exclusive Azure OpenAI deployment for Hackathon
    AZURE_OPENAI_ENDPOINT: str = os.getenv("AZURE_OPENAI_ENDPOINT", "")
    AZURE_OPENAI_KEY: str = os.getenv("AZURE_OPENAI_KEY", "")
    AZURE_OPENAI_DEPLOYMENT: str = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4o-mini")
    AZURE_OPENAI_API_VERSION: str = "2024-12-01-preview"

    # ── AI Model Settings (Optimized for Speed + Accuracy) ─────────────────────
    AI_TEMPERATURE: float = 0.3      # Low = precise, deterministic, reproducible
    AI_MAX_TOKENS: int = 1500        # REDUCED from 4096 for fast responses (<30s total)
    AI_TIMEOUT_SECONDS: int = 28     # REDUCED from 55 → faster fallback + module batching

    # ── Azure AI Search ───────────────────────────────────────────────────────
    AZURE_SEARCH_ENDPOINT: str = ""
    AZURE_SEARCH_KEY: str = ""
    AZURE_SEARCH_INDEX: str = "govrag-docs"

    # ── Azure Blob Storage ────────────────────────────────────────────────────
    AZURE_STORAGE_CONNECTION_STRING: str = ""
    AZURE_STORAGE_CONTAINER: str = "documents"

    # ── Azure Monitor ─────────────────────────────────────────────────────────
    APPLICATIONINSIGHTS_CONNECTION_STRING: str = ""

    # ── RAG Settings ──────────────────────────────────────────────────────────
    RAG_TOP_K: int = 5               # How many chunks to retrieve
    RAG_MIN_RELEVANCE: float = 0.3   # Minimum relevance score to include
    RAG_CHUNK_SIZE: int = 512        # Tokens per chunk
    RAG_CHUNK_OVERLAP: int = 128     # Overlap between chunks

    # ── Safety Thresholds ─────────────────────────────────────────────────────
    SAFETY_BLOCK_THRESHOLD: int = 40   # Below this % = BLOCKED (too risky)
    SAFETY_WARN_THRESHOLD: int = 70    # Below this % = WARNING added
    SAFETY_MAX_QUERY_LENGTH: int = 2000
    SAFETY_MAX_RESUME_LENGTH: int = 8000
    SAFETY_MAX_JOB_DESC_LENGTH: int = 4000

    # ── Rate Limiting (Optimized for 17 Parallel Career Modules) ──────────────
    RATE_LIMIT_PER_HOUR: int = 300   # INCREASED from 50 → supports parallel execution
    RATE_LIMIT_ENABLED: bool = True  # 300 reqs/hour = 5 reqs/min = concurrent-friendly

    # ── Data Paths ────────────────────────────────────────────────────────────
    DATA_DIR: Path = PROJECT_ROOT / "data"
    CAREER_DATA_DIR: Path = PROJECT_ROOT / "data" / "career"
    COMPLIANCE_DATA_DIR: Path = PROJECT_ROOT / "data" / "compliance"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


# Singleton settings instance
settings = Settings()
