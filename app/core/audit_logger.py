"""
GovRAG V3 — Audit Logger (In-Memory + Azure Monitor)
Created: March 21, 2026 | Microsoft Hackathon

HOW IT WORKS (for Shahzad & Zara):
Every question asked → logged with timestamp, confidence, sources used.
We log METRICS only, NEVER user data (privacy-first).

In-memory: Fast access for dashboard (last 500 entries, lost on restart)
Azure Monitor: Permanent audit trail via structured console logs
  (App Insights picks up JSON from stdout automatically)

WHAT WE LOG: timestamp, confidence%, faithfulness%, sources count, latency
WHAT WE NEVER LOG: user query text, resume content, any PII
"""

import time
import json
from datetime import datetime
from typing import Optional


class AuditEntry:
    """One audit record — what happened during a query."""

    def __init__(self, query_hash: str, verdict: str, confidence: int = 0,
                 faithfulness: int = 0, sources_count: int = 0,
                 provider: str = "", model: str = "", latency_ms: int = 0,
                 warnings: list = None, mode: str = "compliance"):
        self.id = f"audit-{int(time.time())}-{query_hash[:8]}"
        self.timestamp = datetime.utcnow().isoformat() + "Z"
        self.verdict = verdict  # ALLOW, WARN, BLOCK, ERROR
        self.confidence = confidence
        self.faithfulness = faithfulness
        self.sources_count = sources_count
        self.provider = provider
        self.model = model
        self.latency_ms = latency_ms
        self.warnings = warnings or []
        self.mode = mode  # "compliance" or "career"

    def to_dict(self):
        return {
            "id": self.id,
            "timestamp": self.timestamp,
            "verdict": self.verdict,
            "confidence": self.confidence,
            "faithfulness": self.faithfulness,
            "sources_count": self.sources_count,
            "provider": self.provider,
            "model": self.model,
            "latency_ms": self.latency_ms,
            "warnings": self.warnings,
            "mode": self.mode,
        }


class AuditLogger:
    """In-memory audit trail + Azure Monitor integration."""

    def __init__(self, max_entries: int = 500):
        self.entries: list[AuditEntry] = []
        self.max_entries = max_entries

    def log(self, **kwargs) -> str:
        """Log an audit entry. Returns audit ID."""
        import hashlib
        query_hash = hashlib.md5(str(time.time()).encode()).hexdigest()
        entry = AuditEntry(query_hash=query_hash, **kwargs)

        # Console log (Azure Monitor picks this up via App Insights)
        print(json.dumps({"type": "GovRAG_Audit", **entry.to_dict()}))

        # In-memory store (for dashboard)
        self.entries.append(entry)
        if len(self.entries) > self.max_entries:
            self.entries = self.entries[-self.max_entries:]

        return entry.id

    def get_metrics(self) -> dict:
        """Aggregate metrics for dashboard."""
        if not self.entries:
            return {
                "total_queries": 0, "avg_confidence": 0, "avg_faithfulness": 0,
                "avg_latency_ms": 0, "block_rate": 0, "total_blocked": 0,
                "hallucination_warnings": 0, "queries_today": 0,
            }

        total = len(self.entries)
        blocked = sum(1 for e in self.entries if e.verdict == "BLOCK")
        today = datetime.utcnow().date().isoformat()
        today_entries = [e for e in self.entries if e.timestamp.startswith(today)]

        with_conf = [e for e in self.entries if e.confidence > 0]
        with_faith = [e for e in self.entries if e.faithfulness > 0]
        with_lat = [e for e in self.entries if e.latency_ms > 0]

        return {
            "total_queries": total,
            "queries_today": len(today_entries),
            "avg_confidence": round(sum(e.confidence for e in with_conf) / len(with_conf)) if with_conf else 0,
            "avg_faithfulness": round(sum(e.faithfulness for e in with_faith) / len(with_faith)) if with_faith else 0,
            "avg_latency_ms": round(sum(e.latency_ms for e in with_lat) / len(with_lat)) if with_lat else 0,
            "block_rate": round((blocked / total) * 100) if total else 0,
            "total_blocked": blocked,
            "hallucination_warnings": sum(1 for e in self.entries if e.faithfulness < 50 and e.faithfulness > 0),
            "by_mode": {
                "compliance": sum(1 for e in self.entries if e.mode == "compliance"),
                "career": sum(1 for e in self.entries if e.mode == "career"),
            },
            "by_verdict": {
                "allow": sum(1 for e in self.entries if e.verdict == "ALLOW"),
                "warn": sum(1 for e in self.entries if e.verdict == "WARN"),
                "block": blocked,
                "error": sum(1 for e in self.entries if e.verdict == "ERROR"),
            },
        }

    def get_recent(self, limit: int = 20) -> list[dict]:
        """Get recent audit entries for dashboard."""
        return [e.to_dict() for e in reversed(self.entries[-limit:])]


# Singleton
audit_logger = AuditLogger()
